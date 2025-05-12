import inflect
import asyncio
import re
from asyncio import Queue
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional, Union
from hydra.core.config_store import ConfigStore
from hydra.utils import instantiate
from pydantic import BaseModel
from hydra import compose, initialize_config_dir
from services_api import planner
import copy
from llm_sorter.models import APIModel, BaseLLMModel
from llm_sorter import WandbLogger
from llm_sorter.environment import ItemsEvent
from llm_sorter.datasets import (
    LLPTask,
    HLPTask,
    LLPStep,
    BaseTask,
    VCTask,
    SpecTask,
    CleanRoomTask,
)
from llm_sorter.infrastructure import SorterPlannerConfig
from llm_sorter.gen_methods import BasePlanGeneration, FullPlanGeneration
from llm_sorter.processors import (
    LLPProcessor,
    HLPProcessor,
    ValidCheckProcessor,
    SpecProcessor,
    CleanRoomProcessor,
)


cs = ConfigStore.instance()
cs.store(name="sorter_planner", node=SorterPlannerConfig)


class Action(BaseModel):
    name: str
    args: list


class Response(BaseModel):
    plan: list[Action]


class RequestRetry(BaseModel):
    goal: str = ""
    commands: list = []
    invalid_command_index: int = -1
    error_code: str = ""
    world_state: dict = {}
    seg_track: dict = {}
    scene_graph: dict = {}


class PlannerOutputType(Enum):
    RobotAction = "RobotAction"
    FeedbackRequest = "FeedbackRequest"
    UnvalidTask = "UnvalidTask"
    HumanMsg = "HumanMsg"
    Done = "Done"
    CleanAllRoom = "CleanAllRoom"


class HumanMsgType(Enum):
    UnvalidTask = "UnvalidTask"
    PlannerIsBusy = "PlannerIsBusy"
    FeedbackIsNotNeeded = "FeedbackIsNotNeeded"


@dataclass
class PlannerOutput:
    data: Union[str, LLPStep]
    type: PlannerOutputType

    def __str__(self):
        return f"[{self.type.value}] {self.data}"


@dataclass
class HumanMsg:
    data: str
    type: HumanMsgType

    def __str__(self) -> str:
        return f"[{self.type.value}] {self.data}"


def find_waypoint_for_shelf(shelf_id, waypoints_data, logger):
    """Finds the waypoint ID associated with a given shelf ID."""
    if shelf_id == -1 or not waypoints_data:
        logger.debug(f"Cannot find waypoint for invalid shelf_id ({shelf_id}) or empty waypoints_data.")
        return -1 # Invalid shelf or no waypoints

    # *** Adjust this matching logic based on your waypoint naming convention ***
    target_waypoint_name_part = f"{shelf_id}"
    # target_waypoint_name_part = str(shelf_id) # Alternative

    for wp_entry in waypoints_data:
        wp_name = wp_entry.get('name', '')
        wp_id = wp_entry.get('waypoint_id', -1)
        # Ensure wp_id is valid and name matches (adjust matching as needed)
        if wp_id != -1 and target_waypoint_name_part in wp_name:
            logger.debug(f"Found waypoint {wp_id} (name: '{wp_name}') for shelf {shelf_id}.")
            return wp_id

    logger.warning(f"Could not find waypoint containing '{target_waypoint_name_part}' for shelf {shelf_id}.")
    return -1 # Indicate waypoint not found

# --- Helper function to find an available free shelf and its waypoint ---
def find_available_shelf_and_waypoint(shelves_placement, waypoints_data, assigned_shelves_set, logger):
    """Finds the first free shelf not in assigned_shelves_set and its waypoint."""
    if not isinstance(shelves_placement, list):
         logger.error("Shelves placement data is not a list.")
         return None, None

    for shelf_info in shelves_placement:
        shelf_id = shelf_info.get('shelf_id', -1)
        # Use the correct key based on your data ('occupied_by_box_with_id' or similar)
        occupied_by = shelf_info.get('occupied_by_box_with_id', None)

        # Check if shelf is valid, free, and not already assigned
        if shelf_id != -1 and occupied_by == -1 and shelf_id not in assigned_shelves_set:
            logger.info(f"Found potentially free shelf: {shelf_id}. Checking waypoint...")
            waypoint_id = find_waypoint_for_shelf(shelf_id, waypoints_data, logger)
            if waypoint_id != -1:
                logger.info(f"Found available free shelf {shelf_id} with waypoint {waypoint_id}.")
                # Mark as assigned *by the caller* if they decide to use it
                return shelf_id, waypoint_id
            else:
                 logger.warning(f"Shelf {shelf_id} is free but corresponding waypoint not found.")

    logger.warning("Could not find any available free shelf with a valid waypoint.")
    return None, None # Return None if no suitable shelf/waypoint found

# --- Helper to find shelf for a given box ID ---
def find_shelf_for_box(box_id, boxes_placement_data, logger):
    """Finds the shelf ID a given box is placed on."""
    if not isinstance(boxes_placement_data, list):
        logger.error("Boxes placement data is not a list.")
        return -1
        
    for entry in boxes_placement_data:
        if entry.get('box_id') == box_id:
            shelf_id = entry.get('placed_on_shelf_with_id', -1)
            if shelf_id != -1:
                 logger.debug(f"Box {box_id} found on shelf {shelf_id}.")
                 return shelf_id
            else:
                 # Box found but not on a shelf (-1)
                 logger.debug(f"Box {box_id} found but not placed on a shelf.")
                 return -1 # Indicate not on a shelf
                 
    logger.warning(f"Box {box_id} not found in boxes_placement data.")
    return -1 # Indicate box not found

# --- Helper to create command dictionaries ---
def make_command(name, **args):
    """Creates a dictionary representing a command."""
    return {"name": name, "args": args}

class SorterPlanner:
    def __init__(
        self,
        logger: WandbLogger,
        llp_processor: LLPProcessor,
        hlp_processor: HLPProcessor,
        vc_processor: ValidCheckProcessor,
        spec_processor: SpecProcessor,
        clean_room_processor: CleanRoomProcessor,
        model: BaseLLMModel,
        gen_method: FullPlanGeneration,
        **kwargs,
    ) -> None:
        self._logger: WandbLogger = logger
        self._model: BaseLLMModel = model
        self._p = inflect.engine()

        self._llp_processor: LLPProcessor = llp_processor
        self._hlp_processor: HLPProcessor = hlp_processor
        self._vc_processor: ValidCheckProcessor = vc_processor
        self._spec_processor: SpecProcessor = spec_processor
        self._clean_room_processor: CleanRoomProcessor = clean_room_processor

        self._gen_method: BasePlanGeneration = gen_method

        self.reset()

    def reset(self):
        self._robot_q: Queue[LLPStep] = Queue()
        self._human_q: Queue[HumanMsg] = Queue()
        self._llm_q: Queue[BaseTask] = Queue()
        self._waiting_q: Queue[HLPTask] = Queue()

        self._reset: bool = False
        self._logger.info("[Reset]")

    def process_task_sync(self, planner_request: planner.PlannerRequest):
        world_state_disc = ""

        hlp_input_goal = planner_request.goal + world_state_disc
        task = HLPTask(goal=hlp_input_goal)

        pred_hlp_task: HLPTask = self._gen_method.predict(task, self._hlp_processor)
        self._logger.info(f"[HLP] {task.goal} {task.feedback.items} -> {pred_hlp_task.subtasks}")
        pred_llp_steps: list[LLPStep] = []
        for llp_task in pred_hlp_task.subtasks:
            pred_llp_task: LLPTask = self._gen_method.predict(llp_task, self._llp_processor)
            pred_llp_steps.extend(pred_llp_task.steps)


        world_model = planner_request.world_model.dict()
        seg_n_track_tele_data = planner_request.telemetry.dict()
        perception_data = seg_n_track_tele_data.get('seg_track', {})

        self._logger.debug(f"Input Waypoints Data: {world_model.get('waypoints', 'MISSING')}")
        self._logger.debug(f"Input Shelves Perception: {perception_data.get('shelves', 'MISSING')}")
        self._logger.debug(f"Input Boxes Perception: {perception_data.get('boxes_output', 'MISSING')}")

        boxes_placement = perception_data.get('boxes_output', [])
        shelves_placement = perception_data.get('shelves', [])
        waypoints_data = world_model.get("waypoints", [])

        # --- Main Processing Logic ---
        final_command_list = []
        assigned_free_shelves = set()
        # *** NEW: Dictionary to map waypoints assigned via "free" back to their shelf ID ***
        waypoint_to_shelf_map = {}

        self._logger.info("Starting main processing loop...")
        for i, step in enumerate(pred_llp_steps):
            self._logger.debug(f"Processing original step index {i}: {step}")
            try:
                 dicted_step = step.to_dict(...) # Simplified
            except Exception as e:
                 self._logger.error(f"Failed to convert step {i} to dict: {e}. Skipping.")
                 continue

            step_name = dicted_step.get("name")
            step_args = dicted_step.get("args", {}) # Get args safely
            process_this_step = True
            self._logger.debug(f"  Step {i}: name='{step_name}', args={step_args}")


            # --- 1. Check for Stacking Conflict on Pick Up ---
            if step_name == "pick_up" and perception_data.get('box_on_box') is True:
                target_box_id = step_args.get('box_id')
                graph_info = perception_data.get('graph_box_on_box')

                if target_box_id is not None and isinstance(graph_info, dict):
                    top_box_id = graph_info.get('id_1')
                    bottom_box_id = graph_info.get('id_2')

                    # **Intervention needed if target is the bottom box**
                    if target_box_id == bottom_box_id:
                        self._logger.info(f"Stacking conflict detected: Trying to pick up bottom box {bottom_box_id} while top box {top_box_id} is present.")

                        # Find location of the stack (use bottom box, should be same shelf as top)
                        stack_shelf_id = find_shelf_for_box(bottom_box_id, boxes_placement, self._logger)
                        stack_waypoint_id = find_waypoint_for_shelf(stack_shelf_id, waypoints_data, self._logger)

                        # Find a free shelf to place the top box
                        free_shelf_id, free_shelf_waypoint_id = find_available_shelf_and_waypoint(
                            shelves_placement, waypoints_data, assigned_free_shelves, self._logger
                        )

                        if stack_waypoint_id != -1 and free_shelf_id is not None and free_shelf_waypoint_id is not None:
                             self._logger.info(f"Found stack waypoint {stack_waypoint_id} and free shelf {free_shelf_id} (waypoint {free_shelf_waypoint_id}). Inserting unstack steps.")
                             
                             # Mark the free shelf as assigned *now* because we are using it
                             assigned_free_shelves.add(free_shelf_id)

                             # Insert unstacking commands
                             final_command_list.append(make_command("move_to", waypoint_id=stack_waypoint_id))
                             final_command_list.append(make_command("pick_up", box_id=top_box_id))
                             final_command_list.append(make_command("move_to", waypoint_id=free_shelf_waypoint_id))
                             final_command_list.append(make_command("drop", box_id=top_box_id, shelf_id=free_shelf_id)) # Use shelf_id for drop
                             
                             # The original pick_up command for bottom_box_id will be processed next (process_this_step remains True)
                             self._logger.info(f"Inserted 4 steps to move box {top_box_id} to shelf {free_shelf_id}.")
                        
                        else:
                             # Failed to find necessary locations/free shelf
                             self._logger.error(f"CRITICAL: Cannot resolve stacking conflict for picking up box {bottom_box_id}. "
                                                f"Stack waypoint: {stack_waypoint_id}, Free shelf: {free_shelf_id}, Free waypoint: {free_shelf_waypoint_id}. "
                                                f"Skipping original pick up command.")
                             process_this_step = False # Do not add the original blocked pick_up command

                    # Implicit else: If target_box_id == top_box_id, or not involved in stack, proceed normally.

                elif target_box_id is None:
                     self._logger.warning(f"Pick_up command has 'box_on_box' perception but missing 'box_id' in args: {step_args}")
                elif not isinstance(graph_info, dict):
                     self._logger.warning(f"Perception has 'box_on_box' true but 'graph_box_on_box' is missing or not a dict: {graph_info}")

            # --- 2. Process "free" arguments (only if the step wasn't skipped) ---
            if process_this_step and step_args:
                 args_modified = False
                 # Use items() for potentially modifying values safely
                 for arg_key, arg_value in list(step_args.items()): 

                     # ***** Use exact match for "free" value *****
                     if arg_value == "free":
                         self._logger.info(f"  Free Check Step {i}: Found 'free' for command '{step_name}' arg '{arg_key}'.")
                         replacement_value = None
                         shelf_to_assign = None # Track shelf ID if we assign one

                         # --- Logic for "move_to" / "go_to" ---
                         if (step_name == "move_to" or step_name == "go_to") and arg_key == "waypoint_id":
                              self._logger.debug(f"    Resolving 'free' for move command waypoint...")
                              free_shelf_id, free_shelf_waypoint_id = find_available_shelf_and_waypoint(
                                  shelves_placement, waypoints_data, assigned_free_shelves, self._logger
                              )
                              if free_shelf_id is not None and free_shelf_waypoint_id is not None:
                                  replacement_value = free_shelf_waypoint_id
                                  shelf_to_assign = free_shelf_id
                                  # Store the mapping for potential later use by 'drop'
                                  waypoint_to_shelf_map[free_shelf_waypoint_id] = free_shelf_id
                                  self._logger.info(f"    -> Assigned waypoint {replacement_value} (for shelf {shelf_to_assign}). Stored mapping.")
                              else:
                                  self._logger.error(f"    -> CRITICAL: Could not find available free shelf/waypoint for move command.")

                         # --- Logic for "drop" / "place" ---
                         elif (step_name == "drop" or step_name == "place") and arg_key == "shelf_id":
                              self._logger.debug(f"    Resolving 'free' for drop command shelf_id...")
                              # Look at the PREVIOUS command added to the list
                              if final_command_list: # Check if not the first command
                                   previous_cmd = final_command_list[-1]
                                   prev_cmd_name = previous_cmd.get("name")
                                   prev_cmd_args = previous_cmd.get("args", {})
                                   self._logger.debug(f"    Checking previous command: {prev_cmd_name}, args={prev_cmd_args}")

                                   # Check if previous command was a move command
                                   if (prev_cmd_name == "move_to" or prev_cmd_name == "go_to") and "waypoint_id" in prev_cmd_args:
                                        target_waypoint_id = prev_cmd_args["waypoint_id"]
                                        # Check if this waypoint resulted from a "free" assignment
                                        if target_waypoint_id in waypoint_to_shelf_map:
                                             mapped_shelf_id = waypoint_to_shelf_map[target_waypoint_id]
                                             replacement_value = mapped_shelf_id
                                             # We are REUSING the assignment, don't need to add to assigned_free_shelves again
                                             shelf_to_assign = None # Indicate no *new* shelf was assigned here
                                             self._logger.info(f"    -> Found preceding move to waypoint {target_waypoint_id}, using mapped shelf {replacement_value} for drop.")
                                        else:
                                             self._logger.warning(f"    -> Preceding move targeted waypoint {target_waypoint_id}, but it wasn't found in the 'free' assignment map ({waypoint_to_shelf_map}). Cannot determine shelf for drop.")
                                   else:
                                        self._logger.warning(f"    -> Preceding command '{prev_cmd_name}' is not a recognized move command with a waypoint_id. Cannot determine shelf for drop.")
                              else:
                                   self._logger.warning("    -> Drop command with 'free' shelf_id is the first command. Cannot determine target shelf.")
                              
                              # If lookup failed, log error (handled implicitly below if replacement_value is still None)

                         # --- Fallback / Unknown ---
                         else:
                              self._logger.warning(f"    Command '{step_name}' requested 'free' for arg '{arg_key}', but the combination is not handled for automatic assignment. Leaving as 'free'.")


                         # --- Apply Replacement ---
                         if replacement_value is not None:
                             step_args[arg_key] = replacement_value
                             args_modified = True
                             # Assign shelf only if a *new* one was found (for move_to)
                             if shelf_to_assign is not None:
                                  assigned_free_shelves.add(shelf_to_assign)
                                  self._logger.debug(f"    Marked shelf {shelf_to_assign} as assigned.")
                         elif arg_value == "free": # Check arg_value again in case logic above didn't handle it
                             # Log error only if we didn't find a replacement for an expected case
                             if (step_name in ["move_to", "go_to"] and arg_key == "waypoint_id") or \
                                (step_name in ["drop", "place"] and arg_key == "shelf_id"):
                                 self._logger.error(f"    -> CRITICAL: Failed to find replacement for 'free' for command '{step_name}' arg '{arg_key}'. Leaving as 'free'. Plan might fail!")


                 if args_modified:
                      dicted_step["args"] = step_args # Update args in the step dict

            # --- 3. Append the processed step (if not skipped) ---
            if process_this_step:
                self._logger.debug(f"  Appending step {i} to final_command_list: {dicted_step}")
                final_command_list.append(dicted_step)
            else:
                self._logger.debug(f"  Skipping appending original step {i}.")

        # --- 4. Post-Processing: Adjust move_to before pick_up ---
        # Iterate through the *final* list to fix waypoints just before pick ups
        processed_command_list = [] # Create yet another list to avoid issues modifying while iterating
        for j, current_cmd in enumerate(final_command_list):
            cmd_name = current_cmd.get("name")
            cmd_args = current_cmd.get("args", {})
            
            # Default: add the command as is
            command_to_add = copy.deepcopy(current_cmd) # Use deepcopy to be safe

            if cmd_name == "pick_up" and "box_id" in cmd_args and j > 0:
                box_to_pick = cmd_args["box_id"]
                # Check the command *that now actually precedes it* in the final list
                previous_cmd = final_command_list[j-1] 
                prev_cmd_name = previous_cmd.get("name")
                prev_cmd_args = previous_cmd.get("args", {})

                if (prev_cmd_name == "move_to" or prev_cmd_name == "go_to") and "waypoint_id" in prev_cmd_args:
                    # Find the *current* perceived location of the box we are about to pick up
                    current_shelf_id = find_shelf_for_box(box_to_pick, boxes_placement, self._logger)
                    correct_waypoint_id = find_waypoint_for_shelf(current_shelf_id, waypoints_data, self._logger)
                    
                    original_wp = prev_cmd_args['waypoint_id']
                    
                    if correct_waypoint_id != -1 and original_wp != correct_waypoint_id:
                         # We need to modify the PREVIOUS command that was ALREADY added 
                         # to processed_command_list in the previous iteration (j-1).
                         if processed_command_list: # Ensure list is not empty
                            command_to_modify = processed_command_list[-1] # Get the last added command
                            if command_to_modify.get("name") == prev_cmd_name and command_to_modify.get("args",{}).get("waypoint_id") == original_wp:
                                self._logger.info(f"Post-processing: Adjusting preceding '{prev_cmd_name}' (index {j-1}) waypoint from {original_wp} to {correct_waypoint_id} for picking up box {box_to_pick} at shelf {current_shelf_id}.")
                                command_to_modify["args"]["waypoint_id"] = correct_waypoint_id
                            else:
                                self._logger.warning(f"Post-processing: Mismatch trying to modify preceding command for pickup at index {j}. Last added cmd: {command_to_modify.get('name')}, Expected: {prev_cmd_name}")
                         else:
                             self._logger.warning(f"Post-processing: Cannot modify preceding command for pickup at index {j} as processed list is empty.")

                    elif correct_waypoint_id == -1:
                         self._logger.warning(f"Post-processing: Cannot find current location/waypoint for box {box_to_pick} to adjust preceding move command for pickup at index {j}.")
                    # else: No adjustment needed if waypoint already correct or couldn't find location
            
            processed_command_list.append(command_to_add)

        self._logger.info(f"Final Processed Plan: {processed_command_list}") # Use processed_command_list here
        return {"plan": processed_command_list}


    async def add_task(self, goal: str) -> None:
        if not self._llm_q.empty() or not self._robot_q.empty():
            msg = HumanMsg(data="Planner is busy", type=HumanMsgType.PlannerIsBusy)
            self._human_q.put_nowait(msg)
        else:
            await self._llm_q.put(CleanRoomTask(goal=goal))
            self._logger.info(f"[Added HLP task] {goal}")

    async def do_planning(self):
        while True:
            # while not self._robot_q.empty() and not self._reset:
            # output = self._robot_q.get_nowait()
            # await self.process_output(output)

            if not self._llm_q.empty() and not self._reset:
                task = await self._llm_q.get()
                await self.process_task(task)

            # while not self._human_q.empty() and not self._reset:
            #     msg = await self._human_q.get()
            #     await self.process_human_msg(msg)

            if self._reset:
                self.reset()

            await asyncio.sleep(0.1)

    async def get_planner_output(self) -> Optional[PlannerOutput]:
        if not self._human_q.empty():
            output = await self._human_q.get()
            self._logger.info(f"[Human msg] {output}")
            output = PlannerOutput(data=output.data, type=PlannerOutputType.HumanMsg)
            return output
        elif not self._robot_q.empty():
            output = await self._robot_q.get()
            self._logger.info(f"[Processed output] {output}")
            return output
        elif self._llm_q.empty() and self._robot_q.empty() and self._human_q.empty():
            self._logger.info("[Error] Planner is empty")
            output = PlannerOutput(data="empty", type=PlannerOutputType.HumanMsg)
            return output
        else:
            return None

    async def valid_check(self, goal: str) -> None:
        task = VCTask(goal=goal)
        pred_vc_task: VCTask = self._gen_method.predict(task, self._vc_processor)
        return pred_vc_task.valid_plan

    async def add_llp_task(self, goal: str) -> None:
        if not self._llm_q.empty() or not self._robot_q.empty():
            msg = HumanMsg(data="Planner is busy", type=HumanMsgType.PlannerIsBusy)
            await self._human_q.put(msg)
        else:
            await self._llm_q.put(LLPTask(goal=goal))
            self._logger.info(f"[Added LLP task] {goal}")

    async def add_feedback(self, feedback: List[str]) -> None:
        if self._waiting_q.empty():
            msg = HumanMsg(data="Feedback is not needed", type=HumanMsgType.FeedbackIsNotNeeded)
            await self._human_q.put(msg)
        else:
            hlp_task: HLPTask = await self._waiting_q.get()
            # add feedback
            hlp_task.feedback = ItemsEvent(items=feedback)
            await self._llm_q.put(hlp_task)

    async def process_task(self, task: Union[VCTask, HLPTask, LLPTask]):
        """Process a given task based on its type with the LLM model.

        Args:
            task (Union[VCTask, HLPTask, LLPTask]): The task to be processed.
        Raises:
            ValueError: If the task type is not recognized.
        """
        if isinstance(task, CleanRoomTask):
            pred_cr_task: CleanRoomTask = self._gen_method.predict(task, self._clean_room_processor)
            self._logger.info(f"[CR] {task.goal} -> {pred_cr_task.clean_room}")

            if pred_cr_task.clean_room:
                await self._robot_q.put(PlannerOutput(data="CleanAllRoom", type=PlannerOutputType.CleanAllRoom))
            else:
                await self._llm_q.put(VCTask(goal=task.goal))
        elif isinstance(task, VCTask):
            pred_vc_task: VCTask = self._gen_method.predict(task, self._vc_processor)
            self._logger.info(f"[VC] {task.goal} -> {pred_vc_task.valid_plan}")

            if pred_vc_task.valid_plan:
                await self._llm_q.put(SpecTask(goal=task.goal))
            else:
                await self._robot_q.put(PlannerOutput(data="Unvalid task", type=PlannerOutputType.UnvalidTask))
        elif isinstance(task, SpecTask):
            pred_spec_task: SpecTask = self._gen_method.predict(
                task,
                self._spec_processor,
            )
            self._logger.info(f"[Spec] {task.goal} -> {pred_spec_task.request}")

            if pred_spec_task.need_feedback:
                await self._robot_q.put(
                    PlannerOutput(
                        data=pred_spec_task.request,
                        type=PlannerOutputType.FeedbackRequest,
                    )
                )
                await self._waiting_q.put(HLPTask(goal=task.goal))
            else:
                await self._llm_q.put(HLPTask(goal=task.goal))

        elif isinstance(task, HLPTask):
            pred_hlp_task: HLPTask = self._gen_method.predict(task, self._hlp_processor)
            self._logger.info(f"[HLP] {task.goal} {task.feedback.items} -> {pred_hlp_task.subtasks}")
            for llp_task in pred_hlp_task.subtasks:
                await self._llm_q.put(llp_task)

            # if no subtasks
            await self.subtask_done()

        elif isinstance(task, LLPTask):
            # Predict full plan with LLM
            pred_llp_task: LLPTask = self._gen_method.predict(task, self._llp_processor)
            self._logger.info(f"[LLP] {task.goal} -> {pred_llp_task.steps}")

            # Process separated steps
            # for example: move, pick_up, put
            for step in pred_llp_task.steps:
                await self._robot_q.put(PlannerOutput(data=step, type=PlannerOutputType.RobotAction))
            # When subtask is done, add "subtask done"
            await self._robot_q.put(PlannerOutput(data=LLPStep("subtask_done"), type=PlannerOutputType.Done))
            await self.subtask_done()
        else:
            raise ValueError("Wrong task type")

    async def subtask_done(self):
        # No other subtasks. Full plan is done.
        if self._llm_q.empty():
            await self._robot_q.put(PlannerOutput(data=LLPStep("task_done"), type=PlannerOutputType.Done))

    async def process_output(self, output: PlannerOutput):
        self._logger.info(f"[Processed output] {output}")

    async def process_human_msg(self, msg: HumanMsg):
        self._logger.info(f"[Human msg] {msg}")


def get_planner_from_cfg(
    cfg: Optional[SorterPlannerConfig] = None,
    config_path="/app/packages/llm_sorter/config/",
    config_name="sorter_planner_as_package",
) -> SorterPlanner:
    with initialize_config_dir(version_base=None, config_dir=config_path, job_name="llm_sorter"):
        cfg: SorterPlannerConfig = compose(config_name=config_name, overrides=[])
    logger: WandbLogger = instantiate(cfg.logger)
    model: APIModel = instantiate(cfg.model, logger=logger)
    gen_method: FullPlanGeneration = instantiate(cfg.gen_method, model=model, logger=logger)
    llp_processor: LLPProcessor = instantiate(cfg.llp_processor, logger=logger)
    hlp_processor: HLPProcessor = instantiate(cfg.hlp_processor, logger=logger)
    vc_processor: HLPProcessor = instantiate(cfg.vc_processor, logger=logger)
    spec_processor: SpecProcessor = instantiate(cfg.spec_processor, logger=logger)
    clean_room_processor: CleanRoomProcessor = instantiate(cfg.clean_room_processor, logger=logger)

    my_planner = SorterPlanner(
        logger=logger,
        llp_processor=llp_processor,
        hlp_processor=hlp_processor,
        vc_processor=vc_processor,
        spec_processor=spec_processor,
        clean_room_processor=clean_room_processor,
        model=model,
        gen_method=gen_method,
    )
    return my_planner


def get_planner_from_parameters(
    log_dir: Path = Path("outputs/sorter_planner"),
    log_filename: Path = Path("run.log"),
    project_name: str = "llm_sorter",
    run_name: str = "vicuna13b full_plan",
    url: str = "http://127.0.0.1:8080/",
    model_name="vicuna13b docker",
    llp_path_to_prompt_dir: str = "prompts/llp",
    llp_prompt_filename: str = "vlm_llp.txt",
    hlp_path_to_prompt_dir: str = "prompts/hlp",
    hlp_prompt_filename: str = "warehouse_hlp.txt",
    vc_path_to_prompt_dir: str = "prompts/valid_check",
    vc_prompt_filename: str = "valid_check.txt",
    spec_path_to_prompt_dir: str = "prompt/spec",
    spec_prompt_filename: str = "vicuna_prompt.txt",
) -> SorterPlanner:
    logger: WandbLogger = WandbLogger(
        log_dir=log_dir,
        log_filename=log_filename,
        project_name=project_name,
        run_name=run_name,
        log_to_stdout=True,
    )
    model: APIModel = APIModel(logger=logger, name=model_name, url=url)
    gen_method: FullPlanGeneration = FullPlanGeneration(model=model, logger=logger)
    llp_processor: LLPProcessor = LLPProcessor(
        logger,
        path_to_prompt_dir=llp_path_to_prompt_dir,
        prompt_filename=llp_prompt_filename,
        load_prompt_from_file=True,
    )
    hlp_processor: HLPProcessor = HLPProcessor(
        logger=logger,
        path_to_prompt_dir=hlp_path_to_prompt_dir,
        prompt_filename=hlp_prompt_filename,
        load_prompt_from_file=True,
    )
    vc_processor: ValidCheckProcessor = ValidCheckProcessor(
        logger=logger,
        path_to_prompt_dir=vc_path_to_prompt_dir,
        prompt_filename=vc_prompt_filename,
    )
    spec_processor: SpecProcessor = SpecProcessor(
        logger=logger,
        path_to_prompt_dir=spec_path_to_prompt_dir,
        prompt_filename=spec_prompt_filename,
    )
    planner = SorterPlanner(
        logger=logger,
        llp_processor=llp_processor,
        hlp_processor=hlp_processor,
        vc_processor=vc_processor,
        spec_processor=spec_processor,
        model=model,
        gen_method=gen_method,
    )
    return planner

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional
import re
from llm_sorter import WandbLogger
from llm_sorter.datasets import BaseDataset, BaseTask


@dataclass
class LLPStep:
    """Step in Low Level Planning task"""

    action: str = ""
    arguments: List[str] = field(default_factory=list)
    text: str = ""

    def __str__(self) -> str:
        return f"{self.action}({', '.join(self.arguments)})"

    def __repr__(self) -> str:
        return str(self)

    def to_dict(self, world_state: dict = None, telemetry: dict = None) -> dict:
        args = {}
        if self.action == "say":
            args = {"text": self.arguments[0]}
        elif self.action == "go_to":
            # --- Handling for "free" keyword ---
            if "free" in self.arguments[0]:
                # Directly use "free" as the identifier
                args = {"waypoint_id": "free"}
            # --- Original logic for other go_to arguments ---
            elif world_state: # Check if world_state is provided for other cases
                waypoint_id = -1 # Default value
                if "box" in self.arguments[0]:  # its box
                    try:
                        box_id = int(re.search(r"\d+", self.arguments[0]).group())
                        shelf_id = 0 # Default
                        # Ensure telemetry and necessary structures exist
                        if telemetry and "world_state" in telemetry and hasattr(telemetry["world_state"], "boxes"):
                           for box in telemetry["world_state"].boxes:  # find shelf_id
                                if box.box_id == box_id:
                                    shelf_id = box.placed_on_shelf_with_id
                                    break
                        if shelf_id == 6:
                            shelf_id = "table"
                        elif shelf_id == 7:
                            shelf_id = "oader" # Assuming 'loader' was intended?
                        # Find waypoint matching the determined shelf/location
                        if "waypoints" in world_state:
                           for entry in world_state["waypoints"]:
                                if str(shelf_id) in entry["name"]:
                                    waypoint_id = entry["waypoint_id"]
                                    break
                    except (AttributeError, TypeError, IndexError, ValueError):
                        # Handle cases where regex fails or data is missing/malformed
                        print(f"Warning: Could not process go_to box argument: {self.arguments[0]}")
                        waypoint_id = -1 # Or handle error appropriately

                elif "table" in self.arguments[0]:  # its table
                    if "waypoints" in world_state:
                       for entry in world_state["waypoints"]:
                            if "table" in entry["name"]:
                                waypoint_id = entry["waypoint_id"]
                                break
                elif "oader" in self.arguments[0]:  # its loader (assuming typo correction)
                     if "waypoints" in world_state:
                       for entry in world_state["waypoints"]:
                            if "oader" in entry["name"]: # Match "loader"
                                waypoint_id = entry["waypoint_id"]
                                break
                else:  # its regular shelf (assume numeric ID)
                    try:
                        shelf_id = int(re.search(r"\d+", self.arguments[0]).group())
                        if "waypoints" in world_state:
                           for entry in world_state["waypoints"]:
                                if str(shelf_id) in entry["name"]:
                                    waypoint_id = entry["waypoint_id"]
                                    break
                    except (AttributeError, TypeError, IndexError, ValueError):
                         print(f"Warning: Could not process go_to shelf argument: {self.arguments[0]}")
                         waypoint_id = -1 # Or handle error appropriately

                # Only assign if not handled by the "free" case above
                if "waypoint_id" not in args:
                     args = {"waypoint_id": waypoint_id}
            else:
                 # Fallback if world_state not provided but needed for non-"free" args
                 # Or if argument doesn't match known patterns
                 try:
                     # Attempt to extract number as fallback waypoint ID
                     waypoint_id_fallback = int(re.search(r"\d+", self.arguments[0]).group())
                     args = {"waypoint_id": waypoint_id_fallback}
                 except (AttributeError, TypeError, IndexError, ValueError):
                     print(f"Warning: Could not determine waypoint for go_to: {self.arguments[0]} without world_state/telemetry or matching pattern.")
                     args = {"waypoint_id": -1} # Default error value


        elif self.action == "pick_up":
            try:
                args = {"box_id": int(re.search(r"\d+", self.arguments[0]).group())}
            except (AttributeError, TypeError, IndexError, ValueError):
                 print(f"Warning: Could not process pick_up argument: {self.arguments[0]}")
                 args = {"box_id": -1} # Default error value

        elif self.action == "drop":
             # --- Handling for "free" keyword ---
            if "free" in self.arguments[0]:
                 # Directly use "free" as the identifier
                 args = {"shelf_id": "free"}
            # --- Original logic for other drop arguments ---
            else:
                shelf_id = 0 # Default value
                if "table" in self.arguments[0]:  # its table
                    if world_state and "shelves" in world_state:
                        for entry in world_state["shelves"]:
                            if "table" in entry["name"]:
                                shelf_id = entry["shelf_id"]
                                break
                elif "oader" in self.arguments[0]:  # its loader
                     if world_state and "shelves" in world_state:
                        for entry in world_state["shelves"]:
                            if "oader" in entry["name"]:
                                shelf_id = entry["shelf_id"]
                                break
                else:  # its regular shelf (assume numeric ID)
                    try:
                        shelf_id = int(re.search(r"\d+", self.arguments[0]).group())
                    except (AttributeError, TypeError, IndexError, ValueError):
                         print(f"Warning: Could not process drop shelf argument: {self.arguments[0]}")
                         shelf_id = -1 # Or handle error appropriately

                # Only assign if not handled by the "free" case above
                if "shelf_id" not in args:
                    args = {"shelf_id": shelf_id}

        return {"name": self.action, "args": args}

@dataclass
class LLPTask(BaseTask):
    """Low Level Planning task"""

    goal: str = ""
    steps: List[LLPStep] = field(default_factory=list)
    text: str = ""
    task_type: int = -1
    plan_id: int = -1

    def __post_init__(self):
        if self.goal.endswith("."):
            self.goal = self.goal[:-1]

    def __str__(self) -> str:
        return f"{self.goal}"

    def __repr__(self) -> str:
        return str(self)


class LLPDataset(BaseDataset):
    """Low Level Planning dataset"""

    def __init__(
        self,
        logger: WandbLogger,
        path_to_data_dir: Path = Path("."),
        dataset_filename: Optional[str] = None,
        dataset_ext: str = "json",
    ):
        path_to_data_dir = Path(path_to_data_dir)
        self.path_to_dataset = path_to_data_dir / f"{dataset_filename}.{dataset_ext}"
        super().__init__(logger=logger)

        with open(self.path_to_dataset, "r") as f:
            js = json.load(f)
        self._data = js
        self._size = len(self._data)

        if len(self) == 0:
            raise ValueError("No data")

        self.actions = set()
        self.objects = set()
        self.receptacles = set()

        for item in self:
            for step in item.steps:
                self.actions.add(step.action)
                if len(step.arguments) == 2:
                    self.objects.add(step.arguments[0])
                    self.receptacles.add(step.arguments[1])

        self._logger.info(f"Possible actions:     {self.actions}")
        self._logger.info(f"Possible objects:     {self.objects}")
        self._logger.info(f"Possible receptacles: {self.receptacles}")

    def __len__(self):
        return self._size

    def get_data(self):
        pass

    def __getitem__(self, idx) -> LLPTask:
        plan = self._data[idx]
        steps = []
        for step in plan["plan"]:
            steps.append(LLPStep(action=step[0], arguments=step[1][::-1]))

        return LLPTask(
            goal=plan["goal_eng"],
            steps=steps,
            task_type=plan["task_type"],
            plan_id=plan["plan_id"],
        )

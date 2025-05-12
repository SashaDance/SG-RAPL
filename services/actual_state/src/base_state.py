from langchain_core.pydantic_v1 import BaseModel
from services_api import planner, actual_state, assistant
import json

common_world_model = {
    "robot_start_position": [0.0, 0.0, 0.9],
    "robot_start_orientation": [0.0, 0.0, 0.0],
    "waypoints": [
        {"waypoint_id": 0, "name": "Robot start point", "position": [0.0, 0.0, 0.0], "theta": 0.0},
        {"waypoint_id": 1, "name": "In front of shelves 1 and 2", "position": [-1.1, 0.0, 0.0], "theta": 180.0},
        {"waypoint_id": 2, "name": "In front of shelves 3 and 4", "position": [-1.1, 1.0, 0.0], "theta": 180.0},
        {"waypoint_id": 3, "name": "In front of shelf 5", "position": [-1.2, 1.1, 0.0], "theta": 90.0},
        {"waypoint_id": 4, "name": "In front of order delivery table", "position": [0.1, 1.0, 0.0], "theta": 0.0},
    ],
    "shelves": [
        {
            "shelf_id": 1,
            "name": "Shelf 1",
            "position": [-1.7, -0.22, 0.0],
            "orientation_rpy": [0.0, 0.0, 180.0],
            "height": 0.78,
            "aruco_marker_id": 10,
        },
        {
            "shelf_id": 2,
            "name": "Shelf 2",
            "position": [-1.7, 0.22, 0.0],
            "orientation_rpy": [0.0, 0.0, 180.0],
            "height": 0.78,
            "aruco_marker_id": 12,
        },
        {
            "shelf_id": 3,
            "name": "Shelf 3",
            "position": [-1.7, 0.78, 0.0],
            "orientation_rpy": [0.0, 0.0, 180.0],
            "height": 0.78,
            "aruco_marker_id": 12,
        },
        {
            "shelf_id": 4,
            "name": "Shelf 4",
            "position": [-1.7, 1.22, 0.0],
            "orientation_rpy": [0.0, 0.0, 180.0],
            "height": 0.78,
            "aruco_marker_id": 12,
        },
        {
            "shelf_id": 5,
            "name": "Shelf 5",
            "position": [-1.2, 1.72, 0.0],
            "orientation_rpy": [0.0, 0.0, 90.0],
            "height": 0.78,
            "aruco_marker_id": 12,
        },
        {
            "shelf_id": 6,
            "name": "Order delivery table",
            "position": [0.6, 1.0, 0.0],
            "orientation_rpy": [0.0, 0.0, 0.0],
            "height": 0.78,
            "aruco_marker_id": 11,
        },
    ],
    "boxes": [
        {
            "box_id": 313,
            "name": "Box 313",
            "placed_on_shelf_with_id": 6,
            "position": [0.0, 0.0, 0.0],
            "orientation_rpy": [0.0, 0.0, 0.0],
            "aruco_marker_id": 313,
            "color_rgb": [255, 50, 50],
        },
        {
            "box_id": 990,
            "name": "Box 990",
            "placed_on_shelf_with_id": 2,
            "position": [0.0, 0.0, 0.0],
            "orientation_rpy": [0.0, 0.0, 0.0],
            "aruco_marker_id": 990,
            "color_rgb": [255, 50, 50],
        },
        {
            "box_id": 999,
            "name": "Box 999",
            "placed_on_shelf_with_id": 4,
            "position": [0.0, 0.0, 0.0],
            "orientation_rpy": [0.0, 0.0, 0.0],
            "aruco_marker_id": 999,
            "color_rgb": [255, 50, 50],
        },
        {
            "box_id": 998,
            "name": "Box 998",
            "placed_on_shelf_with_id": 5,
            "position": [0.0, 0.0, 0.0],
            "orientation_rpy": [0.0, 0.0, 0.0],
            "aruco_marker_id": 998,
            "color_rgb": [255, 50, 50],
        },
    ],
    "walls": [],
    "localization_markers": [],
}

common_telemetry = {
    "images": [],
    "world_state": {
        "robot_position": [1.0, 1.0, 1.57],
        "boxes": [
            {"box_id": 313, "placed_on_shelf_with_id": 1},
            {"box_id": 990, "placed_on_shelf_with_id": 2},
            {"box_id": 998, "placed_on_shelf_with_id": 4},
            {"box_id": 999, "placed_on_shelf_with_id": 5},
        ],
        "shelves": [
            {"shelf_id": 1, "occupied_by_box_with_id": 313},
            {"shelf_id": 2, "occupied_by_box_with_id": 990},
            {"shelf_id": 3, "occupied_by_box_with_id": -1},
            {"shelf_id": 4, "occupied_by_box_with_id": 998},
            {"shelf_id": 5, "occupied_by_box_with_id": 999},
            {"shelf_id": 6, "occupied_by_box_with_id": -1},
        ],
    },
    "seg_track": [],
    "scene_graph": [
        {
            "id_1": 313,
            "timestamp_1": 17459802,
            "id_2": 990,
            "timestamp_2": 17459802,
            "rel_id": 2,
            "class_name_1": "box",
            "rel_name": "right",
            "class_name_2": "box",
        },
        {
            "id_1": 998,
            "timestamp_1": 17459802,
            "id_2": 999,
            "timestamp_2": 17459802,
            "rel_id": 2,
            "class_name_1": "box",
            "rel_name": "right",
            "class_name_2": "box",
        },
    ],
}

test_telemetry = {
    "images": [],
    # "images": [{"url":"ab66c57a567a576a5c6a763", "src": "webcam"}],
    "world_state": {
        "robot_position": [1.0, 1.0, 1.57],
        "boxes": [
            {"box_id": 313, "placed_on_shelf_with_id": 6},
            {"box_id": 990, "placed_on_shelf_with_id": 2},
            {"box_id": 998, "placed_on_shelf_with_id": 1},
            {"box_id": 999, "placed_on_shelf_with_id": 5},
        ],
        "shelves": [
            {"shelf_id": 1, "occupied_by_box_with_id": 998},
            {"shelf_id": 2, "occupied_by_box_with_id": 990},
            {"shelf_id": 3, "occupied_by_box_with_id": -1},
            {"shelf_id": 4, "occupied_by_box_with_id": -1},
            {"shelf_id": 5, "occupied_by_box_with_id": 999},
            {"shelf_id": 6, "occupied_by_box_with_id": 313},
        ],
    },
    "seg_track": [],
    "scene_graph": [
        {
            "id_1": 998,
            "timestamp_1": 17459802,
            "id_2": 999,
            "timestamp_2": 17459802,
            "rel_id": 2,
            "class_name_1": "box",
            "rel_name": "right",
            "class_name_2": "box",
        },
    ],
}

class ActualState(BaseModel):
    world_model: planner.WorldModel = planner.WorldModel(**common_world_model)
    telemetry: assistant.Telemetry = assistant.Telemetry(**common_telemetry)

    def get(self):
        """Return the current state"""
        response = actual_state.ActualStateResponse(world_model=self.world_model, telemetry=self.telemetry)
        return response.json()

    def update(self, new_state: actual_state.ActualStateRequest):
        """Update the state and return updated state"""
        if isinstance(new_state, str):
            input_state = json.loads(new_state)
        elif isinstance(new_state, dict):
            input_state = new_state
        else:
            raise TypeError("new_state must be a JSON string or dictionary")

        self.world_model = planner.WorldModel(**input_state["world_model"])

        last_plan_state = input_state["plan_history"][-1]

        commands = []
        if "commands" in last_plan_state.keys():
            commands = last_plan_state["commands"]

        #update telemetry from last plan

        self.telemetry = assistant.Telemetry(**last_plan_state["telemetry"])

        #update completed plan actions

        end_idx = len(commands) - 1
        if "error_message" in input_state.keys() and input_state["error_message"]:
            end_idx = last_plan_state["invalid_command_index"]
        if commands:
            for command in commands[:end_idx]:
                if command["name"] == "pick_up":
                    box_id = command["args"]["box_id"]
                    #put -1 for shelf in occupied_by_box
                    for entry in self.telemetry.world_state.shelves:
                        if entry.occupied_by_box_with_id == box_id:
                            entry.occupied_by_box_with_id = -1
                            break

                #put -1 for box in placed_on_shelf
                    for entry in self.telemetry.world_state.boxes:
                        if entry.box_id == box_id:
                            entry.placed_on_shelf_with_id = -1
                            break

                elif command["name"] == "drop": #put shelf_id for given box
                    shelf_id = command["args"]["shelf_id"]
                    box_id = 0

                #find box_id of held box and put shelf_id for box in placed_on_shelf
                    for entry in self.telemetry.world_state.boxes:
                        if entry.placed_on_shelf_with_id == -1:
                            entry.placed_on_shelf_with_id = shelf_id
                            box_id = entry.box_id
                            break

                #put shelf_id for shelf in occupied_by_box
                    for entry in self.telemetry.world_state.shelves:
                        if entry.shelf_id == shelf_id:
                            entry.occupied_by_box_with_id = box_id
                            break

        #update worldmodel according to telemetry
        box_shelf_pairs = {}
        for entry in self.telemetry.world_state.boxes:
                box_shelf_pairs[entry.box_id] = entry.placed_on_shelf_with_id
        for entry in self.world_model.boxes:
                entry.placed_on_shelf_with_id = box_shelf_pairs[entry.box_id]

        
        response = actual_state.ActualStateResponse(world_model=self.world_model, telemetry=self.telemetry)
        return response.json()


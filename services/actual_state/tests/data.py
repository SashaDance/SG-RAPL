from services_api import actual_state, planner
from pydantic.v1 import BaseModel

class TestCase(BaseModel):
    name: str
    request: actual_state.ActualStateRequest
    response: actual_state.ActualStateResponse
    response_comparator: object = lambda checked_response, target_response: checked_response == target_response

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
            "placed_on_shelf_with_id": 1,
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
            "placed_on_shelf_with_id": 5,
            "position": [0.0, 0.0, 0.0],
            "orientation_rpy": [0.0, 0.0, 0.0],
            "aruco_marker_id": 999,
            "color_rgb": [255, 50, 50],
        },
        {
            "box_id": 998,
            "name": "Box 998",
            "placed_on_shelf_with_id": 4,
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

common_get_world_model =  {
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
common_get_telemetry = {
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

test_case_3_telemetry = {
    "images": [],
    "world_state": {
        "robot_position": [1.0, 1.0, 1.57],
        "boxes": [
            {"box_id": 313, "placed_on_shelf_with_id": 6},
            {"box_id": 990, "placed_on_shelf_with_id": 2},
            {"box_id": 998, "placed_on_shelf_with_id": 4},
            {"box_id": 999, "placed_on_shelf_with_id": 5},
        ],
        "shelves": [
            {"shelf_id": 1, "occupied_by_box_with_id": -1},
            {"shelf_id": 2, "occupied_by_box_with_id": 990},
            {"shelf_id": 3, "occupied_by_box_with_id": -1},
            {"shelf_id": 4, "occupied_by_box_with_id": 998},
            {"shelf_id": 5, "occupied_by_box_with_id": 999},
            {"shelf_id": 6, "occupied_by_box_with_id": 313},
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
test_case_3_world_model = {
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
            "placed_on_shelf_with_id": 5,
            "position": [0.0, 0.0, 0.0],
            "orientation_rpy": [0.0, 0.0, 0.0],
            "aruco_marker_id": 999,
            "color_rgb": [255, 50, 50],
        },
        {
            "box_id": 998,
            "name": "Box 998",
            "placed_on_shelf_with_id": 4,
            "position": [0.0, 0.0, 0.0],
            "orientation_rpy": [0.0, 0.0, 0.0],
            "aruco_marker_id": 998,
            "color_rgb": [255, 50, 50],
        },
    ],
    "walls": [],
    "localization_markers": [],
}

test_case_4_telemetry = {
    "images": [],
    "world_state": {
        "robot_position": [1.0, 1.0, 1.57],
        "boxes": [
            {"box_id": 313, "placed_on_shelf_with_id": -1},
            {"box_id": 990, "placed_on_shelf_with_id": 2},
            {"box_id": 998, "placed_on_shelf_with_id": 4},
            {"box_id": 999, "placed_on_shelf_with_id": 5},
        ],
        "shelves": [
            {"shelf_id": 1, "occupied_by_box_with_id": -1},
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
test_case_4_world_model = {
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
            "placed_on_shelf_with_id": -1,
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
            "placed_on_shelf_with_id": 5,
            "position": [0.0, 0.0, 0.0],
            "orientation_rpy": [0.0, 0.0, 0.0],
            "aruco_marker_id": 999,
            "color_rgb": [255, 50, 50],
        },
        {
            "box_id": 998,
            "name": "Box 998",
            "placed_on_shelf_with_id": 4,
            "position": [0.0, 0.0, 0.0],
            "orientation_rpy": [0.0, 0.0, 0.0],
            "aruco_marker_id": 998,
            "color_rgb": [255, 50, 50],
        },
    ],
    "walls": [],
    "localization_markers": [],
}


test_cases = [
    TestCase(
        name="1. get initial data",
        request=actual_state.ActualStateRequest(
            task="get",
            error_message="",
            world_model=planner.WorldModel(**common_get_world_model),
            plan_history=[
                planner.RequestRetry(
                    telemetry=planner.Telemetry(**common_get_telemetry),
                )
            ],
        ),
        response=actual_state.ActualStateResponse(
            world_model=planner.WorldModel(**common_get_world_model), 
            telemetry=planner.Telemetry(**common_get_telemetry),
        ),

    ),
    TestCase(
        name="2. update initial data(no errors, no plan)",
        request=actual_state.ActualStateRequest(
            task="update",
            error_message="",
            world_model=planner.WorldModel(**common_world_model),
            plan_history=[
                planner.RequestRetry(
                    telemetry=planner.Telemetry(**common_telemetry),
                )
            ],
        ),
        response=actual_state.ActualStateResponse(
            world_model=planner.WorldModel(**common_world_model), 
            telemetry=planner.Telemetry(**common_telemetry),
        ),
    ),
        TestCase(
        name="3. update initial data(no errors, full plan completed)",
        request=actual_state.ActualStateRequest(
            task="update",
            error_message="",
            world_model=planner.WorldModel(**common_world_model),
            plan_history=[
                planner.RequestRetry(
                    telemetry=planner.Telemetry(**common_telemetry),
                    commands=[
                        planner.Action(name="say", args={"text": "walking up to box 313"}),
                        planner.Action(name="go_to", args={"waypoint_id": 1}),
                        planner.Action(name="say", args={"text": "taking box 313"}),
                        planner.Action(name="pick_up", args={"box_id": 313}),
                        planner.Action(name="say", args={"text": "walking up to order delivery table"}),
                        planner.Action(name="go_to", args={"waypoint_id": 4}),
                        planner.Action(name="say", args={"text": "putting box 313"}),
                        planner.Action(name="drop", args={"shelf_id": 6}),
                        planner.Action(name="say", args={"text": "walking up to waypoint 0"}),
                        planner.Action(name="go_to", args={"waypoint_id": 0}),
                    ]
                )
            ],
        ),
        response=actual_state.ActualStateResponse(
            world_model=planner.WorldModel(**test_case_3_world_model), 
            telemetry=planner.Telemetry(**test_case_3_telemetry),
        ),
    ),
        TestCase(
        name="4. update initial data(error, plan partially completed)",
        request=actual_state.ActualStateRequest(
            task="update",
            error_message="error",
            world_model=planner.WorldModel(**common_world_model),
            plan_history=[
                planner.RequestRetry(
                    telemetry=planner.Telemetry(**common_telemetry),
                    commands=[
                        planner.Action(name="say", args={"text": "walking up to box 313"}),
                        planner.Action(name="go_to", args={"waypoint_id": 1}),
                        planner.Action(name="say", args={"text": "taking box 313"}),
                        planner.Action(name="pick_up", args={"box_id": 313}),
                        planner.Action(name="say", args={"text": "walking up to order delivery table"}),
                        planner.Action(name="go_to", args={"waypoint_id": 4}),
                        planner.Action(name="say", args={"text": "putting box 313"}),
                        planner.Action(name="drop", args={"shelf_id": 6}),
                        planner.Action(name="say", args={"text": "walking up to waypoint 0"}),
                        planner.Action(name="go_to", args={"waypoint_id": 0}),
                    ],
                    invalid_command_index = 7,
                )
            ],
        ),
        response=actual_state.ActualStateResponse(
            world_model=planner.WorldModel(**test_case_4_world_model), 
            telemetry=planner.Telemetry(**test_case_4_telemetry),
        ),
    )
]


test_cases = {test_case.name: test_case for test_case in test_cases}

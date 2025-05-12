from services_api import planner
from pydantic.v1 import BaseModel


class TestCase(BaseModel):
    name: str
    request: planner.PlannerRequest
    response: planner.PlannerResponse
    response_comparator: object = lambda checked_response, target_response: checked_response == target_response


loader_world_model = {
    "robot_start_position": [0.0, 0.0, 0.9],
    "robot_start_orientation": [0.0, 0.0, 0.0],
    "waypoints": [
        {"waypoint_id": 0, "name": "Robot start point", "position": [0.0, 0.0, 0.0], "theta": 0.0},
        {"waypoint_id": 1, "name": "In front of shelves 1 and 2", "position": [-1.1, 0.0, 0.0], "theta": 180.0},
        {"waypoint_id": 2, "name": "In front of shelves 3 and 4", "position": [-1.1, 1.0, 0.0], "theta": 180.0},
        {"waypoint_id": 3, "name": "In front of shelf 5", "position": [-1.2, 1.1, 0.0], "theta": 90.0},
        {"waypoint_id": 4, "name": "In front of order delivery table", "position": [0.1, 1.0, 0.0], "theta": 0.0},
        {"waypoint_id": 5, "name": "In front of loader", "position": [0.1, 1.0, 0.0], "theta": 0.0},
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
        {
            "shelf_id": 7,
            "name": "Loader",
            "position": [0.6, 1.0, 0.0],
            "orientation_rpy": [0.0, 0.0, 0.0],
            "height": 0.78,
            "aruco_marker_id": 13,
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

loader_313_telemetry_v2 = {
    "images": [],
    "world_state": {
        "robot_position": [1.0, 1.0, 1.57],
        "boxes": [
            {"box_id": 313, "placed_on_shelf_with_id": 6},
        ],
        "shelves": [
            {"shelf_id": 1, "occupied_by_box_with_id": -1},
            {"shelf_id": 2, "occupied_by_box_with_id": -1},
            {"shelf_id": 3, "occupied_by_box_with_id": -1},
            {"shelf_id": 4, "occupied_by_box_with_id": -1},
            {"shelf_id": 5, "occupied_by_box_with_id": -1},
            {"shelf_id": 6, "occupied_by_box_with_id": 313},
            {"shelf_id": 7, "occupied_by_box_with_id": -1},
        ],
    },
    "seg_track": [],
    "scene_graph": [],
}


loader_313_telemetry = {
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
            {"shelf_id": 7, "occupied_by_box_with_id": -1},
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

delivery_order_313_telemetry = {
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

return_313_box_telemetry = {
    "images": [],
    # "images": [{"url":"ab66c57a567a576a5c6a763", "src": "webcam"}],
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

take_998_box_telemetry = {
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


loader_return_313_box_telemetry = {
    "images": [],
    # "images": [{"url":"ab66c57a567a576a5c6a763", "src": "webcam"}],
    "world_state": {
        "robot_position": [1.0, 1.0, 1.57],
        "boxes": [
            {"box_id": 313, "placed_on_shelf_with_id": 7},
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
            {"shelf_id": 7, "occupied_by_box_with_id": 313},
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
loader_313_telemetry_v2


loader_no_drop_telemetry = {
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
test_cases = [
    # delivery_order_313_to_loader_v2
    TestCase(
        name="delivery_order_313_to_loader_no_drop",
        request=planner.PlannerRequest(
            goal="go to order delivery table",
            telemetry=planner.Telemetry(**loader_no_drop_telemetry),
            world_model=planner.WorldModel(**loader_world_model),
            retries=[],
            max_retries=5,
        ),
        response=planner.PlannerResponse(
            plan=[
                planner.Action(name="say", args={"text": "walking up to order delivery table"}),
                planner.Action(name="go_to", args={"waypoint_id": 4}),
                planner.Action(name="say", args={"text": "putting box 313"}),
                planner.Action(name="drop", args={"shelf_id": 6}),
                planner.Action(name="say", args={"text": "walking up to waypoint 0"}),
                planner.Action(name="go_to", args={"waypoint_id": 0}),
            ]
        ),
    ),
    TestCase(
        name="delivery_order_313_to_loader_v2",
        request=planner.PlannerRequest(
            goal="bring box 313 to loader",
            telemetry=planner.Telemetry(**loader_313_telemetry_v2),
            world_model=planner.WorldModel(**loader_world_model),
            retries=[],
            max_retries=5,
        ),
        response=planner.PlannerResponse(
            plan=[
                planner.Action(name="say", args={"text": "walking up to box 313"}),
                planner.Action(name="go_to", args={"waypoint_id": 4}),
                planner.Action(name="say", args={"text": "taking box 313"}),
                planner.Action(name="pick_up", args={"box_id": 313}),
                planner.Action(name="say", args={"text": "walking up to loader"}),
                planner.Action(name="go_to", args={"waypoint_id": 5}),
                planner.Action(name="say", args={"text": "putting box 313"}),
                planner.Action(name="drop", args={"shelf_id": 7}),
                planner.Action(name="say", args={"text": "walking up to waypoint 0"}),
                planner.Action(name="go_to", args={"waypoint_id": 0}),
            ]
        ),
    ),
    # # delivery_order_313_to_loader_v3
    # TestCase(
    #     name="delivery_order_313_to_loader_v3",
    #     request=planner.PlannerRequest(
    #         goal="bring box 313 to loader, and go back to order delivery table",
    #         telemetry=planner.Telemetry(**loader_313_telemetry_v2),
    #         world_model=planner.WorldModel(**loader_world_model),
    #         retries=[],
    #         max_retries=5,
    #     ),
    #     response=planner.PlannerResponse(
    #         plan=[
    #             planner.Action(name="say", args={"text": "walking up to box 313"}),
    #             planner.Action(name="go_to", args={"waypoint_id": 4}),
    #             planner.Action(name="say", args={"text": "taking box 313"}),
    #             planner.Action(name="pick_up", args={"box_id": 313}),
    #             planner.Action(name="say", args={"text": "walking up to loader"}),
    #             planner.Action(name="go_to", args={"waypoint_id": 5}),
    #             planner.Action(name="say", args={"text": "putting box 313"}),
    #             planner.Action(name="drop", args={"shelf_id": 7}),
    #             planner.Action(name="say", args={"text": "walking up to waypoint 4"}),
    #             planner.Action(name="go_to", args={"waypoint_id": 4}),
    #         ]
    #     ),
    # ),
    TestCase(
        name="delivery_order_313_to_loader",
        request=planner.PlannerRequest(
            goal="bring box 313 to loader",
            telemetry=planner.Telemetry(**loader_313_telemetry),
            world_model=planner.WorldModel(**loader_world_model),
            retries=[],
            max_retries=5,
        ),
        response=planner.PlannerResponse(
            plan=[
                planner.Action(name="say", args={"text": "walking up to box 313"}),
                planner.Action(name="go_to", args={"waypoint_id": 1}),
                planner.Action(name="say", args={"text": "taking box 313"}),
                planner.Action(name="pick_up", args={"box_id": 313}),
                planner.Action(name="say", args={"text": "walking up to loader"}),
                planner.Action(name="go_to", args={"waypoint_id": 5}),
                planner.Action(name="say", args={"text": "putting box 313"}),
                planner.Action(name="drop", args={"shelf_id": 7}),
                planner.Action(name="say", args={"text": "walking up to waypoint 0"}),
                planner.Action(name="go_to", args={"waypoint_id": 0}),
            ]
        ),
    ),
    # return 313 from loader to free shelf
    TestCase(
        name="return_box_313_from_loader",
        request=planner.PlannerRequest(
            goal="return box 313 to a free shelf",
            telemetry=planner.Telemetry(**loader_return_313_box_telemetry),
            world_model=planner.WorldModel(**loader_world_model),
            retries=[],
            max_retries=5,
        ),
        response=planner.PlannerResponse(
            plan=[
                planner.Action(name="say", args={"text": "walking up to box 313"}),
                planner.Action(name="go_to", args={"waypoint_id": 5}),
                planner.Action(name="say", args={"text": "taking box 313"}),
                planner.Action(name="pick_up", args={"box_id": 313}),
                planner.Action(name="say", args={"text": "walking up to free shelf"}),
                planner.Action(name="go_to", args={"waypoint_id": 1}),
                planner.Action(name="say", args={"text": "putting box 313"}),
                planner.Action(name="drop", args={"shelf_id": 1}),
                planner.Action(name="say", args={"text": "walking up to waypoint 0"}),
                planner.Action(name="go_to", args={"waypoint_id": 0}),
            ]
        ),
    ),
    # delivery_order_313
    TestCase(
        name="delivery_order_313",
        request=planner.PlannerRequest(
            goal="bring box 313 to order delivery table",
            telemetry=planner.Telemetry(**delivery_order_313_telemetry),
            world_model=planner.WorldModel(**common_world_model),
            retries=[],
            max_retries=5,
        ),
        response=planner.PlannerResponse(
            plan=[
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
        ),
    ),
    # # delivery_order_313
    # TestCase(
    #     name="delivery_order_313",
    #     request=planner.PlannerRequest(
    #         goal="bring box 313 to order delivery table and stay there",
    #         telemetry=planner.Telemetry(**delivery_order_313_telemetry),
    #         world_model=planner.WorldModel(**common_world_model),
    #         retries=[],
    #         max_retries=5,
    #     ),
    #     response=planner.PlannerResponse(
    #         plan=[
    #             planner.Action(name="say", args={"text": "walking up to box 313"}),
    #             planner.Action(name="go_to", args={"waypoint_id": 1}),
    #             planner.Action(name="say", args={"text": "taking box 313"}),
    #             planner.Action(name="pick_up", args={"box_id": 313}),
    #             planner.Action(name="say", args={"text": "walking up to order delivery table"}),
    #             planner.Action(name="go_to", args={"waypoint_id": 4}),
    #             planner.Action(name="say", args={"text": "putting box 313"}),
    #             planner.Action(name="drop", args={"shelf_id": 6}),
    #         ]
    #     ),
    # ),
    # return_box_313
    TestCase(
        name="return_box_313",
        request=planner.PlannerRequest(
            goal="return box 313 to a free shelf",
            telemetry=planner.Telemetry(**return_313_box_telemetry),
            world_model=planner.WorldModel(**common_world_model),
            retries=[],
            max_retries=5,
        ),
        response=planner.PlannerResponse(
            plan=[
                planner.Action(name="say", args={"text": "walking up to box 313"}),
                planner.Action(name="go_to", args={"waypoint_id": 4}),
                planner.Action(name="say", args={"text": "taking box 313"}),
                planner.Action(name="pick_up", args={"box_id": 313}),
                planner.Action(name="say", args={"text": "walking up to free shelf"}),
                planner.Action(name="go_to", args={"waypoint_id": 1}),
                planner.Action(name="say", args={"text": "putting box 313"}),
                planner.Action(name="drop", args={"shelf_id": 1}),
                planner.Action(name="say", args={"text": "walking up to waypoint 0"}),
                planner.Action(name="go_to", args={"waypoint_id": 0}),
            ]
        ),
    ),
    TestCase(
        name="10. put box on table(unspecified)",
        request=planner.PlannerRequest(
            goal="put box on order delivery table",
            telemetry=planner.Telemetry(**delivery_order_313_telemetry),
            world_model=planner.WorldModel(**common_world_model),
            retries=[],
            max_retries=5,
        ),
        response=planner.PlannerResponse(
            plan=[
                planner.Action(name="say", args={"text": "walking up to order delivery table"}),
                planner.Action(name="go_to", args={"waypoint_id": 4}),
                planner.Action(name="say", args={"text": "putting box"}),
                planner.Action(name="drop", args={"shelf_id": 6}),
                planner.Action(name="say", args={"text": "walking up to waypoint 0"}),
                planner.Action(name="go_to", args={"waypoint_id": 0}),
            ]
        ),
    ),
    TestCase(
        name="11. take box from shelf 3 and put on order delivery table(replanning, correct waypoint: 1)",
        request=planner.PlannerRequest(
            goal="take box 998 from shelf 3 and put on order delivery table",
            telemetry=planner.Telemetry(**take_998_box_telemetry),
            world_model=planner.WorldModel(**common_world_model),
            retries=[
                planner.RequestRetry(
                    goal="take box 313 from shelf 3 and put on order delivery table",
                    commands=[
                        planner.Action(name="say", args={"text": "walking up to shelf 3"}),
                        planner.Action(name="go_to", args={"waypoint_id": 2}),
                        planner.Action(name="say", args={"text": "taking box 313"}),
                        planner.Action(name="pick_up", args={"box_id": 313}),
                        planner.Action(name="say", args={"text": "walking up to order delivery table"}),
                        planner.Action(name="go_to", args={"waypoint_id": 4}),
                        planner.Action(name="say", args={"text": "putting box 313"}),
                        planner.Action(name="drop", args={"shelf_id": 6}),
                        planner.Action(name="say", args={"text": "walking up to waypoint 0"}),
                        planner.Action(name="go_to", args={"waypoint_id": 0}),
                    ],
                    invalid_command_index=3,
                    error_code="",
                )
            ],
            max_retries=5,
        ),
        response=planner.PlannerResponse(
            plan=[
                planner.Action(name="say", args={"text": "walking up to waypoint 1"}),
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
        ),
    ),
    TestCase(
        name="12. take box from shelf 3 and put on order delivery table(replanning, correct waypoint: 3)",
        request=planner.PlannerRequest(
            goal="take box 313 from shelf 3 and put on order delivery table",
            telemetry=planner.Telemetry(**take_998_box_telemetry),
            world_model=planner.WorldModel(**common_world_model),
            retries=[
                planner.RequestRetry(
                    goal="take box 313 from shelf 3 and put on order delivery table",
                    commands=[
                        planner.Action(name="say", args={"text": "walking up to shelf 3"}),
                        planner.Action(name="go_to", args={"waypoint_id": 2}),
                        planner.Action(name="say", args={"text": "taking box 313"}),
                        planner.Action(name="pick_up", args={"box_id": 313}),
                        planner.Action(name="say", args={"text": "walking up to order delivery table"}),
                        planner.Action(name="go_to", args={"waypoint_id": 4}),
                        planner.Action(name="say", args={"text": "putting box 313"}),
                        planner.Action(name="drop", args={"shelf_id": 6}),
                        planner.Action(name="say", args={"text": "walking up to waypoint 0"}),
                        planner.Action(name="go_to", args={"waypoint_id": 0}),
                    ],
                    invalid_command_index=3,
                    error_code="",
                ),
                planner.RequestRetry(
                    goal="take box 313 from shelf 3 and put on order delivery table",
                    commands=[
                        planner.Action(name="say", args={"text": "walking up to waypoint 1"}),
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
                    invalid_command_index=3,
                    error_code="",
                ),
            ],
            max_retries=5,
        ),
        response=planner.PlannerResponse(
            plan=[
                planner.Action(name="say", args={"text": "walking up to waypoint 3"}),
                planner.Action(name="go_to", args={"waypoint_id": 3}),
                planner.Action(name="say", args={"text": "taking box 313"}),
                planner.Action(name="pick_up", args={"box_id": 313}),
                planner.Action(name="say", args={"text": "walking up to order delivery table"}),
                planner.Action(name="go_to", args={"waypoint_id": 4}),
                planner.Action(name="say", args={"text": "putting box 313"}),
                planner.Action(name="drop", args={"shelf_id": 6}),
                planner.Action(name="say", args={"text": "walking up to waypoint 0"}),
                planner.Action(name="go_to", args={"waypoint_id": 0}),
            ]
        ),
    ),
    TestCase(
        name="13. take box from shelf 3 and put on order delivery table(replanning, no availible plan)",
        request=planner.PlannerRequest(
            goal="take box 313 from shelf 3 and put on order delivery table",
            telemetry=planner.Telemetry(**return_313_box_telemetry),
            world_model=planner.WorldModel(**common_world_model),
            retries=[
                planner.RequestRetry(
                    goal="take box 313 from shelf 3 and put on order delivery table",
                    commands=[
                        planner.Action(name="say", args={"text": "walking up to shelf 3"}),
                        planner.Action(name="go_to", args={"waypoint_id": 2}),
                        planner.Action(name="say", args={"text": "taking box 313"}),
                        planner.Action(name="pick_up", args={"box_id": 313}),
                        planner.Action(name="say", args={"text": "walking up to order delivery table"}),
                        planner.Action(name="go_to", args={"waypoint_id": 4}),
                        planner.Action(name="say", args={"text": "putting box 313"}),
                        planner.Action(name="drop", args={"shelf_id": 6}),
                        planner.Action(name="say", args={"text": "walking up to waypoint 0"}),
                        planner.Action(name="go_to", args={"waypoint_id": 0}),
                    ],
                    invalid_command_index=3,
                    error_code="",
                ),
                planner.RequestRetry(
                    goal="take box 313 from shelf 3 and put on order delivery table",
                    commands=[
                        planner.Action(name="say", args={"text": "walking up to waypoint 1"}),
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
                    invalid_command_index=3,
                    error_code="",
                ),
                planner.RequestRetry(
                    goal="take box 313 from shelf 3 and put on order delivery table",
                    commands=[
                        planner.Action(name="say", args={"text": "walking up to waypoint 3"}),
                        planner.Action(name="go_to", args={"waypoint_id": 3}),
                        planner.Action(name="say", args={"text": "taking box 313"}),
                        planner.Action(name="pick_up", args={"box_id": 313}),
                        planner.Action(name="say", args={"text": "walking up to order delivery table"}),
                        planner.Action(name="go_to", args={"waypoint_id": 4}),
                        planner.Action(name="say", args={"text": "putting box 313"}),
                        planner.Action(name="drop", args={"shelf_id": 6}),
                        planner.Action(name="say", args={"text": "walking up to waypoint 0"}),
                        planner.Action(name="go_to", args={"waypoint_id": 0}),
                    ],
                    invalid_command_index=3,
                    error_code="",
                ),
                planner.RequestRetry(
                    goal="take box 313 from shelf 3 and put on order delivery table",
                    commands=[
                        planner.Action(name="say", args={"text": "walking up to waypoint 4"}),
                        planner.Action(name="go_to", args={"waypoint_id": 4}),
                        planner.Action(name="say", args={"text": "taking box 313"}),
                        planner.Action(name="pick_up", args={"box_id": 313}),
                        planner.Action(name="say", args={"text": "walking up to order delivery table"}),
                        planner.Action(name="go_to", args={"waypoint_id": 4}),
                        planner.Action(name="say", args={"text": "putting box 313"}),
                        planner.Action(name="drop", args={"shelf_id": 6}),
                        planner.Action(name="say", args={"text": "walking up to waypoint 0"}),
                        planner.Action(name="go_to", args={"waypoint_id": 0}),
                    ],
                    invalid_command_index=3,
                    error_code="",
                ),
            ],
            max_retries=5,
        ),
        response=planner.PlannerResponse(plan=[]),
    ),
    TestCase(
        name="14. take box from shelf 3 and put on order delivery table(replanning, replan limit exceeded)",
        request=planner.PlannerRequest(
            goal="take box 313 from shelf 3 and put on order delivery table",
            telemetry=planner.Telemetry(**return_313_box_telemetry),
            world_model=planner.WorldModel(**common_world_model),
            retries=[
                planner.RequestRetry(
                    goal="take box 313 from shelf 3 and put on order delivery table",
                    commands=[
                        planner.Action(name="say", args={"text": "walking up to shelf 3"}),
                        planner.Action(name="go_to", args={"waypoint_id": 2}),
                        planner.Action(name="say", args={"text": "taking box 313"}),
                        planner.Action(name="pick_up", args={"box_id": 313}),
                        planner.Action(name="say", args={"text": "walking up to order delivery table"}),
                        planner.Action(name="go_to", args={"waypoint_id": 4}),
                        planner.Action(name="say", args={"text": "putting box 313"}),
                        planner.Action(name="drop", args={"shelf_id": 6}),
                        planner.Action(name="say", args={"text": "walking up to waypoint 0"}),
                        planner.Action(name="go_to", args={"waypoint_id": 0}),
                    ],
                    invalid_command_index=3,
                    error_code="",
                ),
                planner.RequestRetry(
                    goal="take box 313 from shelf 3 and put on order delivery table",
                    commands=[
                        planner.Action(name="say", args={"text": "walking up to waypoint 1"}),
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
                    invalid_command_index=3,
                    error_code="",
                ),
                planner.RequestRetry(
                    goal="take box 313 from shelf 3 and put on order delivery table",
                    commands=[
                        planner.Action(name="say", args={"text": "walking up to waypoint 3"}),
                        planner.Action(name="go_to", args={"waypoint_id": 3}),
                        planner.Action(name="say", args={"text": "taking box 313"}),
                        planner.Action(name="pick_up", args={"box_id": 313}),
                        planner.Action(name="say", args={"text": "walking up to order delivery table"}),
                        planner.Action(name="go_to", args={"waypoint_id": 4}),
                        planner.Action(name="say", args={"text": "putting box 313"}),
                        planner.Action(name="drop", args={"shelf_id": 6}),
                        planner.Action(name="say", args={"text": "walking up to waypoint 0"}),
                        planner.Action(name="go_to", args={"waypoint_id": 0}),
                    ],
                    invalid_command_index=3,
                    error_code="",
                ),
                planner.RequestRetry(
                    goal="take box 313 from shelf 3 and put on order delivery table",
                    commands=[
                        planner.Action(name="say", args={"text": "walking up to waypoint 4"}),
                        planner.Action(name="go_to", args={"waypoint_id": 4}),
                        planner.Action(name="say", args={"text": "taking box 313"}),
                        planner.Action(name="pick_up", args={"box_id": 313}),
                        planner.Action(name="say", args={"text": "walking up to order delivery table"}),
                        planner.Action(name="go_to", args={"waypoint_id": 4}),
                        planner.Action(name="say", args={"text": "putting box 313"}),
                        planner.Action(name="drop", args={"shelf_id": 6}),
                        planner.Action(name="say", args={"text": "walking up to waypoint 0"}),
                        planner.Action(name="go_to", args={"waypoint_id": 0}),
                    ],
                    invalid_command_index=3,
                    error_code="",
                ),
            ],
            max_retries=3,
        ),
        response=planner.PlannerResponse(plan=[]),
    ),
]

test_cases = {test_case.name: test_case for test_case in test_cases}

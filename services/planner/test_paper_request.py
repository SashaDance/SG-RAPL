from services_api import planner
import pytest
from tests.data import TestCase
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


common_telemetries_1 = [
        {
        "images": [],
        "world_state": {
            "robot_position": [1.0, 1.0, 1.57],
            "boxes": [
                {"box_id": 313, "placed_on_shelf_with_id": step[0]},
                {"box_id": 990, "placed_on_shelf_with_id": step[1]},
                {"box_id": 998, "placed_on_shelf_with_id": step[2]},
                {"box_id": 999, "placed_on_shelf_with_id": step[3]},
                {"box_id": 215, "placed_on_shelf_with_id": step[4]}
            ],
            "shelves": [
                {"shelf_id": 1, "occupied_by_box_with_id": step[5]},
                {"shelf_id": 2, "occupied_by_box_with_id": step[6]},
                {"shelf_id": 3, "occupied_by_box_with_id": step[7]},
                {"shelf_id": 4, "occupied_by_box_with_id": step[8]},
                {"shelf_id": 5, "occupied_by_box_with_id": step[9]},
                {"shelf_id": 6, "occupied_by_box_with_id": step[10]},
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

    for i, step in enumerate(
        [
            (0, 0, 0, 0, 1, #Take box 215 from shelf 1 and put it on order delivery table.
            215, 0, 0, 0, 0, -1), 

            (0, 0, 5, 0, 0, #Take box 998 from shelf 5 and put it on shelf 3.
            0, 0, -1, 0, 998, 0), 

            (2, 0, 0, 0, 0, #"Bring box 313 from shelf 2 to order delivery table.",
            0, 313, 0, 0, 998, 0),

            (0, 0, 0, 1, 0, #"Return box 999 from shelf 1 to a free shelf.",
            999, 0, -1, 0, 0, 0),

            (0, 0, 0, 0, 4, #Take box 215 from shelf 4 and put it on shelf 1
            -1, 0, 0, 215, 0, 0 ), 

            (0, 0, 0, 4, 0, #"Move box 999 from shelf 4 to a free shelf.",
            0, 0, -1, 999, 0, 0),
            
            (0, 5, 0, 0, 0, #"Take box 990 from shelf 5 and put it on order delivery table."
            0, 0, 0, 0, 0, -1),

            (0, 0, 2, 0, 0, #Take box 998 from shelf 2 and put it on order delivery table.
            0, 998, 0, 0, 0, -1),

            (0, 0, 0, 0, 6, #"Return box 215 from order delivery table to a free shelf."
            0, 0, -1, 0, 0, 215),

            (1, 0, 0, 0, 0, #Bring box 313 from shelf 1 to order delivery table.
            313, 0, 0, 0, 0, -1),

            (0, 0, 0, 0, 3, #Take box 215 from shelf 3 and put it on shelf 5
            0, 0, 215, 0, 0, -1),

            (0, 2, 0, 0, 0, #Take box 990 from shelf 2 and put it on order delivery table.
            0, 990, 0, 0, 0, -1),

            (0, 0, 6, 0, 0,  #Move box 998 from order delivery table to a free shelf.
            0, 0, -1, 0, 0, 998),

            (0, 0, 0, 2, 0, #Take box 999 from shelf 2 and put it on order delivery table.
            0, 999, 0, 0, 0, -1),

            (0, 0, 0, 3, 0, #Return box 999 from shelf 2 to a free shelf.
            0, 999, -1, 0, 0, 0),

            (0, 0, 0, 6, 0,  #Move box 999 from order delivery table to shelf 4.
            0, 0, 0, -1, 0, 999),

            (0, 0, 3, 0, 0, #Take box 998 from shelf 3 and put it on order delivery table.
            0, 0, 998, 0, 0, -1),

            (5, 0, 0, 0, 0, #Take box 313 from shelf 5 and put it on shelf 1.
            -1, 0, 0, 0, 313, 0),

            (0, 0, 0, 0, 6, #Move box 215 from order delivery table to shelf 1.
            -1, 0, 0, 0, 0, 215)
        ]
    )
]

common_telemetries_2 = [
        {
        "images": [],
        "world_state": {
            "robot_position": [1.0, 1.0, 1.57],
            "boxes": [
                {"box_id": 313, "placed_on_shelf_with_id": step[0]},
                {"box_id": 990, "placed_on_shelf_with_id": step[1]},
                {"box_id": 998, "placed_on_shelf_with_id": step[2]},
                {"box_id": 999, "placed_on_shelf_with_id": step[3]},
                {"box_id": 215, "placed_on_shelf_with_id": step[4]}
            ],
            "shelves": [
                {"shelf_id": 1, "occupied_by_box_with_id": step[5]},
                {"shelf_id": 2, "occupied_by_box_with_id": step[6]},
                {"shelf_id": 3, "occupied_by_box_with_id": step[7]},
                {"shelf_id": 4, "occupied_by_box_with_id": step[8]},
                {"shelf_id": 5, "occupied_by_box_with_id": step[9]},
                {"shelf_id": 6, "occupied_by_box_with_id": step[10]},
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

    for i, step in enumerate(
        [
            (5, 0, 0, 0, 1, #"Take box 215 from shelf 1 and put it on order delivery table, then take box 313 from shelf 5 and put it on shelf 3.",
            215, 0, -1, 0, 313, -1),

            (0, 0, 1, 2, 0, #"Bring box 999 from shelf 2 to order delivery table, then return box 998 from shelf 1 to a free shelf.",
            998, 999, -1, 0, 0, -1),

            (2, 4, 0, 0, 0, #"Take box 990 from shelf 4 and put it on shelf 1, then take box 313 from shelf 2 and move it to shelf 4."
            -1, 313, 0, 990, -1, 0),

            (0, 4, 0, 5, 0, #"Move box 990 from shelf 4 to a free shelf, then take box 999 from shelf 5 and put it on order delivery table."
            0, 0, -1, 990, 999, -1),

            (2, 0, 0, 0, 0, #"Take box 313 from shelf 2 and put it on order delivery table, then return box 990 from order delivery table to a free shelf."
            0, 313, -1, 0, 0, 990),

            (3, 0, 1, 0, 0, #"Bring box 998 from shelf 1 to order delivery table, then take box 313 from shelf 3 and put it on shelf 5."
            998, 0, 313, 0, -1, -1),

            (0, 0, 2, 0, 0, #"Take box 998 from shelf 2 and put it on order delivery table, then move box 999 from order delivery table to a free shelf."
            0, 998, -1, 0, 0, 999),

            (0, 0, 0, 2, 2, #"Take box 999 from shelf 2 and put it on order delivery table, then return box 215 from shelf 2 to a free shelf."
            0, 999, -1, 0, 0, -1),

            (0, 0, 0, 6, 3, #"Move box 999 from order delivery table to shelf 4, then take box 215 from shelf 3 and put it on order delivery table."
            0, 0, 0, -1, 0, 999),

            (5, 6, 0, 0, 0, #"Take box 313 from shelf 5 and put it on order delivery table, then move box 990 from order delivery table to shelf 1."
            -1, 0, 0, 0, 313, 990),
        ]
    )
]

common_telemetries_3 = [
        {
        "images": [],
        "world_state": {
            "robot_position": [1.0, 1.0, 1.57],
            "boxes": [
                {"box_id": 313, "placed_on_shelf_with_id": step[0]},
                {"box_id": 990, "placed_on_shelf_with_id": step[1]},
                {"box_id": 998, "placed_on_shelf_with_id": step[2]},
                {"box_id": 999, "placed_on_shelf_with_id": step[3]},
                {"box_id": 215, "placed_on_shelf_with_id": step[4]}
            ],
            "shelves": [
                {"shelf_id": 1, "occupied_by_box_with_id": step[5]},
                {"shelf_id": 2, "occupied_by_box_with_id": step[6]},
                {"shelf_id": 3, "occupied_by_box_with_id": step[7]},
                {"shelf_id": 4, "occupied_by_box_with_id": step[8]},
                {"shelf_id": 5, "occupied_by_box_with_id": step[9]},
                {"shelf_id": 6, "occupied_by_box_with_id": step[10]},
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

    for i, step in enumerate(
        [
            (0, 6, 0, 5, 1, #"Take box 215 from shelf 1 and put it on order delivery table, then take box 999 from shelf 5 and put it on shelf 3, then move box 990 from order delivery table to shelf 1."
            215, 0, -1, 0, 999, 990),

            (2, 0, 1, 4, 0, #Take box 999 from shelf 4 and put it on shelf 1, then take box 313 from shelf 2 and move it to shelf 4, then return box 998 from shelf 1 to a free shelf.
            998, 313, -1, 999, 0, 0),

            (2, 6, 3, 0, 0, #Take box 313 from shelf 2 and put it on order delivery table, then return box 990 from order delivery table to a free shelf, then take box 998 from shelf 3 and put it on shelf 5.
            0, 313, 998, 0, -1, -1),

            (0, 1, 2, 0, 0, #Take box 998 from shelf 2 and put it on order delivery table, then return box 999 from shelf 2 to a free shelf, then return box 990 from shelf 1 to a free shelf.
            990, 998, -1, -1, 0, -1),

        ]
    )
]

common_telemetries_4 = [
        {
        "images": [],
        "world_state": {
            "robot_position": [1.0, 1.0, 1.57],
            "boxes": [
                {"box_id": 313, "placed_on_shelf_with_id": step[0]},
                {"box_id": 990, "placed_on_shelf_with_id": step[1]},
                {"box_id": 998, "placed_on_shelf_with_id": step[2]},
                {"box_id": 999, "placed_on_shelf_with_id": step[3]},
                {"box_id": 215, "placed_on_shelf_with_id": step[4]}
            ],
            "shelves": [
                {"shelf_id": 1, "occupied_by_box_with_id": step[5]},
                {"shelf_id": 2, "occupied_by_box_with_id": step[6]},
                {"shelf_id": 3, "occupied_by_box_with_id": step[7]},
                {"shelf_id": 4, "occupied_by_box_with_id": step[8]},
                {"shelf_id": 5, "occupied_by_box_with_id": step[9]},
                {"shelf_id": 6, "occupied_by_box_with_id": step[10]},
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

    for i, step in enumerate(
        [
            (0, 2, 5, 0, 1, #Take box 215 from shelf 1 and put it on order delivery table, then take box 998 from shelf 5 and put it on shelf 3, then bring box 990 from shelf 2 to order delivery table, then return box 999 from shelf 1 to a free shelf.
            215, 990, -1, -1, 998, -1),

            (2, 3, 2, 6, 0, #Take box 313 from shelf 2 and put it on order delivery table, then return box 998 from shelf 2 to a free shelf, move box 999 from order delivery table to shelf 4, then take box 990 from shelf 3 and put it on order delivery table.
            0, 313, 990, -1, 0, -1),

            (4, 0, 5, 4, 2, #Take box 999 from shelf 4 and put it on shelf 1, then take box 215 from shelf 2 and move it to shelf 4, move box 313 from shelf 4 to a free shelf, then take box 998 from shelf 5 and put it on order delivery table.
            0, 215, 0, 999, 998, -1),

        ]
    )
]

one_act = [
    TestCase(
        name=f"1_action_task_{i}",
        request=planner.PlannerRequest(
            goal=goal,
            telemetry=planner.Telemetry(**common_telemetries_1[i]),
            world_model=planner.WorldModel(**common_world_model),
            retries=[],
            max_retries=5,
        ),
        response=planner.PlannerResponse(
            plan=[
 #               planner.Action(name="say", args={"text": f"walking up to {step[0]}"}),
                planner.Action(name="go_to", args={"waypoint_id": step[1]}),
 #               planner.Action(name="say", args={"text": f"taking box {step[2]}"}),
                planner.Action(name="pick_up", args={"box_id": step[2]}),
 #               planner.Action(name="say", args={"text": f"walking up to {step[3]}"}),
                planner.Action(name="go_to", args={"waypoint_id": step[4]}),
 #               planner.Action(name="say", args={"text": f"putting box {step[2]}"}),
                planner.Action(name="drop", args={"shelf_id": step[5]})
            ]
        ),
    ) for i, (goal, step) in enumerate([
        ("Take box 215 from shelf 1 and put it on order delivery table.",
        ('shelf 1', 1, 215, 'order delivery table', 4, 6,)),
        ("Take box 998 from shelf 5 and put it on shelf 3.",
        ('shelf 5', 3, 998, 'shelf 3', 2, 3)),
        ("Bring box 313 from shelf 2 to order delivery table.",
        ('shelf 2', 1, 313, 'order delivery table', 4, 6, )),
        ("Return box 999 from shelf 1 to a free shelf.",
        ('shelf 1', 1, 999, "free shelf", 2, 3)),
        ("Take box 215 from shelf 4 and put it on shelf 1.", 
        ('shelf 4', 2, 215, "shelf 1", 1, 1,)),
        ("Move box 999 from shelf 4 to a free shelf.",
        ('shelf 4', 2, 999, "free shelf", 2, 3,)),
        ("Take box 990 from shelf 5 and put it on order delivery table.",
        ('shelf 5', 3, 990, "order delivery table", 4, 6)),
        ("Take box 998 from shelf 2 and put it on order delivery table.",
        ('shelf 2', 1, 998, "order delivery table", 4, 6,)),
        ("Return box 215 from order delivery table to a free shelf.",
        ('order delivery table', 4, 215, "free shelf", 2, 3)),
        ("Bring box 313 from shelf 1 to order delivery table.", 
        ('shelf 1', 1, 313, "order_delivery table", 4, 6,)),
        ("Take box 215 from shelf 3 and put it on shelf 5.", 
        ('shelf 3', 1, 215, "shelf 5", 3, 5)),
        ("Take box 990 from shelf 2 and put it on order delivery table.", 
        ('shelf 2', 1, 990, "order delivery table", 4, 6)),
        ("Move box 998 from order delivery table to a free shelf.", 
        ("order delivery table", 4, 998, "free shelf", 2, 3)),
        ("Take box 999 from shelf 2 and put it on order delivery table.", 
        ('shelf 2', 1, 999, "order delivery table", 4, 6,)),
        ("Return box 999 from shelf 2 to a free shelf.", 
        ('shelf 2', 1, 999, "free shelf", 2, 3)),
        ("Move box 999 from order delivery table to shelf 4.", 
        ("order delivery table", 4, 999, "shelf 4", 2, 4,)),    
        ("Take box 998 from shelf 3 and put it on order delivery table.", 
        ("shelf 3", 2, 998, "order delivery table", 4, 6)),    
        ("Take box 313 from shelf 5 and put it on shelf 1.", 
        ("shelf 5", 3, 313, "shelf 1", 1, 1)),    
        ("Move box 215 from order delivery table to shelf 1.", 
        ("order delivery table", 4, 215, "shelf 1", 1, 1)) 
    ])
]

two_act = [
    TestCase(
        name=f"2_actions_task_{i}",
        request=planner.PlannerRequest(
            goal=goal,
            telemetry=planner.Telemetry(**common_telemetries_2[i]),
            world_model=planner.WorldModel(**common_world_model),
            retries=[],
            max_retries=5,
        ),
        response=planner.PlannerResponse(
            plan=[
#                planner.Action(name="say", args={"text": f"walking up to {step[0]}"}),
                planner.Action(name="go_to", args={"waypoint_id": step[1]}),
#                planner.Action(name="say", args={"text": f"taking box {step[2]}"}),
                planner.Action(name="pick_up", args={"box_id": step[2]}),
#                planner.Action(name="say", args={"text": f"walking up to {step[3]}"}),
                planner.Action(name="go_to", args={"waypoint_id": step[4]}),
#                planner.Action(name="say", args={"text": f"putting box {step[2]}"}),
                planner.Action(name="drop", args={"shelf_id": step[5]}),

#                planner.Action(name="say", args={"text": f"walking up to {step[6 + 0]}"}),
                planner.Action(name="go_to", args={"waypoint_id": step[6 + 1]}),
#                planner.Action(name="say", args={"text": f"taking box {step[6 + 2]}"}),
                planner.Action(name="pick_up", args={"box_id": step[6 + 2]}),
#                planner.Action(name="say", args={"text": f"walking up to {step[6 + 3]}"}),
                planner.Action(name="go_to", args={"waypoint_id": step[6 + 4]}),
#                planner.Action(name="say", args={"text": f"putting box {step[6 + 2]}"}),
                planner.Action(name="drop", args={"shelf_id": step[6 + 5]}),

            ]
        ),
    ) for i, (goal, step) in enumerate([
        ("Take box 215 from shelf 1 and put it on order delivery table, then take box 313 from shelf 5 and put it on shelf 3.",
        ('shelf 1', 1, 215, 'order delivery table', 4, 6,
         'shelf 5', 3, 313, 'shelf 3', 2, 3)),
        ("Bring box 999 from shelf 2 to order delivery table, then return box 998 from shelf 1 to a free shelf.",
        ('shelf 2', 1, 999, 'order delivery table', 4, 6,
         'shelf 1', 1, 998, "free shelf", 2, 3)),
        ("Take box 990 from shelf 4 and put it on shelf 1, then take box 313 from shelf 2 and move it to shelf 4.", 
        ('shelf 4', 2, 990, "shelf 1", 1, 1,
         'shelf 2', 1, 313, "shelf 4", 2, 4)),
        ("Move box 990 from shelf 4 to a free shelf, then take box 999 from shelf 5 and put it on order delivery table.",
        ('shelf 4', 2, 990, "free shelf", 2, 3,
         'shelf 5', 3, 999, "order delivery table", 4, 6)),
        ("Take box 313 from shelf 2 and put it on order delivery table, then return box 990 from order delivery table to a free shelf.",
        ('shelf 2', 1, 313, "order delivery table", 4, 6,
         'order delivery table', 4, 990, "free shelf", 2, 3)),
        ("Bring box 998 from shelf 1 to order delivery table, then take box 313 from shelf 3 and put it on shelf 5.", 
        ('shelf 1', 1, 998, "order_delivery table", 4, 6,
         'shelf 3', 2, 313, "shelf 5", 3, 5)),
        ("Take box 998 from shelf 2 and put it on order delivery table, then move box 999 from order delivery table to a free shelf.", 
        ('shelf 2', 1, 998, "order delivery table", 4, 6,
         "order delivery table", 4, 999, "free shelf", 2, 3)),
        ("Take box 999 from shelf 2 and put it on order delivery table, then return box 215 from shelf 2 to a free shelf.", 
        ('shelf 2', 1, 999, "order delivery table", 4, 6,
        'shelf 2', 1, 215, "free shelf", 2, 3)),
        ("Move box 999 from order delivery table to shelf 4, then take box 215 from shelf 3 and put it on order delivery table.", 
        ("order delivery table", 4, 999, "shelf 4", 2, 4,
        "shelf 3", 2, 215, "order delivery table", 4, 6)),
        ("Take box 313 from shelf 5 and put it on order delivery table, then move box 990 from order delivery table to shelf 1.", 
        ("shelf 5", 3, 313, "order delivery table", 4, 6, 
        "order delivery table", 4, 990, "shelf 1", 1, 1))
    ])
]

three_act = [   
    TestCase(
        name=f"3_action_task_{i}",
        request=planner.PlannerRequest(
            goal=goal,
            telemetry=planner.Telemetry(**common_telemetries_3[i]),
            world_model=planner.WorldModel(**common_world_model),
            retries=[],
            max_retries=5,
        ),
        response=planner.PlannerResponse(
            plan=[
#                planner.Action(name="say", args={"text": f"walking up to {step[0]}"}),
                planner.Action(name="go_to", args={"waypoint_id": step[1]}),
#                planner.Action(name="say", args={"text": f"taking box {step[2]}"}),
                planner.Action(name="pick_up", args={"box_id": step[2]}),
#                planner.Action(name="say", args={"text": f"walking up to {step[3]}"}),
                planner.Action(name="go_to", args={"waypoint_id": step[4]}),
#                planner.Action(name="say", args={"text": f"putting box {step[2]}"}),
                planner.Action(name="drop", args={"shelf_id": step[5]}),

#                planner.Action(name="say", args={"text": f"walking up to {step[6 + 0]}"}),
                planner.Action(name="go_to", args={"waypoint_id": step[6 + 1]}),
#                planner.Action(name="say", args={"text": f"taking box {step[6 + 2]}"}),
                planner.Action(name="pick_up", args={"box_id": step[6 + 2]}),
#                planner.Action(name="say", args={"text": f"walking up to {step[6 + 3]}"}),
                planner.Action(name="go_to", args={"waypoint_id": step[6 + 4]}),
#                planner.Action(name="say", args={"text": f"putting box {step[6 + 2]}"}),
                planner.Action(name="drop", args={"shelf_id": step[6 + 5]}),

#                planner.Action(name="say", args={"text": f"walking up to {step[6*2 + 0]}"}),
                planner.Action(name="go_to", args={"waypoint_id": step[6*2 + 1]}),
#                planner.Action(name="say", args={"text": f"taking box {step[6*2 + 2]}"}),
                planner.Action(name="pick_up", args={"box_id": step[6*2 + 2]}),
#                planner.Action(name="say", args={"text": f"walking up to {step[6*2 + 3]}"}),
                planner.Action(name="go_to", args={"waypoint_id": step[6*2 + 4]}),
#                planner.Action(name="say", args={"text": f"putting box {step[6*2 + 2]}"}),
                planner.Action(name="drop", args={"shelf_id": step[6*2 + 5]}),

            ]
        ),
    ) for i, (goal, step) in enumerate([
        ("Take box 215 from shelf 1 and put it on order delivery table, then take box 999 from shelf 5 and put it on shelf 3, then move box 990 from order delivery table to shelf 1.",
        ('shelf 1', 1, 215, 'order delivery table', 4, 6,
         'shelf 5', 3, 999, 'shelf 3', 2, 3,
         "order delivery table", 4, 990, "shelf 1", 1, 1)), 
        ("Take box 999 from shelf 4 and put it on shelf 1, then take box 313 from shelf 2 and move it to shelf 4, then return box 998 from shelf 1 to a free shelf.", 
        ('shelf 4', 2, 999, "shelf 1", 1, 1,
         'shelf 2', 1, 313, "shelf 4", 2, 4,
         'shelf 1', 1, 998, "free shelf", 2, 3)),
        ("Take box 313 from shelf 2 and put it on order delivery table, then return box 990 from order delivery table to a free shelf, then take box 998 from shelf 3 and put it on shelf 5.",
        ('shelf 2', 1, 313, "order delivery table", 4, 6,
         'order delivery table', 4, 990, "free shelf", 2, 3,
         'shelf 3', 2, 998, "shelf 5", 3, 5)),
        ("Take box 998 from shelf 2 and put it on order delivery table, then return box 999 from shelf 2 to a free shelf, then return box 990 from shelf 1 to a free shelf.", 
        ('shelf 2', 1, 998, "order delivery table", 4, 6,
         'shelf 2', 1, 999, "free shelf", 2, 3,
         'shelf 1', 1, 990, "free shelf", 2, 3))
        ]
    )
]

four_act = [
    TestCase(
        name=f"4_action_task_{i}",
        request=planner.PlannerRequest(
            goal=goal,
            telemetry=planner.Telemetry(**common_telemetries_4[i]),
            world_model=planner.WorldModel(**common_world_model),
            retries=[],
            max_retries=5,
        ),
        response=planner.PlannerResponse(
            plan=[
#                planner.Action(name="say", args={"text": f"walking up to {step[0]}"}),
                planner.Action(name="go_to", args={"waypoint_id": step[1]}),
#                planner.Action(name="say", args={"text": f"taking box {step[2]}"}),
                planner.Action(name="pick_up", args={"box_id": step[2]}),
#               planner.Action(name="say", args={"text": f"walking up to {step[3]}"}),
                planner.Action(name="go_to", args={"waypoint_id": step[4]}),
#                planner.Action(name="say", args={"text": f"putting box {step[2]}"}),
                planner.Action(name="drop", args={"shelf_id": step[5]}),

#                planner.Action(name="say", args={"text": f"walking up to {step[6]}"}),
                planner.Action(name="go_to", args={"waypoint_id": step[7]}),
#                planner.Action(name="say", args={"text": f"taking box {step[8]}"}),
                planner.Action(name="pick_up", args={"box_id": step[8]}),
#                planner.Action(name="say", args={"text": f"walking up to {step[9]}"}),
                planner.Action(name="go_to", args={"waypoint_id": step[10]}),
 #               planner.Action(name="say", args={"text": f"putting box {step[8]}"}),
                planner.Action(name="drop", args={"shelf_id": step[11]}),

#                planner.Action(name="say", args={"text": f"walking up to {step[6]}"}),
                planner.Action(name="go_to", args={"waypoint_id": step[7]}),
#                planner.Action(name="say", args={"text": f"taking box {step[8]}"}),
                planner.Action(name="pick_up", args={"box_id": step[8]}),
#                planner.Action(name="say", args={"text": f"walking up to {step[9]}"}),
                planner.Action(name="go_to", args={"waypoint_id": step[10]}),
#               planner.Action(name="say", args={"text": f"putting box {step[8]}"}),
                planner.Action(name="drop", args={"shelf_id": step[11]}),

   #             planner.Action(name="say", args={"text": f"walking up to {step[6]}"}),
                planner.Action(name="go_to", args={"waypoint_id": step[7]}),
  #              planner.Action(name="say", args={"text": f"taking box {step[8]}"}),
                planner.Action(name="pick_up", args={"box_id": step[8]}),
 #               planner.Action(name="say", args={"text": f"walking up to {step[9]}"}),
                planner.Action(name="go_to", args={"waypoint_id": step[10]}),
#                planner.Action(name="say", args={"text": f"putting box {step[8]}"}),
                planner.Action(name="drop", args={"shelf_id": step[11]}),
                
            ]
        ),
    ) for i, (goal, step) in enumerate([
        ("Take box 215 from shelf 1 and put it on order delivery table, then take box 998 from shelf 5 and put it on shelf 3, then bring box 990 from shelf 2 to order delivery table, then return box 999 from shelf 1 to a shelf 3.",
        ('shelf 1', 1, 215, 'order delivery table', 4, 6,
         'shelf 5', 3, 998, 'shelf 3', 2, 3,
         'shelf 2', 1, 990, 'order delivery table', 4, 6,
         'shelf 1', 1, 999, "shelf 3", 2, 3)),
        ("Take box 313 from shelf 2 and put it on order delivery table, then return box 998 from shelf 2 to shelf 4, move box 999 from order delivery table to shelf 4, then take box 990 from shelf 3 and put it on order delivery table.", 
        ('shelf 2', 1, 313, "order delivery table", 4, 6,
         'shelf 2', 1, 998, "shelf 4", 2, 3,
         "order delivery table", 4, 999, "shelf 4", 2, 4,
         "shelf 3", 2, 990, "order delivery table", 4, 6)),
        ("Take box 999 from shelf 4 and put it on shelf 1, then take box 215 from shelf 2 and move it to shelf 4, move box 313 from shelf 4 to a free shelf, then take box 998 from shelf 5 and put it on order delivery table.", 
        ('shelf 4', 2, 999, "shelf 1", 1, 1,
         'shelf 2', 1, 215, "shelf 4", 2, 4,
         'shelf 4', 2, 313, "free shelf", 2, 3,
         'shelf 5', 3, 998, "order delivery table", 4, 6)),        ]
    )
]

test_cases =  two_act + three_act + four_act

def test(test_case):
    response = planner.chain.invoke(test_case.request.json())
    #print(json.dumps(response.json(), indent=2))
    comp =  json.loads(test_case.response.json())["plan"]
    #print(f"{test_case.name}:{action_response == comp}")
    action_response = []

    for act in json.loads(response.json())["plan"]: #json.loads(response.json()):
        if act["name"] != "say":
            action_response.append(act)
    print(f"{test_case.name}:{action_response == comp}")
    #if not(action_response == json.loads(test_case.response.json())["plan"]):
    print("******************************response*******************************")
    print(action_response)
    print("******************************target************************************")
    print(json.loads(test_case.response.json())["plan"])


for case in test_cases:
	test(case)

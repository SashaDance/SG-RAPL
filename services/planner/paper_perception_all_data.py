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
             "placed_on_shelf_with_id": 6, # Initial state
             "position": [0.0, 0.0, 0.0],
             "orientation_rpy": [0.0, 0.0, 0.0],
             "aruco_marker_id": 313,
             "color_rgb": [255, 50, 50],
         },
         {
             "box_id": 990,
             "name": "Box 990",
             "placed_on_shelf_with_id": 2, # Initial state
             "position": [0.0, 0.0, 0.0],
             "orientation_rpy": [0.0, 0.0, 0.0],
             "aruco_marker_id": 990,
             "color_rgb": [255, 50, 50],
         },
         {
             "box_id": 999,
             "name": "Box 999",
             "placed_on_shelf_with_id": 4, # Initial state
             "position": [0.0, 0.0, 0.0],
             "orientation_rpy": [0.0, 0.0, 0.0],
             "aruco_marker_id": 999,
             "color_rgb": [255, 50, 50],
         },
         {
             "box_id": 998,
             "name": "Box 998",
             "placed_on_shelf_with_id": 5, # Initial state
             "position": [0.0, 0.0, 0.0],
             "orientation_rpy": [0.0, 0.0, 0.0],
             "aruco_marker_id": 998,
             "color_rgb": [255, 50, 50],
         },
     ],
     "walls": [],
     "localization_markers": [],
}

seg_track_datas = [
    #0 simple 3 box, free shelves
    {
        "count_box_and_containers": 4,
        "scores": [0.912,0.881,0.88,0.876],
        "classes_ids": [2,1,1,2],
        "tracking_ids": [998,1,990,313],
        "boxes": [
            {
                "x_min": 260,
                "y_min": 363,
                "x_max": 402,
                "y_max": 470
            },
            {
                "x_min": 1132,
                "y_min": 549,
                "x_max": 1294,
                "y_max": 706
            },
            {
                "x_min": 675,
                "y_min": 351,
                "x_max": 816,
                "y_max": 425
            },
            {
                "x_min": 431,
                "y_min": 377,
                "x_max": 535,
                "y_max": 447
            }
        ],
        "poses": [],
        "box_on_box": False,
        "man_in_frame": True,
        "box_container_on_floor": True,
        "box_or_container_in_frame": True,
        "right_size_flags": False,
        "boxes_output": [
            {"box_id": 998,"placed_on_shelf_with_id": 1},
            {"box_id": 0,"placed_on_shelf_with_id": -1},
            {"box_id": 990,"placed_on_shelf_with_id": 3},
            {"box_id": 313,"placed_on_shelf_with_id": 2}
        ],
        "shelves": [
            {
                "shelf_id": 3,
                "x": 0.107,
                "y": -0.297,
                "occupied_by_box_with_id": 990,
                "pose": {}
            },
            {
                "shelf_id": 4,
                "x": 0.378,
                "y": -0.357,
                "occupied_by_box_with_id": -1,
                "pose": {}
            },
            {
                "shelf_id": 1,
                "x": -0.698,
                "y": -0.101,
                "occupied_by_box_with_id": 998,
                "pose": {}
            },
            {
                "shelf_id": 2,
                "x": -0.427,
                "y": -0.164,
                "occupied_by_box_with_id": 313,
                "pose": {}
            },
            {
                "shelf_id": 5,
                "x": 0.878,
                "y": -0.351,
                "occupied_by_box_with_id": 0,
                "pose": {}
            }
        ],
        "graph_box_on_box": None
    },
    #1 simple 2 box, box on box, free shelf
    {
        "count_box_and_containers": 4,
        "scores": [0.913, 0.87, 0.829, 0.786],
        "classes_ids": [1, 1, 2, 2],
        "tracking_ids": [0, 2, 998, 313],
        "boxes": [
            {"x_min": 211,"y_min": 364,"x_max": 418,"y_max": 478},
            {"x_min": 1133,"y_min": 549,"x_max": 1291,"y_max": 708},
            {"x_min": 962,"y_min": 378,"x_max": 1072,"y_max": 439},
            {"x_min": 981,"y_min": 333,"x_max": 1062,"y_max": 379}
        ],
        "poses": [],
        "box_on_box": True,
        "man_in_frame": True,
        "box_container_on_floor": True,
        "box_or_container_in_frame": True,
        "right_size_flags": False,
        "boxes_output": [
            {"box_id": 0, "placed_on_shelf_with_id": -1},
            {"box_id": 0, "placed_on_shelf_with_id": -1},
            {"box_id": 998, "placed_on_shelf_with_id": 2},
            {"box_id": 313, "placed_on_shelf_with_id": 2}
        ],
        "shelves": [
            {
                "shelf_id": 1,
                "x": -0.698,
                "y": -0.101,
                "occupied_by_box_with_id": -1,
                "pose": {}
            },
            {
                "shelf_id": 2,
                "x": -0.427,
                "y": -0.164,
                "occupied_by_box_with_id": 313,
                "pose": {}
            }
        ],
        "graph_box_on_box": {
            "id_1": 998,
            "id_2": 313,
            "rel_id": 2,
            "class_name_1": "box",
            "rel_name": "on_top",
            "class_name_2": "box"
        }
    },
    #3 simple 1 box , free shelf
    {
        "count_box_and_containers": 4,
        "scores": [0.966,0.937,0.906,0.849],
        "classes_ids": [2,1,2,1],
        "tracking_ids": [998,0,1,3],
        "boxes": [
            {
                "x_min": 250,
                "y_min": 210,
                "x_max": 700,
                "y_max": 574
            },
            {
                "x_min": 816,
                "y_min": 25,
                "x_max": 1224,
                "y_max": 372
            },
            {
                "x_min": 374,
                "y_min": 70,
                "x_max": 665,
                "y_max": 244
            },
            {
                "x_min": 0,
                "y_min": 420,
                "x_max": 43,
                "y_max": 559
            }
        ],
        "poses": [],
        "box_on_box": False,
        "man_in_frame": True,
        "box_container_on_floor": True,
        "box_or_container_in_frame": True,
        "right_size_flags": True,
        "boxes_output": [
            {"box_id": 998,"placed_on_shelf_with_id": 3},
            {"box_id": 0,"placed_on_shelf_with_id": -1},
            {"box_id": 0,"placed_on_shelf_with_id": -1},
            {"box_id": 0,"placed_on_shelf_with_id": -1}
        ],
        "shelves": [
            {
                "shelf_id": 3,
                "x": -0.105,
                "y": 0.104,
                "occupied_by_box_with_id": 998,
                "pose": {}
            },
            {
                "shelf_id": 4,
                "x": 0.227,
                "y": 0.102,
                "occupied_by_box_with_id": -1,
                "pose": {}
            }
        ],
        "graph_box_on_box": None
    },
    #5 simple 1 box
    {
        "count_box_and_containers": 1,
        "scores": [0.966],
        "classes_ids": [2],
        "tracking_ids": [998],
        "boxes": [
            {
                "x_min": 619,
                "y_min": 230,
                "x_max": 1037,
                "y_max": 540
            }
        ],
        "poses": [],
        "box_on_box": False,
        "man_in_frame": True,
        "box_container_on_floor": False,
        "box_or_container_in_frame": True,
        "right_size_flags": True,
        "boxes_output": [
            {"box_id": 998,"placed_on_shelf_with_id": 5}
        ],
        "shelves": [
            {
                "shelf_id": 5,
                "x": 0.042,
                "y": 0.077,
                "occupied_by_box_with_id": 998,
                "pose": {}
            }
        ],
        "graph_box_on_box": None
    },
    #6 simple 2 box
    {
        "count_box_and_containers": 4,
        "scores": [0.949,0.867,0.762,0.513],
        "classes_ids": [1,1,1,2],
        "tracking_ids": [990,313,2,3],
        "boxes": [
            {
                "x_min": 855,
                "y_min": 241,
                "x_max": 1353,
                "y_max": 566
            },
            {
                "x_min": 383,
                "y_min": 311,
                "x_max": 709,
                "y_max": 546
            },
            {
                "x_min": 1398,
                "y_min": 421,
                "x_max": 1440,
                "y_max": 556
            },
            {
                "x_min": 384,
                "y_min": 313,
                "x_max": 710,
                "y_max": 545
            }
        ],
        "poses": [],
        "box_on_box": False,
        "man_in_frame": True,
        "box_container_on_floor": False,
        "box_or_container_in_frame": True,
        "right_size_flags": False,
        "boxes_output": [
            {"box_id": 990,"placed_on_shelf_with_id": 2},
            {"box_id": 313,"placed_on_shelf_with_id": 1},
            {"box_id": 0,"placed_on_shelf_with_id": -1},
            {"box_id": 0,"placed_on_shelf_with_id": -1}
        ],
        "shelves": [
            {
                "shelf_id": 1,
                "x": -0.068,
                "y": 0.089,
                "occupied_by_box_with_id": 313,
                "pose": {}
            },
            {
                "shelf_id": 2,
                "x": 0.273,
                "y": 0.087,
                "occupied_by_box_with_id": 990,
                "pose": {}
            }
        ],
        "graph_box_on_box": None
    },
    #7 simple 2 box
    {
        "count_box_and_containers": 5,
        "scores": [0.957,0.939,0.932,0.811,0.707],
        "classes_ids": [2,1,2,1,1],
        "tracking_ids": [998,999,0,2,4],
        "boxes": [
            {
                "x_min": 392,
                "y_min": 220,
                "x_max": 883,
                "y_max": 559
            },
            {
                "x_min": 880,
                "y_min": 287,
                "x_max": 1245,
                "y_max": 553
            },
            {
                "x_min": 511,
                "y_min": 82,
                "x_max": 800,
                "y_max": 241
            },
            {
                "x_min": 1396,
                "y_min": 397,
                "x_max": 1440,
                "y_max": 562
            },
            {
                "x_min": 1229,
                "y_min": 372,
                "x_max": 1366,
                "y_max": 530
            }
        ],
        "poses": [],
        "box_on_box": False,
        "man_in_frame": True,
        "box_container_on_floor": True,
        "box_or_container_in_frame": True,
        "right_size_flags": False,
        "boxes_output": [
            {"box_id": 998,"placed_on_shelf_with_id": 1},
            {"box_id": 999,"placed_on_shelf_with_id": 2},
            {"box_id": 0,"placed_on_shelf_with_id": -1},
            {"box_id": 0,"placed_on_shelf_with_id": -1},
            {"box_id": 0,"placed_on_shelf_with_id": -1}
        ],
        "shelves": [
            {
                "shelf_id": 1,
                "x": -0.068,
                "y": 0.089,
                "occupied_by_box_with_id": 998,
                "pose": {}
            },
            {
                "shelf_id": 2,
                "x": 0.272,
                "y": 0.086,
                "occupied_by_box_with_id": 999,
                "pose": {}
            }
        ],
        "graph_box_on_box": None
    },
    #8 simple 2 box
    {
        "count_box_and_containers": 2,
        "scores": [0.95,0.945],
        "classes_ids": [1,1],
        "tracking_ids": [999,990],
        "boxes": [
            {
                "x_min": 832,
                "y_min": 252,
                "x_max": 1266,
                "y_max": 581
            },
            {
                "x_min": 218,
                "y_min": 167,
                "x_max": 844,
                "y_max": 591
            }
        ],
        "poses": [],
        "box_on_box": False,
        "man_in_frame": False,
        "box_container_on_floor": False,
        "box_or_container_in_frame": True,
        "right_size_flags": True,
        "boxes_output": [
            {"box_id": 999,"placed_on_shelf_with_id": 4},
            {"box_id": 990,"placed_on_shelf_with_id": 3}
        ],
        "shelves": [
            {
                "shelf_id": 3,
                "x": -0.105,
                "y": 0.104,
                "occupied_by_box_with_id": 990,
                "pose": {}
            },
            {
                "shelf_id": 4,
                "x": 0.227,
                "y": 0.102,
                "occupied_by_box_with_id": 999,
                "pose": {}
            }
        ],
        "graph_box_on_box": None
    }
]

telemetries = [
    {
        "images": [],
        "world_state": {
            "robot_position": [1.0, 1.0, 1.57],
            "boxes": [
                 {"box_id": 313, "placed_on_shelf_with_id": 6}, 
                 {"box_id": 990, "placed_on_shelf_with_id": 2},
                 {"box_id": 998, "placed_on_shelf_with_id": 5},
                 {"box_id": 999, "placed_on_shelf_with_id": 4},
                 {"box_id": 215, "placed_on_shelf_with_id": 1}
            ],
            "shelves": [
                 {"shelf_id": 1, "occupied_by_box_with_id": 215},
                 {"shelf_id": 2, "occupied_by_box_with_id": 990},
                 {"shelf_id": 3, "occupied_by_box_with_id": -1},
                 {"shelf_id": 4, "occupied_by_box_with_id": 999},
                 {"shelf_id": 5, "occupied_by_box_with_id": 998},
                 {"shelf_id": 6, "occupied_by_box_with_id": 313},
            ],
        },
        "seg_track": seg_data
    } for seg_data in seg_track_datas
]

test_definitions_0 = [
    # ("Take box 313 from shelf 2 and put it on order delivery table.",
    #  ('shelf 2', 1, 313, 'order delivery table', 4, 6)),

    # --- 15 New Test Cases ---
    # Move Box 998 (starts on shelf 1 per seg_track)
    ("Take box 998 from shelf 1 and put it on shelf 4.", #ok
     ('shelf 1', 1, 998, 'shelf 4', 2, 4)),
    ("Take box 998 from shelf 5 and put it on shelf 3.", #fixed
     ('shelf 1', 1, 998, 'shelf 5', 2, 3)),
    ("Take box 998 from shelf 5 and put it on the order delivery table.",
     ('shelf 1', 1, 998, 'order delivery table', 4, 6)),
    ("Take box 998 from shelf 5 and put it on shelf 2.",
     ('shelf 1', 1, 998, 'shelf 2', 1, 2)), # Nearby shelf
    ("Take box 998 from shelf 1 and put it on shelf 3.",
     ('shelf 1', 1, 998, 'shelf 3', 2, 3)),

    # Move Box 313 (starts on shelf 2 per seg_track)
    ("Take box 313 from shelf 2 and put it on shelf 5.",
     ('shelf 2', 1, 313, 'shelf 5', 3, 5)),
    ("Take box 313 from shelf 4 and put it on shelf 1.",
     ('shelf 2', 1, 313, 'shelf 1', 1, 1)), # Nearby shelf
    ("Take box 313 from shelf 4 and put it on the order delivery table.",
     ('shelf 2', 1, 313, 'order delivery table', 4, 6)),
    ("Take box 313 from shelf 2 and put it on shelf 4.",
     ('shelf 2', 1, 313, 'shelf 4', 2, 4)),

    # Move Box 990 (starts on shelf 3 per seg_track) #2
    ("Take box 990 from shelf 2 and put it on the order delivery table.",
     ('shelf 3', 2, 990, 'order delivery table', 4, 6)),
    ("Take box 990 from shelf 2 and put it on shelf 1.",
     ('shelf 3', 2, 990, 'shelf 1', 1, 1)),
    ("Take box 990 from shelf 2 and put it on shelf 5.",
     ('shelf 3', 2, 990, 'shelf 5', 3, 5)),
    ("Take box 990 from shelf 3 and put it on shelf 2.",
     ('shelf 3', 2, 990, 'shelf 2', 1, 2)),

    # Move Box 999 (starts on shelf 4 per world_model, not seen in seg_track)
    ("Take box 999 from shelf 4 and put it on shelf 1.",
     ('shelf 4', 2, 999, 'shelf 1', 1, 1)),
    ("Take box 999 from shelf 4 and put it on the order delivery table.",
     ('shelf 4', 2, 999, 'order delivery table', 4, 6)),
]

test_definitions_1 = [
    # --- Moving Top Box (998 from Shelf 2) ---
    ("Move box 998 from shelf 2 to shelf 1",
     ('shelf 2', 1, 998, 'shelf 1', 1, 1)),
    ("Move box 998 from shelf 5 to shelf 3",
     ('shelf 2', 1, 998, 'shelf 3', 2, 3)),
    ("Move box 998 from shelf 2 to shelf 4",
     ('shelf 2', 1, 998, 'shelf 4', 2, 4)),
    ("Move box 998 from shelf 3 to shelf 5",
     ('shelf 2', 1, 998, 'shelf 5', 3, 5)),
    ("Move box 998 from shelf 2 to the order table", # Shelf 6 = order table
     ('shelf 2', 1, 998, 'order delivery table', 4, 6)),
    ("Move box 998 from shelf 2 back to shelf 2", # Edge case: move to same shelf
     ('shelf 2', 1, 998, 'shelf 2', 1, 2)),

    # --- Moving Other Box (999 from Shelf 4 - assumed) ---
    ("Move box 999 from shelf 5 to shelf 1",
     ('shelf 4', 2, 999, 'shelf 1', 1, 1)),
    ("Move box 999 from shelf 4 to shelf 2", # Move to the currently stacked shelf
     ('shelf 4', 2, 999, 'shelf 2', 1, 2)),
    ("Move box 999 from shelf 2 to shelf 3",
     ('shelf 4', 2, 999, 'shelf 3', 2, 3)),
    ("Move box 999 from shelf 4 to shelf 5",
     ('shelf 4', 2, 999, 'shelf 5', 3, 5)),
    ("Move box 999 from shelf 1 to the order table",
     ('shelf 4', 2, 999, 'order delivery table', 4, 6)),
    ("Move box 999 from shelf 4 back to shelf 4", # Edge case: move to same shelf
     ('shelf 4', 2, 999, 'shelf 4', 2, 4)),
]

test_definitions_3 = [
    ("Move box 998 from shelf 3 to shelf 1",
     ('shelf 3', 2, 998, 'shelf 1', 1, 1)),
    ("Move box 998 from shelf 1 to shelf 2",
     ('shelf 3', 2, 998, 'shelf 2', 1, 2)),
    ("Move box 998 from shelf 2 to shelf 4", # Shelf 4 is known empty
     ('shelf 3', 2, 998, 'shelf 4', 2, 4)),
    ("Move box 998 from shelf 1 to shelf 5",
     ('shelf 3', 2, 998, 'shelf 5', 3, 5)),
    ("Move box 998 from shelf 3 to the order table", # Shelf 6
     ('shelf 3', 2, 998, 'order delivery table', 4, 6)),

    # --- Moving Box 313 (Assumed from Shelf 6, WP 4) ---
    ("Move box 313 from shelf 2 to shelf 1",
     ('order delivery table', 4, 313, 'shelf 1', 1, 1)),
    ("Move box 313 from the order table to shelf 2",
     ('order delivery table', 4, 313, 'shelf 2', 1, 2)),
    ("Move box 313 from shelf 5 to shelf 3", # Target shelf is occupied by stack
     ('order delivery table', 4, 313, 'shelf 3', 2, 3)),
    ("Move box 313 from shelf 1 to shelf 4", # Target shelf is known empty
     ('order delivery table', 4, 313, 'shelf 4', 2, 4)),
    ("Move box 313 from the order table to shelf 5",
     ('order delivery table', 4, 313, 'shelf 5', 3, 5)),

    # --- Moving Box 990 (Assumed from Shelf 2, WP 1) ---
    ("Move box 990 from shelf 2 to shelf 1",
     ('shelf 2', 1, 990, 'shelf 1', 1, 1)),
    ("Move box 990 from shelf 4 to shelf 3", # Target shelf is occupied by stack
     ('shelf 2', 1, 990, 'shelf 3', 2, 3)),
    ("Move box 990 from shelf 5 to shelf 4", # Target shelf is known empty
     ('shelf 2', 1, 990, 'shelf 4', 2, 4)),
    ("Move box 990 from shelf 3 to shelf 5",
     ('shelf 2', 1, 990, 'shelf 5', 3, 5)),
    ("Move box 990 from shelf 2 to the order table", # Shelf 6
     ('shelf 2', 1, 990, 'order delivery table', 4, 6)),
]

test_definitions_5 = [
    ("Move box 998 from shelf 5 to shelf 1",
     ('shelf 5', 3, 998, 'shelf 1', 1, 1)),
    ("Move box 998 from shelf 4 to shelf 2",
     ('shelf 5', 3, 998, 'shelf 2', 1, 2)),
    ("Move box 998 from shelf 5 to the order table", # Shelf 6
     ('shelf 5', 3, 998, 'order delivery table', 4, 6)),

    # --- Moving Box 313 (Assumed from Shelf 6, WP 4) ---
    ("Move box 313 from the order table to shelf 1",
     ('order delivery table', 4, 313, 'shelf 1', 1, 1)),
    ("Move box 313 from the order table to shelf 3",
     ('order delivery table', 4, 313, 'shelf 3', 2, 3)),
    ("Move box 313 from the order table to shelf 5", # Target is occupied by 998
     ('order delivery table', 4, 313, 'shelf 5', 3, 5)),

    # --- Moving Box 990 (Assumed from Shelf 2, WP 1) ---
    ("Move box 990 from shelf 5 to shelf 3",
     ('shelf 2', 1, 990, 'shelf 3', 2, 3)),
    ("Move box 990 from shelf 5 to shelf 4",
     ('shelf 2', 1, 990, 'shelf 4', 2, 4)),
    ("Move box 990 from shelf 2 to the order table", # Shelf 6
     ('shelf 2', 1, 990, 'order delivery table', 4, 6)),

    # --- Moving Box 999 (Assumed from Shelf 4, WP 2) ---
    ("Move box 999 from shelf 3 to shelf 1",
     ('shelf 4', 2, 999, 'shelf 1', 1, 1)),
    ("Move box 999 from shelf 3 to shelf 5", # Target is occupied by 998
     ('shelf 4', 2, 999, 'shelf 5', 3, 5)),
    ("Move box 999 from shelf 4 to the order table", # Shelf 6
     ('shelf 4', 2, 999, 'order delivery table', 4, 6)),
]

test_definitions_6 = [
    # --- Moving Box 990 (Seen on Shelf 2, WP 1) ---
    ("Move box 990 from shelf 5 to shelf 1", # Target occupied by 313
     ('shelf 2', 1, 990, 'shelf 1', 1, 1)),
    ("Move box 990 from shelf 5 to shelf 3",
     ('shelf 2', 1, 990, 'shelf 3', 2, 3)),
    ("Move box 990 from shelf 2 to shelf 4",
     ('shelf 2', 1, 990, 'shelf 4', 2, 4)),
    ("Move box 990 from shelf 2 to the order table", # Shelf 6
     ('shelf 2', 1, 990, 'order delivery table', 4, 6)),

    # --- Moving Box 313 (Seen on Shelf 1, WP 1) ---
    ("Move box 313 from shelf 1 to shelf 2", # Target occupied by 990
     ('shelf 1', 1, 313, 'shelf 2', 1, 2)),
    ("Move box 313 from shelf 4 to shelf 3",
     ('shelf 1', 1, 313, 'shelf 3', 2, 3)),
    ("Move box 313 from shelf 4 to shelf 5",
     ('shelf 1', 1, 313, 'shelf 5', 3, 5)),
    ("Move box 313 from shelf 1 to the order table", # Shelf 6
     ('shelf 1', 1, 313, 'order delivery table', 4, 6)),

    # --- Moving Box 998 (Assumed from Shelf 5, WP 3) ---
    ("Move box 998 from shelf 5 to shelf 1", # Target occupied by 313
     ('shelf 5', 3, 998, 'shelf 1', 1, 1)),
    ("Move box 998 from shelf 3 to shelf 2", # Target occupied by 990
     ('shelf 5', 3, 998, 'shelf 2', 1, 2)),
    ("Move box 998 from shelf 5 to shelf 4",
     ('shelf 5', 3, 998, 'shelf 4', 2, 4)),
    ("Move box 998 from shelf 2 to the order table", # Shelf 6
     ('shelf 5', 3, 998, 'order delivery table', 4, 6)),

    # --- Moving Box 999 (Assumed from Shelf 4, WP 2) ---
    ("Move box 999 from shelf 4 to shelf 1", # Target occupied by 313
     ('shelf 4', 2, 999, 'shelf 1', 1, 1)),
    ("Move box 999 from shelf 4 to shelf 3",
     ('shelf 4', 2, 999, 'shelf 3', 2, 3)),
    ("Move box 999 from shelf 4 to the order table", # Shelf 6
     ('shelf 4', 2, 999, 'order delivery table', 4, 6)),
]

test_definitions_7 = [
    ("Move box 998 from shelf 1 to shelf 2", # Target occupied by 999
     ('shelf 1', 1, 998, 'shelf 2', 1, 2)),
    ("Move box 998 from shelf 2 to shelf 3",
     ('shelf 1', 1, 998, 'shelf 3', 2, 3)),
    ("Move box 998 from shelf 1 to shelf 4",
     ('shelf 1', 1, 998, 'shelf 4', 2, 4)),
    ("Move box 998 from shelf 2 to shelf 5",
     ('shelf 1', 1, 998, 'shelf 5', 3, 5)),
    ("Move box 998 from shelf 1 to the order table", # Shelf 6
     ('shelf 1', 1, 998, 'order delivery table', 4, 6)),

    # --- Moving Box 999 (Seen on Shelf 2, WP 1) ---
    ("Move box 999 from shelf 2 to shelf 1", # Target occupied by 998
     ('shelf 2', 1, 999, 'shelf 1', 1, 1)),
    ("Move box 999 from shelf 2 to shelf 3",
     ('shelf 2', 1, 999, 'shelf 3', 2, 3)),
    ("Move box 999 from shelf 2 to shelf 4",
     ('shelf 2', 1, 999, 'shelf 4', 2, 4)),
    ("Move box 999 from shelf 2 to shelf 5",
     ('shelf 2', 1, 999, 'shelf 5', 3, 5)),
    ("Move box 999 from shelf 2 to the order table", # Shelf 6
     ('shelf 2', 1, 999, 'order delivery table', 4, 6)),

    # --- Moving Box 313 (Assumed from Shelf 6, WP 4) ---
    ("Move box 313 from the order table to shelf 1", # Target occupied by 998
     ('order delivery table', 4, 313, 'shelf 1', 1, 1)),
    ("Move box 313 from the order table to shelf 2", # Target occupied by 999
     ('order delivery table', 4, 313, 'shelf 2', 1, 2)),
    ("Move box 313 from the order table to shelf 3",
     ('order delivery table', 4, 313, 'shelf 3', 2, 3)),
    ("Move box 313 from the order table to shelf 4",
     ('order delivery table', 4, 313, 'shelf 4', 2, 4)),
    ("Move box 313 from the order table to shelf 5",
     ('order delivery table', 4, 313, 'shelf 5', 3, 5)),
]

test_definitions_8 = [
        # --- Moving Box 999 (Seen on Shelf 4, WP 2) ---
    ("Move box 999 from shelf 4 to shelf 1",
     ('shelf 4', 2, 999, 'shelf 1', 1, 1)),
    ("Move box 999 from shelf 4 to shelf 2",
     ('shelf 4', 2, 999, 'shelf 2', 1, 2)),
    ("Move box 999 from shelf 4 to the order table", # Shelf 6
     ('shelf 4', 2, 999, 'order delivery table', 4, 6)),

    # --- Moving Box 990 (Seen on Shelf 3, WP 2) ---
    ("Move box 990 from shelf 3 to shelf 1",
     ('shelf 3', 2, 990, 'shelf 1', 1, 1)),
    ("Move box 990 from shelf 3 to shelf 5",
     ('shelf 3', 2, 990, 'shelf 5', 3, 5)),
    ("Move box 990 from shelf 3 to the order table", # Shelf 6
     ('shelf 3', 2, 990, 'order delivery table', 4, 6)),

    # --- Moving Box 313 (Assumed from Shelf 6, WP 4) ---
    ("Move box 313 from the order table to shelf 2",
     ('order delivery table', 4, 313, 'shelf 2', 1, 2)),
    ("Move box 313 from the order table to shelf 3", # Target occupied by 990
     ('order delivery table', 4, 313, 'shelf 3', 2, 3)),
    ("Move box 313 from the order table to shelf 4", # Target occupied by 999
     ('order delivery table', 4, 313, 'shelf 4', 2, 4)),

    # --- Moving Box 998 (Assumed from Shelf 5, WP 3) ---
    ("Move box 998 from shelf 5 to shelf 1",
     ('shelf 5', 3, 998, 'shelf 1', 1, 1)),
    ("Move box 998 from shelf 5 to shelf 3", # Target occupied by 990
     ('shelf 5', 3, 998, 'shelf 3', 2, 3)),
    ("Move box 998 from shelf 5 to the order table", # Shelf 6
     ('shelf 5', 3, 998, 'order delivery table', 4, 6)),

    # --- Moving Box 1 (Assumed from Shelf 1, WP 1) ---
    ("Move box 1 from shelf 1 to shelf 2",
     ('shelf 1', 1, 1, 'shelf 2', 1, 2)),
    ("Move box 1 from shelf 1 to shelf 4", # Target occupied by 999
     ('shelf 1', 1, 1, 'shelf 4', 2, 4)),
    ("Move box 1 from shelf 1 to the order table", # Shelf 6
     ('shelf 1', 1, 1, 'order delivery table', 4, 6)),
] 


test_free_3 = [
    ("Move box 998 from shelf 3 to free shelf",
      ('shelf 3', 2, 998, 'shelf 4', 2, 4)),
    ("Move box 313 from shelf 6 to shelf 4",
      ('order delivery table', 4, 313, 'shelf', 2, 4)),
    ("Move box 990 from shelf 2 to free shelf",
      ('shelf 2', 1, 990, 'shelf 4', 2, 4)),
    ("Transfer box 998 from shelf 3 to shelf 4",
      ('shelf 3', 2, 998, 'shelf 4', 2, 4)),
    ("Place box 313 from order table onto free shelf",
      ('order delivery table', 4, 313, 'shelf 4', 2, 4))
]

test_free_1 = [
    ("Move box 998 from shelf 2 to free shelf",
      ('shelf 2', 1, 998, 'shelf 1', 1, 1)),
    ("Move box 999 from shelf 4 to shelf 1", 
     ('shelf 4', 2, 999, 'shelf 1', 1, 1)),
    ("Transfer box 998 from shelf 2 to free shelf",
      ('shelf 2', 1, 998, 'shelf 1', 1, 1)),
    ("Place box 999 from shelf 4 onto free shelf 1", 
     ('shelf 4', 2, 999, 'shelf 1', 1, 1)),
    ("Move box 998 from shelf 2 to shelf 3", 
     ('shelf 2', 1, 998, 'shelf 3', 2, 3))
]

test_free_0 = [
    ("Move box 998 from shelf 1 to free shelf", # 2 5
     ('shelf 1', 1, 998, 'shelf 4', 2, 4)),
    ("Move box 990 from shelf 3 to shelf 5", 
     ('shelf 3', 2, 990, 'shelf 5', 3, 5)),
    ("Move box 313 from shelf 2 to free shelf", 
     ('shelf 2', 1, 313, 'shelf 4', 2, 4)),
    ("Move box 998 from shelf 1 to free shelf", 
     ('shelf 1', 1, 998, 'shelf 5', 3, 5)),
    ("Move box 990 from shelf 3 to order delivery table", 
     ('shelf 3', 2, 990, 'order delivery table', 4, 6)),
]

test_on_top_1 = [
    ("Move box 998 from shelf 2 to shelf 1", 998, 1),
    ("Move box 998 from shelf 2 to shelf 3", 998, 3),
    ("Move box 998 from shelf 2 to shelf 4", 998, 4),
    ("Move box 998 from shelf 2 to shelf 5", 998, 5),
    ("Move box 998 from shelf 2 to order table", 998, 6), # Shelf 6 is order table

    # Complex plans: Moving the bottom box (313) from shelf 2
    ("Move box 313 from shelf 2 to shelf 3", 313, 3), # Temp shelf for 998 = 1
    ("Move box 313 from shelf 2 to shelf 4", 313, 4), # Temp shelf for 998 = 1
    ("Move box 313 from shelf 2 to shelf 5", 313, 5), # Temp shelf for 998 = 1
    ("Move box 313 from shelf 2 to order table", 313, 6), # Temp shelf for 998 = 1
    ("Move box 313 from shelf 2 to shelf 1", 313, 1), # Target is free shelf 1, use temp shelf 3 for 998
]

test_cases_stacked_logic = []

def get_waypoint_for_shelf(shelf_id):
    if shelf_id in [1, 2]: return 1
    if shelf_id in [3, 4]: return 2
    if shelf_id == 5: return 3
    if shelf_id == 6: return 4
    return 0 # Default or error

stack_info = telemetries[1]["seg_track"].get("graph_box_on_box")
top_box_id = stack_info["id_1"]    # 998
bottom_box_id = stack_info["id_2"] # 313
source_shelf_id = telemetries[1]["seg_track"]["boxes_output"][2]["placed_on_shelf_with_id"] # Shelf 2
source_wp = telemetries[1].get(source_shelf_id)

primary_temp_shelf_id = 1 # From telemetry_data["seg_track"]["shelves"]
primary_temp_wp = get_waypoint_for_shelf(primary_temp_shelf_id)

alternative_temp_shelf_id = 3
alternative_temp_wp = get_waypoint_for_shelf(alternative_temp_shelf_id)

for i, (goal, box_to_move, target_shelf_id) in enumerate(test_on_top_1):
    target_wp = get_waypoint_for_shelf(target_shelf_id)
    expected_plan = []
    plan_type = 'simple' # Default

    if box_to_move == top_box_id: # Moving the top box
        plan_type = 'simple'
        expected_plan = [
            planner.Action(name="go_to", args={"waypoint_id": source_wp}),
            planner.Action(name="pick_up", args={"box_id": top_box_id}),
            planner.Action(name="go_to", args={"waypoint_id": target_wp}),
            planner.Action(name="drop", args={"shelf_id": target_shelf_id})
        ]
    elif box_to_move == bottom_box_id: # Moving the bottom box
        plan_type = 'complex'
        # Determine temporary shelf for the top box
        temp_shelf_id = primary_temp_shelf_id
        temp_wp = primary_temp_wp
        if target_shelf_id == primary_temp_shelf_id: # If target is the primary temp shelf
            temp_shelf_id = alternative_temp_shelf_id
            temp_wp = alternative_temp_wp

        # 1. Move top box (998) to temporary shelf
        expected_plan.extend([
            planner.Action(name="go_to", args={"waypoint_id": source_wp}),
            planner.Action(name="pick_up", args={"box_id": top_box_id}),
            planner.Action(name="go_to", args={"waypoint_id": temp_wp}),
            planner.Action(name="drop", args={"shelf_id": temp_shelf_id})
        ])
        # 2. Move bottom box (313) to final destination
        expected_plan.extend([
             planner.Action(name="go_to", args={"waypoint_id": source_wp}),
             planner.Action(name="pick_up", args={"box_id": bottom_box_id}),
             planner.Action(name="go_to", args={"waypoint_id": target_wp}),
             planner.Action(name="drop", args={"shelf_id": target_shelf_id})
        ])
    else:
        # Should not happen with the current definitions, but handle defensively
        print(f"WARN: Box ID {box_to_move} in definition does not match stack IDs {top_box_id}/{bottom_box_id}")
        continue


    test_case = TestCase(
        name=f"stacked_plan_{plan_type}_{i}", # Include plan type in name
        request=planner.PlannerRequest(
            goal=goal,
            telemetry=planner.Telemetry(**telemetries[1]),
            world_model=planner.WorldModel(**common_world_model),
            retries=[],
            max_retries=5,
        ),
        response=planner.PlannerResponse(plan=expected_plan),
    )
    test_cases_stacked_logic.append(test_case)

test_cases_0 = [
    TestCase(
        name=f"telem_0_1_action_task_{i}", # Unique name for each test
        request=planner.PlannerRequest(
            goal=goal,
            telemetry=planner.Telemetry(**telemetries[0]), # Use the consistent telemetry
            world_model=planner.WorldModel(**common_world_model),
            retries=[],
            max_retries=5,
        ),
        response=planner.PlannerResponse(
            plan=[
                planner.Action(name="go_to", args={"waypoint_id": step[1]}),
                planner.Action(name="pick_up", args={"box_id": step[2]}),
                planner.Action(name="go_to", args={"waypoint_id": step[4]}),
                planner.Action(name="drop", args={"shelf_id": step[5]})
            ]
        ),
    ) for i, (goal, step) in enumerate(test_definitions_0)
]

test_cases_1 = [
    TestCase(
        name=f"telem_1_1_action_task_{i}", # Unique name for each test
        request=planner.PlannerRequest(
            goal=goal,
            telemetry=planner.Telemetry(**telemetries[1]), # Use the consistent telemetry
            world_model=planner.WorldModel(**common_world_model),
            retries=[],
            max_retries=5,
        ),
        response=planner.PlannerResponse(
            plan=[
                planner.Action(name="go_to", args={"waypoint_id": step[1]}),
                planner.Action(name="pick_up", args={"box_id": step[2]}),
                planner.Action(name="go_to", args={"waypoint_id": step[4]}),
                planner.Action(name="drop", args={"shelf_id": step[5]})
            ]
        ),
    ) for i, (goal, step) in enumerate(test_definitions_1)
]

test_cases_3 = [
    TestCase(
        name=f"telem_3_1_action_task_{i}", # Unique name for each test
        request=planner.PlannerRequest(
            goal=goal,
            telemetry=planner.Telemetry(**telemetries[2]), # Use the consistent telemetry
            world_model=planner.WorldModel(**common_world_model),
            retries=[],
            max_retries=5,
        ),
        response=planner.PlannerResponse(
            plan=[
                planner.Action(name="go_to", args={"waypoint_id": step[1]}),
                planner.Action(name="pick_up", args={"box_id": step[2]}),
                planner.Action(name="go_to", args={"waypoint_id": step[4]}),
                planner.Action(name="drop", args={"shelf_id": step[5]})
            ]
        ),
    ) for i, (goal, step) in enumerate(test_definitions_3)
]

test_cases_5 = [
    TestCase(
        name=f"telem_5_1_action_task_{i}", # Unique name for each test
        request=planner.PlannerRequest(
            goal=goal,
            telemetry=planner.Telemetry(**telemetries[3]), # Use the consistent telemetry
            world_model=planner.WorldModel(**common_world_model),
            retries=[],
            max_retries=5,
        ),
        response=planner.PlannerResponse(
            plan=[
                planner.Action(name="go_to", args={"waypoint_id": step[1]}),
                planner.Action(name="pick_up", args={"box_id": step[2]}),
                planner.Action(name="go_to", args={"waypoint_id": step[4]}),
                planner.Action(name="drop", args={"shelf_id": step[5]})
            ]
        ),
    ) for i, (goal, step) in enumerate(test_definitions_5)
]

test_cases_6 = [
    TestCase(
        name=f"telem_6_1_action_task_{i}", # Unique name for each test
        request=planner.PlannerRequest(
            goal=goal,
            telemetry=planner.Telemetry(**telemetries[4]), # Use the consistent telemetry
            world_model=planner.WorldModel(**common_world_model),
            retries=[],
            max_retries=5,
        ),
        response=planner.PlannerResponse(
            plan=[
                planner.Action(name="go_to", args={"waypoint_id": step[1]}),
                planner.Action(name="pick_up", args={"box_id": step[2]}),
                planner.Action(name="go_to", args={"waypoint_id": step[4]}),
                planner.Action(name="drop", args={"shelf_id": step[5]})
            ]
        ),
    ) for i, (goal, step) in enumerate(test_definitions_6)
]

test_cases_7 = [
    TestCase(
        name=f"telem_7_1_action_task_{i}",
        request=planner.PlannerRequest(
            goal=goal,
            telemetry=planner.Telemetry(**telemetries[5]),
            world_model=planner.WorldModel(**common_world_model),
            retries=[],
            max_retries=5,
        ),
        response=planner.PlannerResponse(
            plan=[
                planner.Action(name="go_to", args={"waypoint_id": step[1]}),
                planner.Action(name="pick_up", args={"box_id": step[2]}),
                planner.Action(name="go_to", args={"waypoint_id": step[4]}),
                planner.Action(name="drop", args={"shelf_id": step[5]})
            ]
        ),
    ) for i, (goal, step) in enumerate(test_definitions_7)
]

test_cases_8 = [
    TestCase(
        name=f"telem_8_1_action_task_{i}",
        request=planner.PlannerRequest(
            goal=goal,
            telemetry=planner.Telemetry(**telemetries[6]),
            world_model=planner.WorldModel(**common_world_model),
            retries=[],
            max_retries=5,
        ),
        response=planner.PlannerResponse(
            plan=[
                planner.Action(name="go_to", args={"waypoint_id": step[1]}),
                planner.Action(name="pick_up", args={"box_id": step[2]}),
                planner.Action(name="go_to", args={"waypoint_id": step[4]}),
                planner.Action(name="drop", args={"shelf_id": step[5]})
            ]
        ),
    ) for i, (goal, step) in enumerate(test_definitions_8)
]

test_cases_free_3 = [
    TestCase(
        name=f"telem_3_free_shelf_task_{i}", # Unique name for each test
        request=planner.PlannerRequest(
            goal=goal,
            telemetry=planner.Telemetry(**telemetries[2]), # Use the consistent telemetry
            world_model=planner.WorldModel(**common_world_model),
            retries=[],
            max_retries=5,
        ),
        response=planner.PlannerResponse(
            plan=[
                planner.Action(name="go_to", args={"waypoint_id": step[1]}),
                planner.Action(name="pick_up", args={"box_id": step[2]}),
                planner.Action(name="go_to", args={"waypoint_id": step[4]}),
                planner.Action(name="drop", args={"shelf_id": step[5]})
            ]
        ),
    ) for i, (goal, step) in enumerate(test_free_3)
]

test_cases_free_1 = [
    TestCase(
        name=f"telem_3_free_shelf_task_{i}", # Unique name for each test
        request=planner.PlannerRequest(
            goal=goal,
            telemetry=planner.Telemetry(**telemetries[1]), # Use the consistent telemetry
            world_model=planner.WorldModel(**common_world_model),
            retries=[],
            max_retries=5,
        ),
        response=planner.PlannerResponse(
            plan=[
                planner.Action(name="go_to", args={"waypoint_id": step[1]}),
                planner.Action(name="pick_up", args={"box_id": step[2]}),
                planner.Action(name="go_to", args={"waypoint_id": step[4]}),
                planner.Action(name="drop", args={"shelf_id": step[5]})
            ]
        ),
    ) for i, (goal, step) in enumerate(test_free_1)
]

test_cases_free_0 = [
    TestCase(
        name=f"telem_3_free_shelf_task_{i}", # Unique name for each test
        request=planner.PlannerRequest(
            goal=goal,
            telemetry=planner.Telemetry(**telemetries[0]), # Use the consistent telemetry
            world_model=planner.WorldModel(**common_world_model),
            retries=[],
            max_retries=5,
        ),
        response=planner.PlannerResponse(
            plan=[
                planner.Action(name="go_to", args={"waypoint_id": step[1]}),
                planner.Action(name="pick_up", args={"box_id": step[2]}),
                planner.Action(name="go_to", args={"waypoint_id": step[4]}),
                planner.Action(name="drop", args={"shelf_id": step[5]})
            ]
        ),
    ) for i, (goal, step) in enumerate(test_free_0)
]

plan_log_data = []

def test(test_case, log_list):
    expected_plan = []
    actual_plan = []
    response_json_str = None

    expected_plan = json.loads(test_case.response.json())["plan"]
    
    response = planner.chain.invoke(test_case.request.json())
    response_json_str = response.json()

    response_data = json.loads(response_json_str)
    if "plan" in response_data and isinstance(response_data["plan"], list):
        actual_plan = [act for act in response_data["plan"] if isinstance(act, dict) and act.get("name") != "say"]
    else:
        print(f"WARN: Unexpected response format for {test_case.name}: {response_data}")

    log_list.append((expected_plan, actual_plan))

    print(f"{test_case.name}: Comparison Result -> {expected_plan == actual_plan}")
    if not (expected_plan == actual_plan):
        print("******************************response*******************************")
        print(json.dumps(actual_plan, indent=2))
        print("******************************target*********************************")
        print(json.dumps(expected_plan, indent=2))
        print("*********************************************************************")

new_coord_tests = [test_cases_0, test_cases_1, test_cases_3, test_cases_5, test_cases_6, test_cases_7, test_cases_8]

free_shelf_tests = [test_cases_free_0, test_cases_free_1, test_cases_free_3]

#test_cases_stacked_logic

for test_cases_to_run in free_shelf_tests:
    for case in test_cases_to_run:
        test(case, plan_log_data)

#for case in test_cases_stacked_logic:
#    test(case, plan_log_data)

print("Test execution finished.")

log_filename = f"plan_log_segmentation_free_shelves_new.json"
with open(log_filename, 'w') as f:
    json.dump(plan_log_data, f, indent=4)
print(f"Successfully wrote comparison log to {log_filename}")

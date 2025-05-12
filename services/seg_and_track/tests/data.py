from pathlib import Path
from pydantic.v1 import BaseModel
from services_api.seg_and_track import SegAndTrackRequest, SegAndTrackResponse

BASE_DIR = Path(__file__).resolve().parent / "images"

class TestCase(BaseModel):
    name: str
    request: SegAndTrackRequest
    response: SegAndTrackResponse
    response_comparator: object = lambda checked_response, target_response: checked_response == target_response

test_case_1730299507052386690 = {
    "count_box_and_containers": 4,
    "scores": [
        0.913,
        0.87,
        0.829,
        0.786
    ],
    "classes_ids": [
        1,
        1,
        2,
        2
    ],
    "tracking_ids": [
        0,
        2,
        998,
        313
    ],
    "boxes": [
        {
            "x_min": 211,
            "y_min": 364,
            "x_max": 418,
            "y_max": 478
        },
        {
            "x_min": 1133,
            "y_min": 549,
            "x_max": 1291,
            "y_max": 708
        },
        {
            "x_min": 962,
            "y_min": 378,
            "x_max": 1072,
            "y_max": 439
        },
        {
            "x_min": 981,
            "y_min": 333,
            "x_max": 1062,
            "y_max": 379
        }
    ],
    "poses": [
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        },
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        },
        {
            "rvec": [
                [
                    -2.795,
                    -0.042,
                    -0.072
                ]
            ],
            "tvec": [
                [
                    0.851,
                    -0.519,
                    1.632
                ]
            ]
        },
        {
            "rvec": [
                [
                    -2.619,
                    -0.226,
                    1.317
                ]
            ],
            "tvec": [
                [
                    0.891,
                    -0.672,
                    1.594
                ]
            ]
        }
    ],
    "box_on_box": True,
    "man_in_frame": True,
    "box_container_on_floor": True,
    "box_or_container_in_frame": True,
    "right_size_flags": False,
    "boxes_output": [
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        },
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        },
        {
            "box_id": 998,
            "placed_on_shelf_with_id": 2
        },
        {
            "box_id": 313,
            "placed_on_shelf_with_id": 2
        }
    ],
    "shelves": [
        {
            "shelf_id": 1,
            "x": -0.698,
            "y": -0.101,
            "occupied_by_box_with_id": -1,
            "pose": {
                "rvec": [
                    [
                        -2.962,
                        0.307,
                        -0.998
                    ]
                ],
                "tvec": [
                    [
                        -0.698,
                        -0.101,
                        0.92
                    ]
                ]
            }
        },
        {
            "shelf_id": 2,
            "x": -0.427,
            "y": -0.164,
            "occupied_by_box_with_id": 313,
            "pose": {
                "rvec": [
                    [
                        -2.711,
                        0.166,
                        -0.919
                    ]
                ],
                "tvec": [
                    [
                        -0.427,
                        -0.164,
                        1.126
                    ]
                ]
            }
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
}

test_case_1730299664277007982 = {
    "count_box_and_containers": 2,
    "scores": [
        0.753,
        0.608
    ],
    "classes_ids": [
        1,
        1
    ],
    "tracking_ids": [
        1,
        4
    ],
    "boxes": [
        {
            "x_min": 1396,
            "y_min": 396,
            "x_max": 1440,
            "y_max": 562
        },
        {
            "x_min": 1231,
            "y_min": 378,
            "x_max": 1365,
            "y_max": 532
        }
    ],
    "poses": [
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        },
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        }
    ],
    "box_on_box": False,
    "man_in_frame": True,
    "box_container_on_floor": False,
    "box_or_container_in_frame": True,
    "right_size_flags": True,
    "boxes_output": [
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        },
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        }
    ],
    "shelves": [
        {
            "shelf_id": 1,
            "x": -0.068,
            "y": 0.089,
            "occupied_by_box_with_id": -1,
            "pose": {
                "rvec": [
                    [
                        -2.866,
                        0.002,
                        -0.025
                    ]
                ],
                "tvec": [
                    [
                        -0.068,
                        0.089,
                        0.335
                    ]
                ]
            }
        },
        {
            "shelf_id": 2,
            "x": 0.274,
            "y": 0.087,
            "occupied_by_box_with_id": -1,
            "pose": {
                "rvec": [
                    [
                        -2.844,
                        0.046,
                        -0.001
                    ]
                ],
                "tvec": [
                    [
                        0.274,
                        0.087,
                        0.339
                    ]
                ]
            }
        }
    ],
    "graph_box_on_box": None
}

test_case_1730299927324139623 = {
    "count_box_and_containers": 4,
    "scores": [
        0.966,
        0.937,
        0.906,
        0.849
    ],
    "classes_ids": [
        2,
        1,
        2,
        1
    ],
    "tracking_ids": [
        998,
        0,
        1,
        3
    ],
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
    "poses": [
        {
            "rvec": [
                [
                    -2.848,
                    -0.007,
                    -0.035
                ]
            ],
            "tvec": [
                [
                    -0.15,
                    -0.087,
                    0.265
                ]
            ]
        },
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        },
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        },
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        }
    ],
    "box_on_box": True,
    "man_in_frame": True,
    "box_container_on_floor": True,
    "box_or_container_in_frame": True,
    "right_size_flags": True,
    "boxes_output": [
        {
            "box_id": 998,
            "placed_on_shelf_with_id": 3
        },
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        },
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        },
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        }
    ],
    "shelves": [
        {
            "shelf_id": 3,
            "x": -0.105,
            "y": 0.104,
            "occupied_by_box_with_id": 998,
            "pose": {
                "rvec": [
                    [
                        -2.903,
                        0.014,
                        -0.055
                    ]
                ],
                "tvec": [
                    [
                        -0.105,
                        0.104,
                        0.277
                    ]
                ]
            }
        },
        {
            "shelf_id": 4,
            "x": 0.227,
            "y": 0.102,
            "occupied_by_box_with_id": -1,
            "pose": {
                "rvec": [
                    [
                        -2.898,
                        0.013,
                        -0.027
                    ]
                ],
                "tvec": [
                    [
                        0.227,
                        0.102,
                        0.29
                    ]
                ]
            }
        }
    ],
    "graph_box_on_box": {
        "id_1": 998,
        "id_2": 1,
        "rel_id": 2,
        "class_name_1": "box",
        "rel_name": "on_top",
        "class_name_2": "box"
    }
}
test_case_1730299932262406396 = {
    "count_box_and_containers": 4,
    "scores": [
        0.959,
        0.909,
        0.86,
        0.822
    ],
    "classes_ids": [
        2,
        2,
        1,
        1
    ],
    "tracking_ids": [
        998,
        0,
        1,
        3
    ],
    "boxes": [
        {
            "x_min": 690,
            "y_min": 222,
            "x_max": 1141,
            "y_max": 570
        },
        {
            "x_min": 737,
            "y_min": 74,
            "x_max": 1034,
            "y_max": 246
        },
        {
            "x_min": 0,
            "y_min": 419,
            "x_max": 41,
            "y_max": 559
        },
        {
            "x_min": 128,
            "y_min": 143,
            "x_max": 487,
            "y_max": 452
        }
    ],
    "poses": [
        {
            "rvec": [
                [
                    -2.838,
                    -0.024,
                    0.053
                ]
            ],
            "tvec": [
                [
                    0.118,
                    -0.089,
                    0.281
                ]
            ]
        },
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        },
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        },
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        }
    ],
    "box_on_box": True,
    "man_in_frame": True,
    "box_container_on_floor": False,
    "box_or_container_in_frame": True,
    "right_size_flags": True,
    "boxes_output": [
        {
            "box_id": 998,
            "placed_on_shelf_with_id": 4
        },
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        },
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        },
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        }
    ],
    "shelves": [
        {
            "shelf_id": 3,
            "x": -0.106,
            "y": 0.104,
            "occupied_by_box_with_id": -1,
            "pose": {
                "rvec": [
                    [
                        -2.915,
                        0.013,
                        -0.047
                    ]
                ],
                "tvec": [
                    [
                        -0.106,
                        0.104,
                        0.277
                    ]
                ]
            }
        },
        {
            "shelf_id": 4,
            "x": 0.228,
            "y": 0.103,
            "occupied_by_box_with_id": 998,
            "pose": {
                "rvec": [
                    [
                        -2.906,
                        0.015,
                        -0.035
                    ]
                ],
                "tvec": [
                    [
                        0.228,
                        0.103,
                        0.29
                    ]
                ]
            }
        }
    ],
    "graph_box_on_box": {
        "id_1": 998,
        "id_2": 0,
        "rel_id": 2,
        "class_name_1": "box",
        "rel_name": "on_top",
        "class_name_2": "box"
    }
}
test_case_1730300099546320364 = {
    "count_box_and_containers": 1,
    "scores": [
        0.966
    ],
    "classes_ids": [
        2
    ],
    "tracking_ids": [
        998
    ],
    "boxes": [
        {
            "x_min": 619,
            "y_min": 230,
            "x_max": 1037,
            "y_max": 540
        }
    ],
    "poses": [
        {
            "rvec": [
                [
                    -2.828,
                    -0.003,
                    -0.038
                ]
            ],
            "tvec": [
                [
                    0.072,
                    -0.11,
                    0.328
                ]
            ]
        }
    ],
    "box_on_box": False,
    "man_in_frame": True,
    "box_container_on_floor": False,
    "box_or_container_in_frame": True,
    "right_size_flags": True,
    "boxes_output": [
        {
            "box_id": 998,
            "placed_on_shelf_with_id": 5
        }
    ],
    "shelves": [
        {
            "shelf_id": 5,
            "x": 0.042,
            "y": 0.077,
            "occupied_by_box_with_id": 998,
            "pose": {
                "rvec": [
                    [
                        -2.826,
                        0.012,
                        -0.009
                    ]
                ],
                "tvec": [
                    [
                        0.042,
                        0.077,
                        0.363
                    ]
                ]
            }
        }
    ],
    "graph_box_on_box": None
}

test_case_wp0 = {
    "count_box_and_containers": 4,
    "scores": [
        0.912,
        0.881,
        0.88,
        0.876
    ],
    "classes_ids": [
        2,
        1,
        1,
        2
    ],
    "tracking_ids": [
        998,
        1,
        990,
        313
    ],
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
    "poses": [
        {
            "rvec": [
                [
                    -2.636,
                    0.217,
                    -1.21
                ]
            ],
            "tvec": [
                [
                    -0.703,
                    -0.28,
                    0.857
                ]
            ]
        },
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        },
        {
            "rvec": [
                [
                    -2.653,
                    0.067,
                    -0.725
                ]
            ],
            "tvec": [
                [
                    0.122,
                    -0.484,
                    1.543
                ]
            ]
        },
        {
            "rvec": [
                [
                    -2.787,
                    0.084,
                    -0.699
                ]
            ],
            "tvec": [
                [
                    -0.472,
                    -0.318,
                    1.064
                ]
            ]
        }
    ],
    "box_on_box": False,
    "man_in_frame": True,
    "box_container_on_floor": True,
    "box_or_container_in_frame": True,
    "right_size_flags": False,
    "boxes_output": [
        {
            "box_id": 998,
            "placed_on_shelf_with_id": 1
        },
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        },
        {
            "box_id": 990,
            "placed_on_shelf_with_id": 3
        },
        {
            "box_id": 313,
            "placed_on_shelf_with_id": 2
        }
    ],
    "shelves": [
        {
            "shelf_id": 3,
            "x": 0.107,
            "y": -0.297,
            "occupied_by_box_with_id": 990,
            "pose": {
                "rvec": [
                    [
                        -2.759,
                        0.178,
                        -0.921
                    ]
                ],
                "tvec": [
                    [
                        0.107,
                        -0.297,
                        1.569
                    ]
                ]
            }
        },
        {
            "shelf_id": 4,
            "x": 0.378,
            "y": -0.357,
            "occupied_by_box_with_id": -1,
            "pose": {
                "rvec": [
                    [
                        3.188,
                        -0.221,
                        1.085
                    ]
                ],
                "tvec": [
                    [
                        0.378,
                        -0.357,
                        1.756
                    ]
                ]
            }
        },
        {
            "shelf_id": 1,
            "x": -0.698,
            "y": -0.101,
            "occupied_by_box_with_id": 998,
            "pose": {
                "rvec": [
                    [
                        -2.962,
                        0.307,
                        -0.998
                    ]
                ],
                "tvec": [
                    [
                        -0.698,
                        -0.101,
                        0.92
                    ]
                ]
            }
        },
        {
            "shelf_id": 2,
            "x": -0.427,
            "y": -0.164,
            "occupied_by_box_with_id": 313,
            "pose": {
                "rvec": [
                    [
                        -2.711,
                        0.166,
                        -0.919
                    ]
                ],
                "tvec": [
                    [
                        -0.427,
                        -0.164,
                        1.126
                    ]
                ]
            }
        },
        {
            "shelf_id": 5,
            "x": 0.878,
            "y": -0.351,
            "occupied_by_box_with_id": -1,
            "pose": {
                "rvec": [
                    [
                        -2.967,
                        -0.106,
                        -0.009
                    ]
                ],
                "tvec": [
                    [
                        0.878,
                        -0.351,
                        1.754
                    ]
                ]
            }
        }
    ],
    "graph_box_on_box": None
}

test_case_wp1 = {
    "count_box_and_containers": 4,
    "scores": [
        0.949,
        0.867,
        0.762,
        0.513
    ],
    "classes_ids": [
        1,
        1,
        1,
        2
    ],
    "tracking_ids": [
        990,
        313,
        2,
        3
    ],
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
    "poses": [
        {
            "rvec": [
                [
                    -2.739,
                    0.01,
                    0.004
                ]
            ],
            "tvec": [
                [
                    0.327,
                    -0.081,
                    0.277
                ]
            ]
        },
        {
            "rvec": [
                [
                    -2.833,
                    0.021,
                    -0.188
                ]
            ],
            "tvec": [
                [
                    -0.112,
                    -0.079,
                    0.333
                ]
            ]
        },
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        },
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        }
    ],
    "box_on_box": False,
    "man_in_frame": True,
    "box_container_on_floor": False,
    "box_or_container_in_frame": True,
    "right_size_flags": False,
    "boxes_output": [
        {
            "box_id": 990,
            "placed_on_shelf_with_id": 2
        },
        {
            "box_id": 313,
            "placed_on_shelf_with_id": 1
        },
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        },
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        }
    ],
    "shelves": [
        {
            "shelf_id": 1,
            "x": -0.068,
            "y": 0.089,
            "occupied_by_box_with_id": 313,
            "pose": {
                "rvec": [
                    [
                        -2.874,
                        0.009,
                        -0.023
                    ]
                ],
                "tvec": [
                    [
                        -0.068,
                        0.089,
                        0.336
                    ]
                ]
            }
        },
        {
            "shelf_id": 2,
            "x": 0.273,
            "y": 0.087,
            "occupied_by_box_with_id": 990,
            "pose": {
                "rvec": [
                    [
                        -2.845,
                        0.044,
                        -0.004
                    ]
                ],
                "tvec": [
                    [
                        0.273,
                        0.087,
                        0.339
                    ]
                ]
            }
        }
    ],
    "graph_box_on_box": None
}

test_case_wp1_2box = {
    "count_box_and_containers": 5,
    "scores": [
        0.957,
        0.939,
        0.932,
        0.811,
        0.707
    ],
    "classes_ids": [
        2,
        1,
        2,
        1,
        1
    ],
    "tracking_ids": [
        998,
        999,
        0,
        2,
        4
    ],
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
    "poses": [
        {
            "rvec": [
                [
                    -2.869,
                    0.013,
                    -0.018
                ]
            ],
            "tvec": [
                [
                    -0.053,
                    -0.094,
                    0.29
                ]
            ]
        },
        {
            "rvec": [
                [
                    -2.781,
                    -0.001,
                    -0.019
                ]
            ],
            "tvec": [
                [
                    0.278,
                    -0.078,
                    0.319
                ]
            ]
        },
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        },
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        },
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        }
    ],
    "box_on_box": True,
    "man_in_frame": True,
    "box_container_on_floor": True,
    "box_or_container_in_frame": True,
    "right_size_flags": False,
    "boxes_output": [
        {
            "box_id": 998,
            "placed_on_shelf_with_id": 1
        },
        {
            "box_id": 999,
            "placed_on_shelf_with_id": 2
        },
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        },
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        },
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        }
    ],
    "shelves": [
        {
            "shelf_id": 1,
            "x": -0.068,
            "y": 0.089,
            "occupied_by_box_with_id": 998,
            "pose": {
                "rvec": [
                    [
                        -2.874,
                        0.009,
                        -0.023
                    ]
                ],
                "tvec": [
                    [
                        -0.068,
                        0.089,
                        0.336
                    ]
                ]
            }
        },
        {
            "shelf_id": 2,
            "x": 0.272,
            "y": 0.086,
            "occupied_by_box_with_id": 999,
            "pose": {
                "rvec": [
                    [
                        -2.844,
                        0.039,
                        0.003
                    ]
                ],
                "tvec": [
                    [
                        0.272,
                        0.086,
                        0.338
                    ]
                ]
            }
        }
    ],
    "graph_box_on_box": {
        "id_1": 998,
        "id_2": 0,
        "rel_id": 2,
        "class_name_1": "box",
        "rel_name": "on_top",
        "class_name_2": "box"
    }
}

test_case_wp2 = {
    "count_box_and_containers": 2,
    "scores": [
        0.95,
        0.945
    ],
    "classes_ids": [
        1,
        1
    ],
    "tracking_ids": [
        999,
        990
    ],
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
    "poses": [
        {
            "rvec": [
                [
                    -2.784,
                    0.001,
                    -0.037
                ]
            ],
            "tvec": [
                [
                    0.223,
                    -0.058,
                    0.262
                ]
            ]
        },
        {
            "rvec": [
                [
                    -2.771,
                    0.017,
                    -0.014
                ]
            ],
            "tvec": [
                [
                    -0.109,
                    -0.068,
                    0.235
                ]
            ]
        }
    ],
    "box_on_box": False,
    "man_in_frame": False,
    "box_container_on_floor": False,
    "box_or_container_in_frame": True,
    "right_size_flags": True,
    "boxes_output": [
        {
            "box_id": 999,
            "placed_on_shelf_with_id": 4
        },
        {
            "box_id": 990,
            "placed_on_shelf_with_id": 3
        }
    ],
    "shelves": [
        {
            "shelf_id": 3,
            "x": -0.105,
            "y": 0.104,
            "occupied_by_box_with_id": 990,
            "pose": {
                "rvec": [
                    [
                        -2.911,
                        0.012,
                        -0.048
                    ]
                ],
                "tvec": [
                    [
                        -0.105,
                        0.104,
                        0.277
                    ]
                ]
            }
        },
        {
            "shelf_id": 4,
            "x": 0.227,
            "y": 0.102,
            "occupied_by_box_with_id": 999,
            "pose": {
                "rvec": [
                    [
                        -2.898,
                        0.013,
                        -0.027
                    ]
                ],
                "tvec": [
                    [
                        0.227,
                        0.102,
                        0.29
                    ]
                ]
            }
        }
    ],
    "graph_box_on_box": None
}

test_case_wp3 = {
    "count_box_and_containers": 1,
    "scores": [
        0.532
    ],
    "classes_ids": [
        1
    ],
    "tracking_ids": [
        2
    ],
    "boxes": [
        {
            "x_min": 1395,
            "y_min": 682,
            "x_max": 1439,
            "y_max": 868
        }
    ],
    "poses": [
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        }
    ],
    "box_on_box": False,
    "man_in_frame": False,
    "box_container_on_floor": True,
    "box_or_container_in_frame": True,
    "right_size_flags": True,
    "boxes_output": [
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        }
    ],
    "shelves": [
        {
            "shelf_id": 5,
            "x": 0.042,
            "y": 0.076,
            "occupied_by_box_with_id": -1,
            "pose": {
                "rvec": [
                    [
                        -2.822,
                        0.003,
                        -0.014
                    ]
                ],
                "tvec": [
                    [
                        0.042,
                        0.076,
                        0.363
                    ]
                ]
            }
        }
    ],
    "graph_box_on_box": None
}
tests = [
    TestCase(
        name="test_case_1730299507052386690",
        request=SegAndTrackRequest(image_path=str(BASE_DIR / "1730299507052386690.png")),
        response=SegAndTrackResponse(**test_case_1730299507052386690),
    ),
    TestCase(
        name="test_case_1730299664277007982",
        request=SegAndTrackRequest(image_path=str(BASE_DIR / "1730299664277007982.png")),
        response=SegAndTrackResponse(**test_case_1730299664277007982),
    ),
    TestCase(
        name="test_case_1730299927324139623",
        request=SegAndTrackRequest(image_path=str(BASE_DIR / "1730299927324139623.png")),
        response=SegAndTrackResponse(**test_case_1730299927324139623),
    ),
    TestCase(
        name="test_case_1730299932262406396",
        request=SegAndTrackRequest(image_path=str(BASE_DIR / "1730299932262406396.png")),
        response=SegAndTrackResponse(**test_case_1730299932262406396),
    ),
    TestCase(
        name="test_case_1730300099546320364",
        request=SegAndTrackRequest(image_path=str(BASE_DIR / "1730300099546320364.png")),
        response=SegAndTrackResponse(**test_case_1730300099546320364),
    ),
    TestCase(
        name="test_case_wp0",
        request=SegAndTrackRequest(image_path=str(BASE_DIR / "wp0.png")),
        response=SegAndTrackResponse(**test_case_wp0),
    ),
    TestCase(
        name="test_case_wp1",
        request=SegAndTrackRequest(image_path=str(BASE_DIR / "wp1.png")),
        response=SegAndTrackResponse(**test_case_wp1),
    ),
    TestCase(
        name="test_case_wp1_2box",
        request=SegAndTrackRequest(image_path=str(BASE_DIR / "wp1_2box.png")),
        response=SegAndTrackResponse(**test_case_wp1_2box),
    ),
    TestCase(
        name="test_case_wp2",
        request=SegAndTrackRequest(image_path=str(BASE_DIR / "wp2.png")),
        response=SegAndTrackResponse(**test_case_wp2),
    ),
    TestCase(
        name="test_case_wp3",
        request=SegAndTrackRequest(image_path=str(BASE_DIR / "wp3.png")),
        response=SegAndTrackResponse(**test_case_wp3),
    ),
]

test_cases = {test_case.name: test_case for test_case in tests}
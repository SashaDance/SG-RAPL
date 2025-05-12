from pydantic.v1 import BaseModel as PydanticBaseModel
from langserve import RemoteRunnable
from langchain.output_parsers import PydanticOutputParser
from services_api.assistant import Telemetry


class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True


class Waypoint(BaseModel):
    waypoint_id: int
    name: str
    position: list[float]
    theta: float


class Shelf(BaseModel):
    shelf_id: int
    name: str
    position: list[float]
    orientation_rpy: list[float]
    height: float
    aruco_marker_id: int


class Box(BaseModel):
    box_id: int
    name: str
    placed_on_shelf_with_id: int
    position: list[float]
    orientation_rpy: list[float]
    aruco_marker_id: int
    color_rgb: list[int]


class WorldModel(BaseModel):
    waypoints: list[Waypoint]
    shelves: list[Shelf]
    boxes: list[Box]
    robot_start_position: list[float]
    robot_start_orientation: list[float]
    walls: list
    localization_markers: list


class RequestRetry(BaseModel):
    goal: str = ""
    telemetry: Telemetry = Telemetry()
    commands: list = []
    invalid_command_index: int = -1
    error_code: str = ""


class PlannerRequest(BaseModel):
    goal: str
    telemetry: Telemetry
    world_model: WorldModel
    retries: list[RequestRetry] = []
    max_retries: int = 5


class Action(BaseModel):
    name: str
    args: dict


class PlannerResponse(BaseModel):
    plan: list[Action] = []


model = RemoteRunnable("http://planner:8000")
chain = model | PydanticOutputParser(pydantic_object=PlannerResponse)

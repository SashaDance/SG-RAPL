from pydantic.v1 import BaseModel
from langserve import RemoteRunnable
from langchain.output_parsers import PydanticOutputParser
from services_api.planner import WorldModel, RequestRetry
from services_api.assistant import Telemetry

class ActualStateRequest(BaseModel):
    task: str = ""
    error_message: str = ""
    world_model: WorldModel
    plan_history: list[RequestRetry] = []

class ActualStateResponse(BaseModel):
    world_model: WorldModel
    telemetry: Telemetry = Telemetry()


model = RemoteRunnable("http://actual_state:8000")
chain = model | PydanticOutputParser(pydantic_object=ActualStateResponse)

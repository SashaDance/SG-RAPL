from fastapi import FastAPI
from langserve import add_routes

from llm_sorter.sorter_planner import get_planner_from_cfg, SorterPlanner

from src.langchain_api import PlannerAPI

app = FastAPI()

planner: SorterPlanner = get_planner_from_cfg(
    config_path="/app/packages/llm_sorter/config/", config_name="sorter_planner_in_container"
)

add_routes(app, PlannerAPI(planner=planner))

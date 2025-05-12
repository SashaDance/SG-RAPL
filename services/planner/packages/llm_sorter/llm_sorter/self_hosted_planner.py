from typing import List


import asyncio
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI
from contextlib import asynccontextmanager

from llm_sorter.sorter_planner import get_planner_from_cfg, SorterPlanner, Action, Request, Response

planner: SorterPlanner = get_planner_from_cfg(
    config_path="/app/packages/llm_sorter/config/", config_name="sorter_planner_in_container"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.ensure_future(planner.do_planning())
    yield
    pass


app = FastAPI(lifespan=lifespan)


class PostTask(BaseModel):
    goal: str


class PostFeedback(BaseModel):
    feedback: List[str]


@app.post("/predict")
def predict(input: Request) -> Response:
    answer = planner.process_task_sync(
        goal=input.goal, world_state=input.world_state, status=input.status, seg_track=input.seg_track
    )
    print(answer)

    return Response(plan=[Action(name=item["name"], args=item["args"]) for item in answer["plan"]])


@app.post("/add_task")
async def add_diff_task(task: PostTask):
    await planner.add_task(goal=task.goal)


@app.post("/process_task_sync")
def add_task(task: PostTask):
    llp_steps = planner.process_task_sync(goal=task.goal)
    return llp_steps


@app.post("/add_feedback")
async def add_feedback(feedback: PostFeedback):
    await planner.add_feedback(feedback=feedback.feedback)


@app.post("/add_llp_task")
async def add_llp_task(task: PostTask):
    await planner.add_llp_task(goal=task.goal)


@app.post("/reset")
async def reset():
    planner.reset()


@app.post("/valid_check")
async def valid_check(task: PostTask) -> bool:
    valid_check = await planner.valid_check(goal=task.goal)
    return valid_check


@app.get("/get_planner_output")
async def get_planner_output():
    return await planner.get_planner_output()


uvicorn.run(app, host="0.0.0.0", port=8082)

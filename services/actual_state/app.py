from fastapi import FastAPI
from langserve import add_routes
from src.base_state import ActualState
from src.langchain_api import ActualStateRunnable

app = FastAPI()

actual_state_instance = ActualState()

add_routes(app, ActualStateRunnable(actual_state_instance))

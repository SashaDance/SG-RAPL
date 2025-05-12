from langchain_core.runnables import Runnable
from src.base_state import ActualState
from services_api import actual_state
from typing import Any
import json

class ActualStateRunnable(Runnable):
    def __init__(self, actual_state: ActualState):
        self.actual_state = actual_state

    def invoke(self, new_state: actual_state.ActualStateRequest, *args: Any, **kwargs: Any): #**kwargs: Any
        #print(new_state)
        if isinstance(new_state, str):
            input_state = json.loads(new_state)
        elif isinstance(new_state, dict):
            input_state = new_state
        else:
            raise TypeError("new_state must be a JSON string or dictionary")

        task = input_state["task"]
        if task == "get":
            return self.actual_state.get()
        elif task == "update":
            return self.actual_state.update(new_state)

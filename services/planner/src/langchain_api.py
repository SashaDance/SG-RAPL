from typing import Any, Optional
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM

from llm_sorter.sorter_planner import SorterPlanner
from services_api import planner

CACHE = {}


class PlannerAPI(LLM):
    planner: SorterPlanner
    """The number of characters from the last message of the prompt to be echoed."""

    def _call(
        self,
        prompt: str,
        stop: Optional[list[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        # prompt = {"goal": "pick up box 73 from shelf 41", "world_state": {}, "status": {},
        #          "seg_track": {"objects":["box 73"]}}
        # prompt = {"goal": prompt.goal, "telemetry": json.dumps(prompt.telemetry), "world_model": json.dumps(prompt.world_model), "retries": [json.dumps(r) for r in prompt.retries], "max_retries": prompt.max_retries}
        if prompt not in CACHE:
            request = planner.PlannerRequest.parse_raw(prompt)
            response = planner.PlannerResponse(**self.planner.process_task_sync(request))
            CACHE[prompt] = response.json()
        return CACHE[prompt]

    @property
    def _identifying_params(self) -> dict[str, Any]:
        """Return a dictionary of identifying parameters."""
        return {"model_name": "planner"}

    @property
    def _llm_type(self) -> str:
        """Get the type of language model used by this chat model. Used for logging purposes only."""
        return "planner"

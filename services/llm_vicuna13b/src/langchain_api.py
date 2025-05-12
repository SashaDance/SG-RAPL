from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from services_api.llm_vicuna13b import Vicuna13BRequest, Vicuna13BResponse
from src.model import Vicuna13B
from typing import Any, Optional


class LLM_Vicuna13b(LLM):
    model: Vicuna13B

    def _call(
        self,
        prompt: str,
        stop: Optional[list[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        request = Vicuna13BRequest.parse_raw(prompt)
        response = Vicuna13BResponse(text=self.model.generate(request.prompt))
        return response.json()

    @property
    def _identifying_params(self) -> dict[str, Any]:
        """Return a dictionary of identifying parameters."""
        return {"model_name": "llm_vicuna13b"}

    @property
    def _llm_type(self) -> str:
        """Get the type of language model used by this chat model. Used for logging purposes only."""
        return "text generative model"

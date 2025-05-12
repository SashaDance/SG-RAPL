from typing import Any, Optional
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from services_api.seg_and_track import SegAndTrackRequest
from .seg_and_track import SegAndTrack

CACHE = {}


class SegAndTrackAPI(LLM):
    model: SegAndTrack
    """The number of characters from the last message of the prompt to be echoed."""

    def _call(
        self,
        prompt: str,
        stop: Optional[list[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        if prompt not in CACHE:
            try:
                segmentor_request = SegAndTrackRequest.parse_raw(prompt)

                response = self.model.get_response(segmentor_request.image_path)

                CACHE[prompt] = response.json()
            except Exception as e:
                raise ValueError(f"Error processing request: {e}")

        return CACHE[prompt]

    @property
    def _identifying_params(self) -> dict[str, Any]:
        """Return a dictionary of identifying parameters."""
        return {"model_name": "seg_and_track"}

    @property
    def _llm_type(self) -> str:
        """Get the type of language model used by this chat model. Used for logging purposes only."""
        return "seg_and_track"

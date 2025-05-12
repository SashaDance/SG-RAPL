from llm_sorter import WandbLogger
from llm_sorter.models import (
    BaseLLMModel,
    BaseModelInput,
    BaseModelOutput,
    ScoringInput,
    ScoringOutput,
)
from langserve import RemoteRunnable
from langchain.output_parsers import PydanticOutputParser
from services_api.llm_vicuna13b import Vicuna13BResponse, Vicuna13BRequest


class APIModel(BaseLLMModel):
    def __init__(
        self,
        logger: WandbLogger,
        name: str = "vicuna_13b docker",
        url: str = "http://llm_vicuna13b:8080",
    ) -> None:
        super().__init__(name=name, logger=logger)
        self._url = "http://llm_vicuna13b:8080"
        self.model = RemoteRunnable("http://llm_vicuna13b:8000")
        self.chain = self.model | PydanticOutputParser(pydantic_object=Vicuna13BResponse)

    def generate(self, inputs: BaseModelInput, **kwargs) -> BaseModelOutput:
        request = Vicuna13BRequest(prompt=inputs.text)
        response = self.chain.invoke(request.json())

        try:
            out = BaseModelOutput(response.text)
            return out
        except Exception as e:
            self._logger.info(f"Error: {e}")
            return BaseModelOutput("")

    def score_text(self, inputs: ScoringInput, **kwargs) -> ScoringOutput:
        pass

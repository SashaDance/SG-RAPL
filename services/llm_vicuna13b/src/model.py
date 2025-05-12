from src.base_model import BaseLLMModel
from transformers import pipeline
from fastchat.model.model_adapter import load_model
import torch


class Vicuna13B(BaseLLMModel):
    MODEL_NAME = "lmsys/vicuna-13b-v1.5"

    def __init__(
        self,
        name: str = "vicuna13b",
    ) -> None:
        self.max_new_tokens = 350
        self.num_gpus = 1
        super().__init__(name=name)
        self._load()

    def _load(self) -> None:
        self.model, self.tokenizer = load_model(
            model_path=self.MODEL_NAME,
            device="cuda",
            num_gpus=self.num_gpus,
            load_8bit=False,
            revision="main",
            debug=False,
        )
        self._prepare_for_generation()

    def _prepare_for_generation(self) -> None:
        self.generation_pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=torch.cuda.current_device(),
        )

    def generate(self, prompt: str, **kwargs) -> str:
        output = self.generation_pipeline(
            prompt,
            do_sample=False,
            return_full_text=False,
            max_new_tokens=self.max_new_tokens,
        )[0]["generated_text"]
        return output

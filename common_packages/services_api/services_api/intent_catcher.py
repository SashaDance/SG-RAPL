from typing import Optional

from pydantic.v1 import BaseModel, Field
from langserve import RemoteRunnable
from langchain.output_parsers import PydanticOutputParser


class Tag(BaseModel):
    name: str
    selection_mode: str


class Intent(BaseModel):
    name: str
    phrases: list[str]
    reg_phrases: list[str]
    min_precision: float
    punctuation: list[str] = []
    tags: list[str] = []


class PredictedIntent(BaseModel):
    name: str
    scope: str = ""
    rule_confidence: float
    rule_match: bool
    rule_support_reference: str = ""
    semantic_confidence: float
    semantic_match: bool
    semantic_support_reference: str = ""


class IntentCatcherRequest(BaseModel):
    intent_catcher_request: str = Field(..., alias="intent_catcher_request")


class IntentCatcherResponse(BaseModel):
    intent_catcher_response: list[PredictedIntent] = Field(..., alias="intent_catcher_response")

    def detected_intents(
        self, rule_match: bool = True, semantic_match: bool = True, scope: Optional[str] = None, confidence_threshold=0
    ) -> dict[str, PredictedIntent]:
        assert rule_match or semantic_match
        intents = {}
        for intent in self.intent_catcher_response:
            if scope and intent.scope != scope:
                continue
            if rule_match and intent.rule_match and intent.rule_confidence >= confidence_threshold:
                intents[intent.name] = intent
        for intent in self.intent_catcher_response:
            if scope and intent.scope != scope:
                continue
            if semantic_match and intent.semantic_match and intent.semantic_confidence >= confidence_threshold:
                intents[intent.name] = intent
        return intents

    def intent_names(self) -> list[str]:
        return [intent.name for intent in self.intent_catcher_response]

    def is_detected_intent(self, intent_name: str) -> bool:
        assert intent_name in self.intent_names, f"intent {intent_name} not in {self.intent_names}"
        return intent_name in self.detected_intents()

    def detected_intents_num(self) -> int:
        return len(self.detected_intents())


model = RemoteRunnable("http://intent_catcher:8000")
chain = model | PydanticOutputParser(pydantic_object=IntentCatcherResponse)

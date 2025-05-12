from pydantic.v1 import BaseModel, Field
from langserve import RemoteRunnable
from langchain.output_parsers import PydanticOutputParser


class TranslationRequest(BaseModel):
    translation_request: str = Field(None, alias="translation_request")


class TranslationResponse(BaseModel):
    translation_response: str = Field(None, alias="translation_response")


model = RemoteRunnable("http://machine_translation:8000/ru2en")
ru2en_chain = model | PydanticOutputParser(pydantic_object=TranslationResponse)

model = RemoteRunnable("http://machine_translation:8000/en2ru")
en2ru_chain = model | PydanticOutputParser(pydantic_object=TranslationResponse)

from pydantic.v1 import BaseModel
from langserve import RemoteRunnable
from langchain.output_parsers import PydanticOutputParser


class Vicuna13BRequest(BaseModel):
    prompt: str


class Vicuna13BResponse(BaseModel):
    text: str


model = RemoteRunnable("http://localhost:8000")
chain = model | PydanticOutputParser(pydantic_object=Vicuna13BResponse)

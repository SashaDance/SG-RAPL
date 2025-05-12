from pydantic.v1 import BaseModel
from langserve import RemoteRunnable
from langchain.output_parsers import PydanticOutputParser


class GigachatRequest(BaseModel):
    text: str


class GigachatResponse(BaseModel):
    text: str
    stop_reason: str  # enum # blacklist


model = RemoteRunnable("http://gigachat:8000")
chain = model | PydanticOutputParser(pydantic_object=GigachatResponse)

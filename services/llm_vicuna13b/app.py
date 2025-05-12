from fastapi import FastAPI
from src.model import Vicuna13B
from langserve import add_routes
from src.langchain_api import LLM_Vicuna13b

app = FastAPI()

model = Vicuna13B()

add_routes(app, LLM_Vicuna13b(model=model))

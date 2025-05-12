from fastapi import FastAPI
from langserve import add_routes
from .src.seg_and_track import SegAndTrack
from .src.langchain_api import SegAndTrackAPI

app = FastAPI()

segmentor = SegAndTrack()

add_routes(app, SegAndTrackAPI(model=segmentor))

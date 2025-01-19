from fastapi import APIRouter, status
from app.schemas import ChatRequest
from fastapi.responses import JSONResponse
from app.services import get_text
from app.results import results
import json

router = APIRouter()


@router.get("/")
async def index():
    return "connected"


@router.get("/get_results")
async def get_patient():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"data": results}
    )


@router.post("/chat")
async def chat(chat_request: ChatRequest):
    text = get_text(chat_request)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"text": text}
    )

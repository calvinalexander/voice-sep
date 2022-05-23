from fastapi import APIRouter

from app.api import audio

router = APIRouter()

router.include_router(audio.router, tags=["audios"], prefix="/audios")

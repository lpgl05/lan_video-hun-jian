from fastapi import APIRouter, File, UploadFile
from services.upload_service import handle_upload_video, handle_upload_audio

router = APIRouter()

@router.post("/api/upload/video")
async def upload_video(video: UploadFile = File(...)):
    return await handle_upload_video(video)

@router.post("/api/upload/audio")
async def upload_audio(audio: UploadFile = File(...)):
    return await handle_upload_audio(audio)

from fastapi import APIRouter, File, UploadFile
from services.upload_service import handle_upload_video, handle_upload_audio, handle_upload_poster

router = APIRouter()

@router.post("/upload/video")
async def upload_video(video: UploadFile = File(...)):
    return await handle_upload_video(video)

@router.post("/upload/audio")
async def upload_audio(audio: UploadFile = File(...)):
    return await handle_upload_audio(audio)

@router.post("/upload/poster")
async def upload_poster(poster: UploadFile = File(...)):
    return await handle_upload_poster(poster)

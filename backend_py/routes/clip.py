from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from services.clip_service import process_clips

router = APIRouter()

class VideoFile(BaseModel):
    id: str
    name: str
    url: str
    size: int
    duration: int
    uploadedAt: str

class AudioFile(BaseModel):
    id: str
    name: str
    url: str
    size: int
    duration: int
    uploadedAt: str

class Script(BaseModel):
    id: str
    content: str
    selected: bool
    generatedAt: str

class StyleConfig(BaseModel):
    title: Dict[str, Any]
    subtitle: Dict[str, Any]

class ClipRequest(BaseModel):
    name: str
    videos: List[VideoFile]
    audios: List[AudioFile]
    scripts: List[Script]
    duration: str
    videoCount: int
    voice: str
    style: StyleConfig

@router.post("/api/clip")
async def clip_video(req: ClipRequest):
    result = await process_clips(req)
    return result

from fastapi import APIRouter, Request
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime
from services.ai_service import generate_scripts_service

router = APIRouter()

class Script(BaseModel):
    id: str
    content: str
    selected: bool = False
    generatedAt: datetime

class GenerateScriptsRequest(BaseModel):
    base_script: str
    video_duration: int
    video_count: int

class GenerateRequest(BaseModel):
    script: str
    duration: int
    count: int = 3

@router.post("/ai/generate-scripts")
async def generate_scripts(req: GenerateScriptsRequest):
    if not req.base_script.strip():
        return {"success": False, "error": "请输入基础文案"}
    if req.video_duration <= 0 or req.video_count <= 0:
        return {"success": False, "error": "视频时长和数量必须大于0"}
    return await generate_scripts_service(req.base_script.strip(), req.video_duration, req.video_count)

@router.post("/ai/generate")
async def generate_ai_content(req: GenerateRequest):
    """AI文案生成端点"""
    if not req.script.strip():
        return {"success": False, "error": "请输入基础文案"}
    if req.duration <= 0:
        return {"success": False, "error": "视频时长必须大于0"}
    return await generate_scripts_service(req.script.strip(), req.duration, req.count)
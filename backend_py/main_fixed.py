from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import json
import aiohttp
import asyncio
from services.ai_service import generate_scripts_service

app = FastAPI(title="Video Generation API", version="1.0.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class VideoFile(BaseModel):
    url: str
    filename: str

class AudioFile(BaseModel):
    url: str
    filename: str

class Script(BaseModel):
    content: str
    duration: int

class ProjectRequest(BaseModel):
    name: str
    videos: List[str]  # URL列表
    audios: List[str]  # URL列表
    scripts: List[str]  # 文案列表
    duration: int
    videoCount: int
    voice: str = "female"
    style: str = "modern"

class GenerateRequest(BaseModel):
    script: str
    duration: int
    count: int = 3

# 存储项目数据
projects_db = {}

@app.get("/")
async def root():
    return {"message": "Video Generation API is running"}

@app.get("/api/ping")
async def ping():
    return {"message": "pong"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/ai/generate")
async def generate_ai_content(req: GenerateRequest):
    """AI文案生成端点"""
    try:
        if not req.script.strip():
            return JSONResponse(
                content={"success": False, "error": "请输入基础文案"},
                media_type="application/json; charset=utf-8"
            )
        if req.duration <= 0:
            return JSONResponse(
                content={"success": False, "error": "视频时长必须大于0"},
                media_type="application/json; charset=utf-8"
            )
        
        # 调用AI服务生成文案
        result = await generate_scripts_service(req.script, req.duration, req.count)
        return JSONResponse(
            content=result,
            media_type="application/json; charset=utf-8"
        )
        
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": f"AI生成失败: {str(e)}"},
            media_type="application/json; charset=utf-8"
        )

@app.post("/api/projects")
async def create_project(project: ProjectRequest):
    """创建项目"""
    try:
        project_id = str(uuid.uuid4())
        
        # 转换数据格式
        video_files = [VideoFile(url=url, filename=f"video_{i}.mp4") for i, url in enumerate(project.videos)]
        audio_files = [AudioFile(url=url, filename=f"audio_{i}.mp3") for i, url in enumerate(project.audios)]
        script_files = [Script(content=script, duration=project.duration) for script in project.scripts]
        
        project_data = {
            "id": project_id,
            "name": project.name,
            "videos": [v.dict() for v in video_files],
            "audios": [a.dict() for a in audio_files],
            "scripts": [s.dict() for s in script_files],
            "duration": project.duration,
            "videoCount": project.videoCount,
            "voice": project.voice,
            "style": project.style,
            "status": "created"
        }
        
        projects_db[project_id] = project_data
        
        return {
            "success": True,
            "project_id": project_id,
            "message": "项目创建成功",
            "data": project_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建项目失败: {str(e)}")

@app.get("/api/projects/{project_id}")
async def get_project(project_id: str):
    """获取项目信息"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    return {
        "success": True,
        "data": projects_db[project_id]
    }

@app.post("/api/projects/{project_id}/generate")
async def generate_video(project_id: str):
    """生成视频"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    # 模拟视频生成过程
    projects_db[project_id]["status"] = "generating"
    
    # 这里可以添加实际的视频生成逻辑
    await asyncio.sleep(1)  # 模拟处理时间
    
    projects_db[project_id]["status"] = "completed"
    projects_db[project_id]["output_video"] = f"http://127.0.0.1:8001/api/download/video/{project_id}.mp4"
    
    return {
        "success": True,
        "message": "视频生成完成",
        "data": projects_db[project_id]
    }

@app.get("/api/download/video/{filename}")
async def download_video(filename: str):
    """下载视频文件"""
    # 这里可以返回实际的视频文件或重定向到OSS
    return {"message": f"视频下载: {filename}", "url": f"https://example.com/videos/{filename}"}

@app.get("/api/download/audio/{filename}")
async def download_audio(filename: str):
    """下载音频文件"""
    # 这里可以返回实际的音频文件或重定向到OSS
    return {"message": f"音频下载: {filename}", "url": f"https://example.com/audios/{filename}"}

# 测试文件端点
@app.get("/test_video.mp4")
async def get_test_video():
    return {"message": "测试视频文件", "url": "https://tian-jiu-video.oss-cn-beijing.aliyuncs.com/uploads/test-video.mp4"}

@app.get("/test_audio.mp3")
async def get_test_audio():
    return {"message": "测试音频文件", "url": "https://tian-jiu-video.oss-cn-beijing.aliyuncs.com/uploads/test-audio.mp3"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
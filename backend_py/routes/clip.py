import asyncio
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any
from services.clip_service import process_clips, process_clips001, process_clips_optimized
from uuid import uuid4
from datetime import datetime

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

class PosterFile(BaseModel):
    id: str
    name: str
    url: str
    size: int
    width: int
    height: int
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
    posters: List[PosterFile]
    scripts: List[Script]
    duration: str
    videoCount: int
    voice: str
    style: StyleConfig

class StartGenerationRequest(BaseModel):
    projectId: str
    # 移除 clipRequest 字段，改为从项目存储中获取

# 添加全局变量存储最新生成的视频
_latest_generated_videos = []

# 任务状态存储（生产环境建议用Redis）
_task_storage = {}

# 添加项目存储
_project_storage = {}

@router.post("/api/projects")
async def save_project_and_generate(req: ClipRequest, background_tasks: BackgroundTasks):
    # 保存项目配置到内存存储
    project_id = str(uuid4())
    _project_storage[project_id] = req
    
    return {
        "success": True,
        "data": {
            "id": project_id,
            "name": req.name,
            "videos": [v.dict() for v in req.videos],
            "audios": [a.dict() for a in req.audios],
            "scripts": [s.dict() for s in req.scripts],
            "duration": req.duration,
            "videoCount": req.videoCount,
            "voice": req.voice,
            "style": req.style.dict(),
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat()
        }
    }

@router.post("/api/generation/start")
async def start_generation(req: StartGenerationRequest, background_tasks: BackgroundTasks):
    # 创建任务ID，立即返回processing状态
    task_id = str(uuid4())
    
    # 从项目存储中获取配置
    if req.projectId not in _project_storage:
        return {
            "success": False,
            "error": f"项目 {req.projectId} 不存在"
        }
    
    clip_req = _project_storage[req.projectId]
    
    # 初始化任务状态
    _task_storage[task_id] = {
        "id": task_id,
        "projectId": req.projectId,
        "status": "processing",
        "progress": 0,
        "result": None,
        "error": None,
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    
    # 在后台异步处理视频剪辑
    background_tasks.add_task(process_video_generation, task_id, clip_req)
    
    return {
        "success": True,
        "data": _task_storage[task_id]
    }

async def process_video_generation(task_id: str, clip_req: ClipRequest):
    """后台异步处理视频生成"""
    start_time = datetime.now()
    try:
        # 1. 初始化任务
        _task_storage[task_id]["progress"] = 5
        _task_storage[task_id]["updatedAt"] = datetime.now().isoformat()
        _task_storage[task_id]["startTime"] = start_time.isoformat()
        
        # 2. 开始处理视频
        _task_storage[task_id]["progress"] = 20
        _task_storage[task_id]["updatedAt"] = datetime.now().isoformat()
        
        # 3. 执行视频剪辑处理
        _task_storage[task_id]["progress"] = 30
        
        # 调试：打印样式配置
        print("=== 调试字体配置 ===")
        print(f"收到的样式配置: {clip_req.style}")
        if hasattr(clip_req.style, 'title'):
            print(f"标题样式: {clip_req.style.title}")
        if hasattr(clip_req.style, 'subtitle'):
            print(f"字幕样式: {clip_req.style.subtitle}")
        print("==================")
        # 🎯 智能选择处理模式：基于创作模式和功能需求
        style_dict = clip_req.style.dict() if hasattr(clip_req.style, "dict") else clip_req.style
        creation_mode = style_dict.get("creationMode", "personal")  # 默认个人创作模式
        has_poster = hasattr(clip_req, 'posters') and clip_req.posters and len(clip_req.posters) > 0
        
        print(f"🎯 创作模式: {'👤 个人创作' if creation_mode == 'personal' else '👥 团队协作'}")
        
        # 🚀 智能选择处理模式
        if creation_mode == "personal":
            # 个人创作模式：优先使用本地处理（未来实现）
            if has_poster:
                print("🎬 个人模式+海报：使用高级处理（PNG动态字幕）")
                result = await process_clips001(clip_req)
            else:
                print("🚀 个人模式：使用优化处理（ASS字幕 + 智能缓存）")
                result = await process_clips_optimized(clip_req)
        else:
            # 团队协作模式：使用OSS云端处理
            if has_poster:
                print("🎬 团队模式+海报：使用高级处理（PNG动态字幕）")
                result = await process_clips001(clip_req)
            else:
                print("🚀 团队模式：使用优化处理（ASS字幕 + 智能缓存）")
                result = await process_clips_optimized(clip_req)
        
        # 4. 处理完成，上传中
        _task_storage[task_id]["progress"] = 90
        _task_storage[task_id]["updatedAt"] = datetime.now().isoformat()
        
        if result.get("success"):
            # 5. 完成 - 计算耗时
            end_time = datetime.now()
            duration_seconds = (end_time - start_time).total_seconds()
            duration_minutes = duration_seconds / 60
            
            _task_storage[task_id].update({
                "status": "completed",
                "progress": 100,
                "result": {
                    "videos": [video["url"] for video in result["videos"]],
                    "previewUrl": result["videos"][0]["url"] if result["videos"] else None
                },
                "updatedAt": end_time.isoformat(),
                "endTime": end_time.isoformat(),
                "durationSeconds": round(duration_seconds, 1),
                "durationMinutes": round(duration_minutes, 1)
            })
            print(f"任务 {task_id} 成功完成，耗时 {duration_minutes:.1f} 分钟")
        else:
            # 失败处理 - 也计算耗时
            end_time = datetime.now()
            duration_seconds = (end_time - start_time).total_seconds()
            duration_minutes = duration_seconds / 60
            
            error_msg = result.get("error", "处理失败")
            print(f"任务 {task_id} 处理失败: {error_msg}，耗时 {duration_minutes:.1f} 分钟")
            _task_storage[task_id].update({
                "status": "failed",
                "progress": 0,
                "error": error_msg,
                "updatedAt": end_time.isoformat(),
                "endTime": end_time.isoformat(),
                "durationSeconds": round(duration_seconds, 1),
                "durationMinutes": round(duration_minutes, 1)
            })
            
    except Exception as e:
        # 异常处理 - 也计算耗时
        end_time = datetime.now()
        duration_seconds = (end_time - start_time).total_seconds()
        duration_minutes = duration_seconds / 60
        
        error_msg = str(e)
        print(f"任务 {task_id} 异常: {error_msg}，耗时 {duration_minutes:.1f} 分钟")
        _task_storage[task_id].update({
            "status": "failed",
            "progress": 0,
            "error": error_msg,
            "updatedAt": end_time.isoformat(),
            "endTime": end_time.isoformat(),
            "durationSeconds": round(duration_seconds, 1),
            "durationMinutes": round(duration_minutes, 1)
        })

@router.get("/api/generation/status/{task_id}")
async def get_generation_status(task_id: str):
    # 从存储中获取任务状态
    if task_id not in _task_storage:
        return {
            "success": False,
            "error": "任务不存在"
        }
    
    return {
        "success": True,
        "data": _task_storage[task_id]
    }
import asyncio
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any
from services.clip_service import process_clips001, process_clips_optimized
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

# 🚀 新增：任务队列控制
_task_queue = asyncio.Queue()  # 任务队列
_is_processing = False  # 是否有任务正在处理
_queue_processor_started = False  # 队列处理器是否已启动

async def start_queue_processor():
    """启动队列处理器 - 确保同一时间只处理一个任务"""
    global _is_processing, _queue_processor_started
    
    if _queue_processor_started:
        return
    
    _queue_processor_started = True
    print("🚀 启动任务队列处理器...")
    
    while True:
        try:
            # 从队列中获取任务
            task_data = await _task_queue.get()
            task_id = task_data['task_id']
            clip_req = task_data['clip_req']
            
            print(f"📋 开始处理队列任务: {task_id}")
            _is_processing = True
            
            # 更新任务状态为处理中
            if task_id in _task_storage:
                _task_storage[task_id]["status"] = "processing"
                _task_storage[task_id]["progress"] = 10
                _task_storage[task_id]["updatedAt"] = datetime.now().isoformat()
            
            # 执行实际的视频生成任务
            await process_video_generation(task_id, clip_req)
            
            print(f"✅ 队列任务完成: {task_id}")
            
        except Exception as e:
            print(f"❌ 队列处理器异常: {e}")
            if task_id in _task_storage:
                _task_storage[task_id]["status"] = "failed"
                _task_storage[task_id]["error"] = f"队列处理异常: {str(e)}"
                _task_storage[task_id]["updatedAt"] = datetime.now().isoformat()
        finally:
            _is_processing = False
            _task_queue.task_done()

# 保存项目配置
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

# 开始生成
@router.post("/api/generation/start")
async def start_generation(req: StartGenerationRequest, background_tasks: BackgroundTasks):
    # 启动队列处理器（如果尚未启动）
    if not _queue_processor_started:
        background_tasks.add_task(start_queue_processor)
    
    # 创建任务ID
    task_id = str(uuid4())
    
    # 从项目存储中获取配置
    if req.projectId not in _project_storage:
        return {
            "success": False,
            "error": f"项目 {req.projectId} 不存在"
        }
    
    clip_req = _project_storage[req.projectId]
    
    # 获取当前队列状态
    queue_size = _task_queue.qsize()
    queue_position = queue_size + 1 if not _is_processing else queue_size + 2
    
    # 初始化任务状态
    _task_storage[task_id] = {
        "id": task_id,
        "projectId": req.projectId,
        "status": "queued" if _is_processing or queue_size > 0 else "processing",
        "progress": 0,
        "result": None,
        "error": None,
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat(),
        "queuePosition": queue_position,
        "queueSize": queue_size + 1
    }
    
    # 将任务加入队列
    await _task_queue.put({
        'task_id': task_id,
        'clip_req': clip_req
    })
    
    # 返回任务信息
    status_msg = "已加入处理队列" if _is_processing or queue_size > 0 else "开始处理"
    
    print(f"📝 新任务 {task_id}: {status_msg}")
    print(f"   队列状态: 队列中{queue_size + 1}个任务, 排队位置#{queue_position}")
    print(f"   正在处理: {'是' if _is_processing else '否'}")
    
    return {
        "success": True,
        "data": {
            **_task_storage[task_id],
            "message": status_msg,
            "estimatedWaitTime": f"预计等待 {queue_position * 3} 分钟" if queue_position > 1 else "正在处理中"
        }
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
        
        # 🎯 统一使用团队协作模式处理
        style_dict = clip_req.style.dict() if hasattr(clip_req.style, "dict") else clip_req.style
        has_poster = hasattr(clip_req, 'posters') and clip_req.posters and len(clip_req.posters) > 0
        
        print(f"🎯 统一团队协作模式")
        
        # 🚀 根据功能需求选择处理模式
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
            print(f"✅ 任务 {task_id} 成功完成，耗时 {duration_minutes:.1f} 分钟")
        else:
            # 失败处理 - 也计算耗时
            end_time = datetime.now()
            duration_seconds = (end_time - start_time).total_seconds()
            duration_minutes = duration_seconds / 60
            
            error_msg = result.get("error", "处理失败")
            print(f"❌ 任务 {task_id} 处理失败: {error_msg}，耗时 {duration_minutes:.1f} 分钟")
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
        print(f"💥 任务 {task_id} 异常: {error_msg}，耗时 {duration_minutes:.1f} 分钟")
        _task_storage[task_id].update({
            "status": "failed",
            "progress": 0,
            "error": error_msg,
            "updatedAt": end_time.isoformat(),
            "endTime": end_time.isoformat(),
            "durationSeconds": round(duration_seconds, 1),
            "durationMinutes": round(duration_minutes, 1)
        })

# 获取任务状态
@router.get("/api/generation/status/{task_id}")
async def get_generation_status(task_id: str):
    # 从存储中获取任务状态
    if task_id not in _task_storage:
        return {
            "success": False,
            "error": "任务不存在"
        }
    
    task_data = _task_storage[task_id].copy()
    
    # 添加队列状态信息
    if task_data["status"] == "queued":
        current_queue_size = _task_queue.qsize()
        task_data["currentQueueSize"] = current_queue_size
        task_data["estimatedWaitTime"] = f"预计等待 {current_queue_size * 3} 分钟"
    
    return {
        "success": True,
        "data": task_data
    }

# 新增：获取队列状态的接口
@router.get("/api/generation/queue/status")
async def get_queue_status():
    """获取当前队列状态"""
    queue_size = _task_queue.qsize()
    
    # 统计各状态的任务数量
    queued_tasks = [t for t in _task_storage.values() if t.get("status") == "queued"]
    processing_tasks = [t for t in _task_storage.values() if t.get("status") == "processing"]
    completed_tasks = [t for t in _task_storage.values() if t.get("status") == "completed"]
    failed_tasks = [t for t in _task_storage.values() if t.get("status") == "failed"]
    
    return {
        "success": True,
        "data": {
            "queueSize": queue_size,
            "isProcessing": _is_processing,
            "statistics": {
                "queued": len(queued_tasks),
                "processing": len(processing_tasks),
                "completed": len(completed_tasks),
                "failed": len(failed_tasks),
                "total": len(_task_storage)
            },
            "estimatedWaitTime": f"新任务预计等待 {(queue_size + 1) * 3} 分钟" if queue_size > 0 or _is_processing else "可立即处理"
        }
    }
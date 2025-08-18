from fastapi import APIRouter, File, UploadFile, HTTPException
from services.upload_service import handle_upload_video, handle_upload_audio, handle_upload_poster, upload_tasks

router = APIRouter()

@router.post("/api/upload/video")
async def upload_video(video: UploadFile = File(...)):
    print('sssssssssssssssssssssssssssssssssssssssssssssssss')
    return await handle_upload_video(video)

@router.post("/api/upload/audio")
async def upload_audio(audio: UploadFile = File(...)):
    return await handle_upload_audio(audio)

@router.post("/api/upload/poster")
async def upload_poster(poster: UploadFile = File(...)):
    return await handle_upload_poster(poster)

@router.get("/api/upload/progress/{task_id}")
async def get_upload_progress(task_id: str):
    """获取上传进度"""
    print(f"查询进度: task_id={task_id}")
    print(f"当前所有任务: {list(upload_tasks.keys())}")
    
    if task_id not in upload_tasks:
        print(f"任务不存在: {task_id}")
        raise HTTPException(status_code=404, detail="任务不存在")
    
    task = upload_tasks[task_id]
    print(f"返回任务状态: {task}")
    return {
        "success": True,
        "data": {
            "task_id": task_id,
            "status": task["status"],
            "progress": task["progress"],
            "speed": task["speed"],
            "filename": task["filename"],
            "file_size": task["file_size"],
            "uploaded_bytes": task["uploaded_bytes"],
            "error": task.get("error")
        }
    }

# 移除调试接口，不再需要复杂的轮询
# @router.get("/api/upload/debug/tasks")
# async def debug_all_tasks():
#     """调试：查看所有上传任务"""
#     return {"success": True, "data": []}

from fastapi import APIRouter, File, UploadFile
import os
from uuid import uuid4
from datetime import datetime

router = APIRouter()

UPLOAD_DIR = "uploads/videos"
USE_OSS = False  # 切换为 True 即可上传到 OSS

# OSS 配置（仅当 USE_OSS=True 时生效）
OSS_ACCESS_KEY_ID = "你的AccessKeyId"
OSS_ACCESS_KEY_SECRET = "你的AccessKeySecret"
OSS_BUCKET_NAME = "你的BucketName"
OSS_ENDPOINT = "你的Endpoint"

@router.post("/api/upload/video")
async def upload_video(video: UploadFile = File(...)):    
    if video is None:
        return {"success": False, "error": "未收到文件"}
    
    try:
        file_id = str(uuid4())
        file_name = video.filename
        content = await video.read()
        
        if not content:
            return {"success": False, "error": "文件内容为空"}
        
        if USE_OSS:
            # 上传到阿里云 OSS
            import oss2
            auth = oss2.Auth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET_NAME)
            oss_path = f"videos/{file_name}"
            bucket.put_object(oss_path, content)
            file_url = f"https://{OSS_BUCKET_NAME}.{OSS_ENDPOINT.replace('https://', '').replace('http://', '')}/{oss_path}"
        else:
            # 保存到本地
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            save_path = os.path.join(UPLOAD_DIR, file_name)
            with open(save_path, "wb") as f:
                f.write(content)
            file_url = f"/uploads/videos/{file_name}"
        
        # 构造符合前端期望的VideoFile格式
        video_file = {
            "id": file_id,
            "name": file_name,
            "url": file_url,
            "size": len(content),
            "duration": 0,  # 需要视频处理库获取实际时长
            "uploadedAt": datetime.now().isoformat()
        }
        
        return {
            "success": True, 
            "data": video_file,
            "message": "文件上传成功"
        }
        
    except Exception as e:
        return {"success": False, "error": f"上传失败: {str(e)}"}


@router.post("/api/upload/audio")
async def upload_audio(audio: UploadFile = File(...)):
    if audio is None:
        return {"success": False, "error": "未收到文件"}

    try:
        file_id = str(uuid4())
        file_name = audio.filename
        content = await audio.read()

        if not content:
            return {"success": False, "error": "文件内容为空"}

        if USE_OSS:
            # 上传到阿里云 OSS
            import oss2
            auth = oss2.Auth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET_NAME)
            oss_path = f"audios/{file_name}"
            bucket.put_object(oss_path, content)
            file_url = f"https://{OSS_BUCKET_NAME}.{OSS_ENDPOINT.replace('https://', '').replace('http://', '')}/{oss_path}"
        else:
            # 保存到本地
            audio_dir = "uploads/audios"
            os.makedirs(audio_dir, exist_ok=True)
            save_path = os.path.join(audio_dir, file_name)
            with open(save_path, "wb") as f:
                f.write(content)
            file_url = f"/uploads/audios/{file_name}"

        audio_file = {
            "id": file_id,
            "name": file_name,
            "url": file_url,
            "size": len(content),
            "duration": 0,  # 需要音频处理库获取实际时长
            "uploadedAt": datetime.now().isoformat()
        }

        return {
            "success": True,
            "data": audio_file,
            "message": "文件上传成功"
        }

    except Exception as e:
        return {"success": False, "error": f"上传失败: {str(e)}"}

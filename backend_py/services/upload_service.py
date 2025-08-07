import os
from uuid import uuid4
from datetime import datetime

UPLOAD_DIR = "uploads/videos"
AUDIO_DIR = "uploads/audios"
USE_OSS = False  # 切换为 True 即可上传到 OSS

# OSS 配置（仅当 USE_OSS=True 时生效）
OSS_ACCESS_KEY_ID = "你的AccessKeyId"
OSS_ACCESS_KEY_SECRET = "你的AccessKeySecret"
OSS_BUCKET_NAME = "你的BucketName"
OSS_ENDPOINT = "你的Endpoint"

async def handle_upload_video(video):
    if video is None:
        return {"success": False, "error": "未收到文件"}
    try:
        file_id = str(uuid4())
        file_name = video.filename
        content = await video.read()
        if not content:
            return {"success": False, "error": "文件内容为空"}
        if USE_OSS:
            import oss2
            auth = oss2.Auth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET_NAME)
            oss_path = f"videos/{file_name}"
            bucket.put_object(oss_path, content)
            file_url = f"https://{OSS_BUCKET_NAME}.{OSS_ENDPOINT.replace('https://', '').replace('http://', '')}/{oss_path}"
        else:
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            save_path = os.path.join(UPLOAD_DIR, file_name)
            with open(save_path, "wb") as f:
                f.write(content)
            file_url = f"/uploads/videos/{file_name}"
        video_file = {
            "id": file_id,
            "name": file_name,
            "url": file_url,
            "size": len(content),
            "duration": 0,
            "uploadedAt": datetime.now().isoformat()
        }
        return {
            "success": True,
            "data": video_file,
            "message": "文件上传成功"
        }
    except Exception as e:
        return {"success": False, "error": f"上传失败: {str(e)}"}

async def handle_upload_audio(audio):
    if audio is None:
        return {"success": False, "error": "未收到文件"}
    try:
        file_id = str(uuid4())
        file_name = audio.filename
        content = await audio.read()
        if not content:
            return {"success": False, "error": "文件内容为空"}
        if USE_OSS:
            import oss2
            auth = oss2.Auth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET_NAME)
            oss_path = f"audios/{file_name}"
            bucket.put_object(oss_path, content)
            file_url = f"https://{OSS_BUCKET_NAME}.{OSS_ENDPOINT.replace('https://', '').replace('http://', '')}/{oss_path}"
        else:
            os.makedirs(AUDIO_DIR, exist_ok=True)
            save_path = os.path.join(AUDIO_DIR, file_name)
            with open(save_path, "wb") as f:
                f.write(content)
            file_url = f"/uploads/audios/{file_name}"
        audio_file = {
            "id": file_id,
            "name": file_name,
            "url": file_url,
            "size": len(content),
            "duration": 0,
            "uploadedAt": datetime.now().isoformat()
        }
        return {
            "success": True,
            "data": audio_file,
            "message": "文件上传成功"
        }
    except Exception as e:
        return {"success": False, "error": f"上传失败: {str(e)}"}

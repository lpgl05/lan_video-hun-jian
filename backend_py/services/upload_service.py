import os
from uuid import uuid4
from datetime import datetime
from models.oss_client import OSSClient

UPLOAD_VIDEO_DIR = "uploads/videos"
UPLOAD_AUDIO_DIR = "uploads/audios"
USE_OSS = True  # 切换为 True 即可上传到 OSS

oss_client = OSSClient()

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
            # 上传到OSS
            file_url = await oss_client.upload_to_oss(
                file_buffer=content,
                original_filename=file_name,
                folder=UPLOAD_VIDEO_DIR
            )
        else:
            os.makedirs(UPLOAD_VIDEO_DIR, exist_ok=True)
            save_path = os.path.join(UPLOAD_VIDEO_DIR, file_name)
            with open(save_path, "wb") as f:
                f.write(content)
            file_url = f"/uploads/videos/{file_name}"
        # duration 字段可后续完善，这里先为 0
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
            "data": video_file
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
            file_url = await oss_client.upload_to_oss(
                file_buffer=content,
                original_filename=file_name,
                folder=UPLOAD_AUDIO_DIR
            )
        else:
            os.makedirs(UPLOAD_AUDIO_DIR, exist_ok=True)
            save_path = os.path.join(UPLOAD_AUDIO_DIR, file_name)
            with open(save_path, "wb") as f:
                f.write(content)
            file_url = f"/uploads/audios/{file_name}"
        # duration 字段可后续完善，这里先为 0
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
            "data": audio_file
        }
    except Exception as e:
        return {"success": False, "error": f"上传失败: {str(e)}"}
import os
from uuid import uuid4
from datetime import datetime
from models.oss_client import OSSClient

UPLOAD_VIDEO_DIR = "uploads/videos"
UPLOAD_AUDIO_DIR = "uploads/audios"
UPLOAD_POSTER_DIR = "uploads/posters"
USE_OSS = False  # 暂时关闭OSS，测试本地上传

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

async def handle_upload_poster(poster):
    if poster is None:
        return {"success": False, "error": "未收到文件"}
    try:
        file_id = str(uuid4())
        file_name = poster.filename
        content = await poster.read()
        if not content:
            return {"success": False, "error": "文件内容为空"}
        
        # 验证图片格式
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        file_ext = os.path.splitext(file_name)[1].lower()
        if file_ext not in allowed_extensions:
            return {"success": False, "error": "不支持的图片格式，请上传 JPG、PNG、GIF、BMP 或 WebP 格式的图片"}
        
        if USE_OSS:
            # 上传到OSS
            file_url = await oss_client.upload_to_oss(
                file_buffer=content,
                original_filename=file_name,
                folder=UPLOAD_POSTER_DIR
            )
        else:
            os.makedirs(UPLOAD_POSTER_DIR, exist_ok=True)
            save_path = os.path.join(UPLOAD_POSTER_DIR, file_name)
            with open(save_path, "wb") as f:
                f.write(content)
            file_url = f"/uploads/posters/{file_name}"
        
        poster_file = {
            "id": file_id,
            "name": file_name,
            "url": file_url,
            "size": len(content),
            "uploadedAt": datetime.now().isoformat()
        }
        return {
            "success": True,
            "data": poster_file
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
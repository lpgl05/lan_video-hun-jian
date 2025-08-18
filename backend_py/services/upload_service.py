import os
from uuid import uuid4
from datetime import datetime
from models.oss_client import OSSClient
import asyncio
from typing import Dict, Any

UPLOAD_VIDEO_DIR = "uploads/videos"
UPLOAD_AUDIO_DIR = "uploads/audios"
UPLOAD_POSTER_DIR = "uploads/posters"
USE_OSS = True  # 切换为 True 即可上传到 OSS

oss_client = OSSClient()

# 全局上传任务追踪器
upload_tasks: Dict[str, Dict[str, Any]] = {}

async def handle_upload_video(video, task_id: str = None):
    if video is None:
        return {"success": False, "error": "未收到文件"}
    try:
        file_id = str(uuid4())
        file_name = video.filename
        
        # 如果没有提供task_id，生成一个
        if not task_id:
            task_id = file_id
        
        # 先创建任务状态（在读取文件之前）
        upload_tasks[task_id] = {
            "status": "receiving",
            "progress": 0,
            "speed": "0 MB/s",
            "filename": file_name,
            "file_size": 0,
            "uploaded_bytes": 0,
            "start_time": datetime.now(),
            "error": None,
            "stage": "http_receiving"  # 新增阶段标识
        }
        
        print(f"创建上传任务: {task_id}")
        print(f"开始接收文件: {file_name}")
        
        # 读取文件内容（这个过程前端无法感知进度）
        content = await video.read()
        if not content:
            return {"success": False, "error": "文件内容为空"}
        
        # 更新文件大小和状态
        upload_tasks[task_id].update({
            "file_size": len(content),
            "progress": 10,  # HTTP接收完成，给10%
            "stage": "oss_uploading",
            "status": "uploading"
        })
        
        print(f"文件接收完成，大小: {len(content) / (1024*1024):.2f}MB")
        print(f"当前所有任务: {list(upload_tasks.keys())}")
        
        if USE_OSS:
            print(f'开始上传视频到阿里云oss, task_id: {task_id}')
            start_time = datetime.now()
            
            def progress_callback(progress: float, uploaded_bytes: int, speed_mbps: float):
                """OSS上传进度回调"""
                if task_id in upload_tasks:
                    upload_tasks[task_id].update({
                        "progress": progress,
                        "uploaded_bytes": uploaded_bytes,
                        "speed": f"{speed_mbps:.2f} MB/s",
                        "status": "uploading"
                    })
                    # 只在关键进度点输出日志
                    if int(progress) % 20 == 0 or progress >= 95:
                        print(f"任务 {task_id} 进度: {progress:.1f}%, 速度: {speed_mbps:.2f}MB/s")
                else:
                    print(f"警告: task_id {task_id} 不存在")
            
            # 上传到OSS
            file_url = await oss_client.upload_to_oss_with_progress(
                file_buffer=content,
                original_filename=file_name,
                folder=UPLOAD_VIDEO_DIR,
                progress_callback=progress_callback
            )
            end_time = datetime.now()
            t = end_time - start_time
            print(f'上传视频到阿里云oss成功，文件url为：{file_url}, 上传耗时： {t}')
            
            # 更新任务状态为完成
            upload_tasks[task_id].update({
                "status": "completed",
                "progress": 100,
                "file_url": file_url
            })
        else:
            os.makedirs(UPLOAD_VIDEO_DIR, exist_ok=True)
            save_path = os.path.join(UPLOAD_VIDEO_DIR, file_name)
            with open(save_path, "wb") as f:
                f.write(content)
            file_url = f"/uploads/videos/{file_name}"
            
            # 更新任务状态为完成
            upload_tasks[task_id].update({
                "status": "completed",
                "progress": 100,
                "file_url": file_url
            })
        # duration 字段可后续完善，这里先为 0
        video_file = {
            "id": file_id,
            "name": file_name,
            "url": file_url,
            "size": len(content),
            "duration": 0,
            "uploadedAt": datetime.now().isoformat(),
            "task_id": task_id  # 添加任务ID
        }
        return {
            "success": True,
            "data": video_file
        }
    except Exception as e:
        return {"success": False, "error": f"上传失败: {str(e)}"}

async def handle_upload_audio(audio, task_id: str = None):
    if audio is None:
        return {"success": False, "error": "未收到文件"}
    try:
        file_id = str(uuid4())
        file_name = audio.filename
        content = await audio.read()
        if not content:
            return {"success": False, "error": "文件内容为空"}
        
        # 如果没有提供task_id，生成一个
        if not task_id:
            task_id = file_id
            
        # 初始化任务状态
        upload_tasks[task_id] = {
            "status": "uploading",
            "progress": 0,
            "speed": "0 MB/s",
            "filename": file_name,
            "file_size": len(content),
            "uploaded_bytes": 0,
            "start_time": datetime.now(),
            "error": None
        }
        
        print(f"创建音频上传任务: {task_id}")
        
        if USE_OSS:
            print(f'开始上传音频到阿里云oss, task_id: {task_id}')
            start_time = datetime.now()
            
            def progress_callback(progress: float, uploaded_bytes: int, speed_mbps: float):
                """OSS音频上传进度回调"""
                if task_id in upload_tasks:
                    upload_tasks[task_id].update({
                        "progress": progress,
                        "uploaded_bytes": uploaded_bytes,
                        "speed": f"{speed_mbps:.2f} MB/s",
                        "status": "uploading"
                    })
                    # 只在关键进度点输出日志
                    if int(progress) % 20 == 0 or progress >= 95:
                        print(f"音频任务 {task_id} 进度: {progress:.1f}%, 速度: {speed_mbps:.2f}MB/s")
                else:
                    print(f"警告: 音频task_id {task_id} 不存在")
            
            file_url = await oss_client.upload_to_oss_with_progress(
                file_buffer=content,
                original_filename=file_name,
                folder=UPLOAD_AUDIO_DIR,
                progress_callback=progress_callback
            )
            end_time = datetime.now()
            t = end_time - start_time
            print(f'上传音频到阿里云oss成功，文件url为：{file_url}, 上传耗时： {t}')
            
            # 更新任务状态为完成
            upload_tasks[task_id].update({
                "status": "completed",
                "progress": 100,
                "file_url": file_url
            })
        else:
            os.makedirs(UPLOAD_AUDIO_DIR, exist_ok=True)
            save_path = os.path.join(UPLOAD_AUDIO_DIR, file_name)
            with open(save_path, "wb") as f:
                f.write(content)
            file_url = f"/uploads/audios/{file_name}"
            
            # 模拟进度更新
            upload_tasks[task_id].update({
                "status": "completed",
                "progress": 100,
                "file_url": file_url
            })
            
        # duration 字段可后续完善，这里先为 0
        audio_file = {
            "id": file_id,
            "name": file_name,
            "url": file_url,
            "size": len(content),
            "duration": 0,
            "uploadedAt": datetime.now().isoformat(),
            "task_id": task_id  # 添加task_id字段
        }
        return {
            "success": True,
            "data": audio_file
        }
    except Exception as e:
        if task_id and task_id in upload_tasks:
            upload_tasks[task_id].update({
                "status": "failed",
                "error": str(e)
            })
        return {"success": False, "error": f"上传失败: {str(e)}"}

async def handle_upload_poster(poster, task_id: str = None):
    if poster is None:
        return {"success": False, "error": "未收到文件"}
    try:
        file_id = str(uuid4())
        file_name = poster.filename
        content = await poster.read()
        if not content:
            return {"success": False, "error": "文件内容为空"}

        # 验证文件类型
        if not poster.content_type or not poster.content_type.startswith('image/'):
            return {"success": False, "error": "只支持图片文件"}

        # 如果没有提供task_id，生成一个
        if not task_id:
            task_id = file_id

        print(f"创建海报上传任务: {task_id}")

        if USE_OSS:
            print(f'开始上传海报到阿里云oss, task_id: {task_id}')
            start_time = datetime.now()

            file_url = await oss_client.upload_to_oss(
                file_buffer=content,
                original_filename=file_name,
                folder=UPLOAD_POSTER_DIR
            )
            end_time = datetime.now()
            t = end_time - start_time
            print(f'上传海报到阿里云oss成功，文件url为：{file_url}, 上传耗时： {t}')
        else:
            os.makedirs(UPLOAD_POSTER_DIR, exist_ok=True)
            save_path = os.path.join(UPLOAD_POSTER_DIR, file_name)
            with open(save_path, "wb") as f:
                f.write(content)
            file_url = f"/uploads/posters/{file_name}"

        # 简单的图片尺寸检测 (可以使用PIL库获取更精确的信息)
        width, height = None, None
        try:
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(content))
            width, height = img.size
        except:
            pass

        poster_file = {
            "id": file_id,
            "name": file_name,
            "url": file_url,
            "size": len(content),
            "width": width,
            "height": height,
            "uploadedAt": datetime.now().isoformat()
        }
        return {
            "success": True,
            "data": poster_file
        }
    except Exception as e:
        return {"success": False, "error": f"上传失败: {str(e)}"}
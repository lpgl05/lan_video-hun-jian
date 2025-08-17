from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import generation, ai, upload, clip
import os

app = FastAPI(title="Video Generation API", version="1.0.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加静态文件服务
from fastapi import Response
from fastapi.responses import FileResponse

# 挂载uploads目录为静态文件服务
uploads_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)
    # 创建子目录
    os.makedirs(os.path.join(uploads_dir, "videos"), exist_ok=True)
    os.makedirs(os.path.join(uploads_dir, "audios"), exist_ok=True)

app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

@app.get("/test_video.mp4")
async def get_test_video():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_video.mp4")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="video/mp4", filename="test_video.mp4")
    return {"error": "File not found"}

@app.get("/test_audio.mp3")
async def get_test_audio():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_audio.mp3")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg", filename="test_audio.mp3")
    return {"error": "File not found"}

# 包含路由
app.include_router(generation.router, prefix="/api")
app.include_router(ai.router, prefix="/api")
app.include_router(upload.router, prefix="/api")
app.include_router(clip.router, prefix="/api")

@app.get("/api/ping")
async def ping():
    return {"message": "pong"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

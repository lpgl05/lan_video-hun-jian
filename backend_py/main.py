from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# CORS 配置，允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routes.generation import router as generation_router
app.include_router(generation_router)
from routes.ai import router as ai_router
app.include_router(ai_router)
from routes.upload import router as upload_router
app.include_router(upload_router)
from routes.clip import router as clip_router
app.include_router(clip_router)

# 注释掉本地文件服务 - 团队协作模式统一使用OSS存储
# import os
# app.mount("/local-files", StaticFiles(directory="uploads"), name="local-files")

@app.get("/api/ping")
def ping():
    return {"msg": "pong"}

# ...后续会补充路由和服务...

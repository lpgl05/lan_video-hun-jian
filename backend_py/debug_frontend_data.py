import json
from datetime import datetime
from routes.clip import ClipRequest

# 模拟前端实际发送的数据（Date对象序列化后的格式）
frontend_data = {
    "name": "测试项目",
    "videos": [
        {
            "id": "video1",
            "name": "test.mp4",
            "url": "/uploads/videos/test.mp4",
            "size": 1024000,
            "duration": 30,
            "thumbnail": "/uploads/thumbnails/test.jpg",
            "uploadedAt": "2025-01-17T16:04:20.178Z"  # 前端Date对象序列化后的ISO格式
        }
    ],
    "audios": [
        {
            "id": "audio1",
            "name": "test.mp3",
            "url": "/uploads/audios/test.mp3",
            "size": 512000,
            "duration": 30,
            "uploadedAt": "2025-01-17T16:04:20.178Z"  # 前端Date对象序列化后的ISO格式
        }
    ],
    "scripts": [
        {
            "id": "script1",
            "content": "这是一个测试文案",
            "selected": True,
            "generatedAt": "2025-01-17T16:04:20.178Z"  # 前端Date对象序列化后的ISO格式
        }
    ],
    "duration": "30s",
    "videoCount": 3,
    "voice": "female",
    "style": {
        "title": {
            "color": "#ffffff",
            "position": "top",
            "fontSize": 24
        },
        "subtitle": {
            "color": "#ffffff",
            "position": "bottom",
            "fontSize": 16
        }
    },
    "posters": [],
    "usePoster": False
}

print("模拟前端发送的数据格式:")
print(json.dumps(frontend_data, indent=2, ensure_ascii=False))
print("\n" + "="*50 + "\n")

try:
    # 尝试验证数据
    clip_request = ClipRequest(**frontend_data)
    print("✅ 数据验证成功!")
    print(f"项目名称: {clip_request.name}")
    print(f"视频数量: {len(clip_request.videos)}")
    print(f"音频数量: {len(clip_request.audios)}")
    print(f"文案数量: {len(clip_request.scripts)}")
    print(f"视频uploadedAt类型: {type(clip_request.videos[0].uploadedAt)}")
    print(f"视频uploadedAt值: {clip_request.videos[0].uploadedAt}")
except Exception as e:
    print(f"❌ 数据验证失败: {e}")
    print(f"错误类型: {type(e)}")
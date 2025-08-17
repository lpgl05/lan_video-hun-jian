#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试前端发送的数据格式
"""

import json
from datetime import datetime
from routes.clip import ClipRequest, VideoFile, AudioFile, Script, StyleConfig, PosterFile
from pydantic import ValidationError

# 模拟前端发送的数据格式
test_data = {
    "name": "测试项目",
    "videos": [
        {
            "id": "video1",
            "name": "test.mp4",
            "url": "/uploads/videos/test.mp4",
            "size": 1024000,
            "duration": 30,
            "thumbnail": "/uploads/thumbnails/test.jpg",
            "uploadedAt": datetime.now().isoformat()
        }
    ],
    "audios": [
        {
            "id": "audio1",
            "name": "test.mp3",
            "url": "/uploads/audios/test.mp3",
            "size": 512000,
            "duration": 30,
            "uploadedAt": datetime.now().isoformat()
        }
    ],
    "scripts": [
        {
            "id": "script1",
            "content": "这是一个测试文案",
            "selected": True,
            "generatedAt": datetime.now().isoformat()
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

def test_data_validation():
    """测试数据验证"""
    print("测试数据格式:")
    print(json.dumps(test_data, indent=2, ensure_ascii=False))
    print("\n" + "="*50 + "\n")
    
    try:
        # 尝试创建ClipRequest对象
        clip_request = ClipRequest(**test_data)
        print("✅ 数据验证成功!")
        print(f"项目名称: {clip_request.name}")
        print(f"视频数量: {len(clip_request.videos)}")
        print(f"音频数量: {len(clip_request.audios)}")
        print(f"文案数量: {len(clip_request.scripts)}")
        return True
        
    except ValidationError as e:
        print("❌ 数据验证失败:")
        for error in e.errors():
            print(f"  - 字段: {error['loc']}")
            print(f"    错误: {error['msg']}")
            print(f"    输入: {error['input']}")
            print()
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

if __name__ == "__main__":
    test_data_validation()
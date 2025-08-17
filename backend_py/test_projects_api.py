import requests
import json
from datetime import datetime

# 测试数据，模拟前端发送的项目数据
test_project_data = {
    "name": "测试项目",
    "videos": [
        {
            "id": "video1",
            "name": "test_video.mp4",
            "url": "/uploads/videos/test_video.mp4",
            "duration": 30,
            "size": 1024000,
            "uploadedAt": datetime.now().isoformat(),
            "thumbnail": "/uploads/videos/test_video_thumb.jpg"
        }
    ],
    "audios": [
        {
            "id": "audio1",
            "name": "test_audio.mp3",
            "url": "/uploads/audios/test_audio.mp3",
            "duration": 25,
            "size": 512000,
            "uploadedAt": datetime.now().isoformat()
        }
    ],
    "posters": [],
    "usePoster": False,
    "scripts": [
        {
            "id": "script1",
            "content": "这是一个测试脚本内容",
            "generatedAt": datetime.now().isoformat()
        }
    ],
    "duration": 30,
    "videoCount": 1,
    "voice": "female",
    "style": "professional"
}

def test_projects_api():
    url = "http://127.0.0.1:8000/api/projects"
    headers = {"Content-Type": "application/json"}
    
    try:
        print("正在测试 /api/projects 端点...")
        print(f"发送数据到: {url}")
        print(f"数据: {json.dumps(test_project_data, indent=2, ensure_ascii=False)}")
        
        response = requests.post(url, json=test_project_data, headers=headers)
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("✅ 项目保存成功！")
            return True
        elif response.status_code == 422:
            print("❌ 422错误仍然存在")
            try:
                error_detail = response.json()
                print(f"错误详情: {json.dumps(error_detail, indent=2, ensure_ascii=False)}")
            except:
                print("无法解析错误详情")
            return False
        else:
            print(f"❌ 其他错误: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务，请确保服务正在运行")
        return False
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    test_projects_api()
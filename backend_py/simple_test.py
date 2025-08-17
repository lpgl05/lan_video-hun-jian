import requests
import time

def test_basic_connection():
    """测试基本的API连接"""
    try:
        print("测试基本连接...")
        response = requests.get("http://127.0.0.1:8000/api/ping", timeout=5)
        print(f"Ping响应: {response.status_code} - {response.text}")
        
        print("\n测试AI文案生成...")
        ai_data = {"prompt": "测试文案"}
        response = requests.post("http://127.0.0.1:8000/api/ai/generate", json=ai_data, timeout=10)
        print(f"AI生成响应: {response.status_code} - {response.text}")
        
        print("\n测试本地文件访问...")
        response = requests.get("http://127.0.0.1:8000/test_video.mp4", timeout=5)
        print(f"视频文件响应: {response.status_code} - 文件大小: {len(response.content)} bytes")
        
        response = requests.get("http://127.0.0.1:8000/test_audio.mp3", timeout=5)
        print(f"音频文件响应: {response.status_code} - 文件大小: {len(response.content)} bytes")
        
    except Exception as e:
        print(f"连接测试失败: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # 等待服务器稳定
    print("等待服务器稳定...")
    time.sleep(3)
    test_basic_connection()
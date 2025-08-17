import requests
import io

def test_upload_endpoints():
    """测试上传端点是否正常工作"""
    base_url = "http://127.0.0.1:8000"
    
    print("=== 测试上传端点修复 ===")
    
    # 创建测试文件
    video_content = b"fake video content for testing"
    audio_content = b"fake audio content for testing"
    
    # 测试视频上传
    try:
        files = {'video': ('test.mp4', io.BytesIO(video_content), 'video/mp4')}
        response = requests.post(f"{base_url}/api/upload/video", files=files)
        print(f"视频上传状态码: {response.status_code}")
        if response.status_code == 200:
            print("✓ 视频上传成功")
            print(f"响应: {response.json()}")
        else:
            print(f"✗ 视频上传失败: {response.text}")
    except Exception as e:
        print(f"✗ 视频上传异常: {str(e)}")
    
    # 测试音频上传
    try:
        files = {'audio': ('test.mp3', io.BytesIO(audio_content), 'audio/mp3')}
        response = requests.post(f"{base_url}/api/upload/audio", files=files)
        print(f"音频上传状态码: {response.status_code}")
        if response.status_code == 200:
            print("✓ 音频上传成功")
            print(f"响应: {response.json()}")
        else:
            print(f"✗ 音频上传失败: {response.text}")
    except Exception as e:
        print(f"✗ 音频上传异常: {str(e)}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_upload_endpoints()
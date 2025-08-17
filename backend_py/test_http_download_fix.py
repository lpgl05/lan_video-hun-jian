import requests
import json
import time

def test_ai_generation():
    """测试AI文案生成功能"""
    print("\n=== 测试AI文案生成 ===")
    try:
        url = "http://127.0.0.1:8001/api/ai/generate"
        data = {
            "script": "创建一个关于科技创新的短视频",
            "duration": 30,
            "count": 3
        }
        
        response = requests.post(url, json=data, timeout=30)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("✓ AI文案生成成功")
                # 处理新的响应格式：data是一个列表
                data = result.get('data', [])
                if isinstance(data, list) and len(data) > 0:
                    print(f"生成的文案: {data[0]}")
                else:
                    print(f"生成的文案: {data}")
                return True
            else:
                print(f"✗ AI文案生成失败: {result.get('error')}")
        else:
            print(f"✗ HTTP错误: {response.text}")
        return False
        
    except Exception as e:
        print(f"✗ AI文案生成异常: {e}")
        return False

def test_project_creation():
    """测试项目创建功能"""
    print("\n=== 测试项目创建 ===")
    try:
        url = "http://127.0.0.1:8001/api/projects"
        data = {
            "name": "测试项目HTTP下载",
            "videos": ["https://tian-jiu-video.oss-cn-beijing.aliyuncs.com/uploads/test-video.mp4"],
            "audios": ["https://tian-jiu-video.oss-cn-beijing.aliyuncs.com/uploads/test-audio.mp3"],
            "scripts": ["这是一个测试脚本"],
            "duration": 30,
            "videoCount": 1,
            "voice": "female",
            "style": "modern"
        }
        
        response = requests.post(url, json=data, timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                project_id = result.get("project_id")
                print(f"✓ 项目创建成功，ID: {project_id}")
                return project_id
            else:
                print(f"✗ 项目创建失败: {result}")
        else:
            print(f"✗ HTTP错误: {response.text}")
        return None
        
    except Exception as e:
        print(f"✗ 项目创建异常: {e}")
        return None

def test_video_generation(project_id):
    """测试视频生成功能"""
    print("\n=== 测试视频生成 ===")
    try:
        url = f"http://127.0.0.1:8001/api/projects/{project_id}/generate"
        
        response = requests.post(url, timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("✓ 视频生成成功")
                print(f"输出视频: {result.get('data', {}).get('output_video')}")
                return True
            else:
                print(f"✗ 视频生成失败: {result}")
        else:
            print(f"✗ HTTP错误: {response.text}")
        return False
        
    except Exception as e:
        print(f"✗ 视频生成异常: {e}")
        return False

def test_file_access():
    """测试文件访问功能"""
    print("\n=== 测试文件访问 ===")
    
    # 测试视频文件
    try:
        response = requests.get("http://127.0.0.1:8001/test_video.mp4", timeout=5)
        if response.status_code == 200:
            print("✓ 测试视频文件访问成功")
        else:
            print(f"✗ 测试视频文件访问失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 测试视频文件访问异常: {e}")
    
    # 测试音频文件
    try:
        response = requests.get("http://127.0.0.1:8001/test_audio.mp3", timeout=5)
        if response.status_code == 200:
            print("✓ 测试音频文件访问成功")
        else:
            print(f"✗ 测试音频文件访问失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 测试音频文件访问异常: {e}")

def main():
    """主测试函数"""
    print("=== 完整功能测试开始 ===")
    
    # 1. 测试AI文案生成
    ai_success = test_ai_generation()
    
    # 2. 测试项目创建
    project_id = test_project_creation()
    
    # 3. 测试视频生成
    video_success = False
    if project_id:
        video_success = test_video_generation(project_id)
    
    # 4. 测试文件访问
    test_file_access()
    
    # 总结
    print("\n=== 测试结果总结 ===")
    print(f"AI文案生成: {'✓ 成功' if ai_success else '✗ 失败'}")
    print(f"项目创建: {'✓ 成功' if project_id else '✗ 失败'}")
    print(f"视频生成: {'✓ 成功' if video_success else '✗ 失败'}")
    print(f"项目ID: {project_id if project_id else '无'}")
    
    if ai_success and project_id and video_success:
        print("\n🎉 所有核心功能测试通过！")
    else:
        print("\n⚠️ 部分功能存在问题，需要进一步调试")

if __name__ == "__main__":
    main()
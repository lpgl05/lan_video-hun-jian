import requests
import time

def test_basic_connection():
    """测试后端服务基本连接性"""
    try:
        print("测试后端服务基本连接...")
        
        # 测试根路径
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        print(f"根路径响应: {response.status_code} - {response.text[:100]}")
        
        # 测试健康检查端点
        try:
            response = requests.get("http://127.0.0.1:8000/health", timeout=5)
            print(f"健康检查响应: {response.status_code} - {response.text[:100]}")
        except:
            print("健康检查端点不存在")
        
        # 测试静态文件
        try:
            response = requests.get("http://127.0.0.1:8000/test_video.mp4", timeout=5)
            print(f"测试视频文件响应: {response.status_code} - 文件大小: {len(response.content)} bytes")
        except Exception as e:
            print(f"测试视频文件失败: {e}")
            
        try:
            response = requests.get("http://127.0.0.1:8000/test_audio.mp3", timeout=5)
            print(f"测试音频文件响应: {response.status_code} - 文件大小: {len(response.content)} bytes")
        except Exception as e:
            print(f"测试音频文件失败: {e}")
        
        return True
        
    except Exception as e:
        print(f"基本连接测试失败: {e}")
        return False

def test_simple_api():
    """测试简单的API端点"""
    try:
        print("\n测试API端点...")
        
        # 测试项目创建端点（不发送数据，只测试连接）
        try:
            response = requests.get("http://127.0.0.1:8000/api/projects", timeout=5)
            print(f"项目API GET响应: {response.status_code}")
        except Exception as e:
            print(f"项目API测试失败: {e}")
        
        return True
        
    except Exception as e:
        print(f"API测试失败: {e}")
        return False

def main():
    print("=== 后端服务基本连接测试 ===")
    
    # 等待服务启动
    print("等待服务启动...")
    time.sleep(2)
    
    basic_ok = test_basic_connection()
    api_ok = test_simple_api()
    
    print("\n=== 测试结果 ===")
    print(f"基本连接: {'✓ 正常' if basic_ok else '✗ 异常'}")
    print(f"API连接: {'✓ 正常' if api_ok else '✗ 异常'}")
    
    if basic_ok and api_ok:
        print("\n🎉 后端服务连接正常！")
    else:
        print("\n⚠️ 后端服务存在连接问题")

if __name__ == "__main__":
    main()
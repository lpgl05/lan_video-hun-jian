import requests
import time

def test_backend_8001():
    """测试8001端口的后端服务"""
    print("=== 测试8001端口后端服务 ===")
    
    base_url = "http://127.0.0.1:8001"
    
    # 测试基本连接
    try:
        response = requests.get(f"{base_url}/api/ping", timeout=5)
        if response.status_code == 200:
            print(f"✓ /api/ping 成功: {response.json()}")
        else:
            print(f"✗ /api/ping 失败: {response.status_code}")
    except Exception as e:
        print(f"✗ /api/ping 异常: {e}")
    
    # 测试根路径
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print(f"✓ 根路径成功: {response.json()}")
        else:
            print(f"✗ 根路径失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 根路径异常: {e}")
    
    # 测试健康检查
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print(f"✓ /health 成功: {response.json()}")
        else:
            print(f"✗ /health 失败: {response.status_code}")
    except Exception as e:
        print(f"✗ /health 异常: {e}")

if __name__ == "__main__":
    test_backend_8001()
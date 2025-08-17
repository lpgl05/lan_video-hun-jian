import requests
import time

def test_minimal():
    """最简单的连接测试"""
    try:
        print("测试最基本的连接...")
        
        # 只测试ping端点
        response = requests.get("http://127.0.0.1:8000/api/ping", timeout=10)
        print(f"Ping响应: {response.status_code} - {response.text}")
        
        if response.status_code == 200:
            print("✓ 后端服务连接正常！")
            return True
        else:
            print(f"✗ 后端服务响应异常: {response.status_code}")
            return False
        
    except requests.exceptions.Timeout:
        print("✗ 连接超时 - 后端服务可能存在阻塞")
        return False
    except requests.exceptions.ConnectionError:
        print("✗ 连接错误 - 后端服务可能未启动")
        return False
    except Exception as e:
        print(f"✗ 其他错误: {e}")
        return False

if __name__ == "__main__":
    print("=== 最小化后端服务测试 ===")
    time.sleep(3)  # 等待服务启动
    test_minimal()
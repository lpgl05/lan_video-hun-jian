import subprocess
import sys

def test_with_curl():
    """使用curl命令测试后端服务"""
    print("=== 使用curl测试后端服务 ===")
    
    try:
        # 测试基本连接
        result = subprocess.run(
            ["curl", "-s", "-w", "%{http_code}", "http://127.0.0.1:8000/api/ping"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print(f"✓ curl测试成功: {result.stdout}")
        else:
            print(f"✗ curl测试失败: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("✗ curl命令超时")
    except FileNotFoundError:
        print("✗ curl命令未找到，尝试使用PowerShell")
        test_with_powershell()
    except Exception as e:
        print(f"✗ curl测试异常: {e}")

def test_with_powershell():
    """使用PowerShell的Invoke-WebRequest测试"""
    try:
        cmd = 'Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/ping" -UseBasicParsing -TimeoutSec 5'
        result = subprocess.run(
            ["powershell", "-Command", cmd],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print(f"✓ PowerShell测试成功: {result.stdout[:200]}")
        else:
            print(f"✗ PowerShell测试失败: {result.stderr}")
            
    except Exception as e:
        print(f"✗ PowerShell测试异常: {e}")

if __name__ == "__main__":
    test_with_curl()
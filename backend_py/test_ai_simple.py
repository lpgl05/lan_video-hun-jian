import asyncio
import httpx
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

async def test_ai_service():
    """测试AI服务是否正常工作"""
    try:
        # 测试本地AI服务端点
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                "http://127.0.0.1:8000/api/ai/generate",
                json={
                    "script": "这是一个测试文案",
                    "duration": 30,
                    "count": 1
                }
            )
            
            print(f"AI服务响应状态码: {response.status_code}")
            print(f"AI服务响应内容: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"AI服务返回数据: {data}")
                return True
            else:
                print(f"AI服务调用失败: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"测试AI服务时发生错误: {str(e)}")
        return False

async def test_fastgpt_direct():
    """直接测试FastGPT API"""
    try:
        api_url = os.getenv('FASTGPT_API_URL')
        api_key = os.getenv('FASTGPT_API_KEY')
        
        print(f"FastGPT API URL: {api_url}")
        print(f"FastGPT API Key: {api_key[:20]}..." if api_key else "API Key未设置")
        
        if not api_url or not api_key:
            print("FastGPT配置缺失")
            return False
            
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "chatId": "test-chat-id",
            "stream": False,
            "detail": False,
            "messages": [
                {
                    "role": "user",
                    "content": "请改写以下文案：这是一个测试文案"
                }
            ],
            "variables": {}
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(api_url, headers=headers, json=data)
            
            print(f"FastGPT直接调用状态码: {response.status_code}")
            print(f"FastGPT直接调用响应: {response.text}")
            
            if response.status_code == 200:
                response_data = response.json()
                print(f"FastGPT成功响应: {response_data}")
                return True
            else:
                print(f"FastGPT调用失败: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"直接测试FastGPT时发生错误: {str(e)}")
        return False

async def main():
    print("=== 开始AI服务测试 ===")
    
    print("\n1. 测试本地AI服务...")
    ai_result = await test_ai_service()
    
    print("\n2. 直接测试FastGPT API...")
    fastgpt_result = await test_fastgpt_direct()
    
    print("\n=== 测试结果汇总 ===")
    print(f"本地AI服务: {'✓ 正常' if ai_result else '✗ 异常'}")
    print(f"FastGPT API: {'✓ 正常' if fastgpt_result else '✗ 异常'}")
    
    if ai_result and fastgpt_result:
        print("\n🎉 所有AI服务测试通过！")
    else:
        print("\n⚠️ 部分AI服务存在问题，需要进一步调试")

if __name__ == "__main__":
    asyncio.run(main())
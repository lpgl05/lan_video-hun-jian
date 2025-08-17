import asyncio
import httpx
import json
from uuid import uuid4
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

async def test_fastgpt_api():
    """
    详细测试FastGPT API调用
    """
    api_url = os.getenv('FASTGPT_API_URL')
    api_key = os.getenv('FASTGPT_API_KEY')
    
    print(f"API URL: {api_url}")
    print(f"API Key: {api_key[:20]}..." if api_key else "API Key: None")
    
    if not api_url or not api_key:
        print("❌ FastGPT API配置缺失")
        return
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 测试简单的提示词
    test_prompt = "请改写以下文案：这是一个测试视频。要求：保持原意，表达更生动。"
    
    data = {
        "chatId": str(uuid4()),
        "stream": False,
        "detail": False,
        "variables": {
            "input": test_prompt,
            "text": test_prompt,
            "content": test_prompt,
            "prompt": test_prompt,
            "文案": test_prompt,
            "原文案": test_prompt,
            "输入文案": test_prompt
        }
    }
    
    print("\n📤 发送请求:")
    print(f"URL: {api_url}")
    print(f"Headers: {json.dumps(headers, indent=2, ensure_ascii=False)}")
    print(f"Data: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(api_url, headers=headers, json=data)
            
            print(f"\n📥 响应状态码: {response.status_code}")
            print(f"响应头: {dict(response.headers)}")
            
            if response.status_code == 200:
                response_data = response.json()
                print(f"\n✅ 完整响应数据:")
                print(json.dumps(response_data, indent=2, ensure_ascii=False))
                
                # 检查错误信息
                if 'responseData' in response_data:
                    print("\n🔍 检查responseData中的错误:")
                    for i, item in enumerate(response_data['responseData']):
                        print(f"  项目 {i}: {json.dumps(item, indent=4, ensure_ascii=False)}")
                        if 'errorText' in item:
                            print(f"  ❌ 发现错误: {item['errorText']}")
                
                # 解析内容
                if 'choices' in response_data and len(response_data['choices']) > 0:
                    choice = response_data['choices'][0]
                    print(f"\n🎯 解析choices[0]: {json.dumps(choice, indent=2, ensure_ascii=False)}")
                    
                    if 'message' in choice and 'content' in choice['message']:
                        content = choice['message']['content']
                        print(f"\n📝 content类型: {type(content)}")
                        print(f"content值: {content}")
                        
                        if isinstance(content, list) and len(content) > 0:
                            print("\n🔍 解析列表格式内容:")
                            for i, item in enumerate(content):
                                print(f"  项目 {i}: {json.dumps(item, indent=4, ensure_ascii=False)}")
                                if isinstance(item, dict) and 'text' in item:
                                    text_obj = item['text']
                                    if isinstance(text_obj, dict) and 'content' in text_obj:
                                        actual_content = text_obj['content']
                                        print(f"  ✅ 找到实际内容: {actual_content}")
                                        return actual_content
                        elif isinstance(content, str):
                            print(f"✅ 字符串格式内容: {content}")
                            return content
                        else:
                            print(f"❌ 未知内容格式: {type(content)}")
                    else:
                        print("❌ 缺少message.content字段")
                else:
                    print("❌ 缺少choices字段")
            else:
                print(f"❌ API调用失败: {response.status_code}")
                print(f"错误响应: {response.text}")
                
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_fastgpt_api())
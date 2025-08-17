import httpx
from uuid import uuid4
from datetime import datetime
import os
from dotenv import load_dotenv
import re

# 加载.env文件中的环境变量
load_dotenv()

FASTGPT_API_URL = os.getenv("FASTGPT_API_URL", "https://api.fastgpt.in/api/v1/chat/completions")
FASTGPT_API_KEY = os.getenv("FASTGPT_API_KEY", "")

style_prompts = {
    'professional': '请用专业正式的语气改写以下文案，保持内容的准确性和权威性：',
    'casual': '请用轻松活泼的语气改写以下文案，让内容更加亲切自然：',
    'emotional': '请用富有情感的语气改写以下文案，增强内容的感染力：',
    'marketing': '请用营销导向的语气改写以下文案，突出产品卖点和价值主张：',
    '': '请改写以下文案，保持原意的同时让表达更加清晰有力：'
}
rewrite_style = 'professional'
style_prompt = style_prompts.get(rewrite_style, style_prompts[''])

async def generate_scripts_service(base_script: str, video_duration: int, count: int = 3):
    """
    生成多个改写版本的文案
    """
    scripts = []
    
    for i in range(count):
        try:
            # 构建简化的提示词
            prompt = f"请改写以下文案：{base_script}。要求：适合{video_duration}秒视频，保持原意，表达更吸引人，控制在{video_duration * 3}字以内。直接输出改写结果。"
            
            print(f"开始生成第{i+1}个文案")
            
            # 调用修复后的FastGPT函数
            generated_script = await call_fastGPT(prompt.strip())
            scripts.append(generated_script)
            
            print(f"第{i+1}个文案生成完成: {generated_script[:50]}...")
                
        except Exception as e:
            print(f"生成第{i+1}个文案时发生错误: {str(e)}")
            scripts.append("生成失败的文案")
    
    return {"success": True, "data": scripts}

async def call_fastGPT(prompt: str, max_retries: int = 3) -> str:
    """
    调用FastGPT API生成文案，带重试机制
    """
    api_url = os.getenv("FASTGPT_API_URL")
    api_key = os.getenv("FASTGPT_API_KEY")
    
    if not api_url or not api_key:
        raise Exception("FastGPT API配置缺失，请检查FASTGPT_API_URL和FASTGPT_API_KEY环境变量")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 优化FastGPT API调用格式
    data = {
        "chatId": str(uuid4()),
        "stream": False,
        "detail": True,  # 启用详细信息以获取更好的错误信息
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "variables": {}
    }
    
    for attempt in range(max_retries):
        try:
            print(f"FastGPT API调用尝试 {attempt + 1}/{max_retries}: {api_url}")
            print(f"请求数据: {data}")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(api_url, json=data, headers=headers, timeout=60.0)
                
                print(f"FastGPT响应状态: {response.status_code}")
                print(f"FastGPT响应内容: {response.text}")
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # 检查标准OpenAI格式响应
                    if 'choices' in result and len(result['choices']) > 0:
                        content = result['choices'][0]['message']['content']
                        if content:
                            # 处理可能的list格式内容
                            if isinstance(content, list):
                                # 如果是列表，提取第一个有效的文本内容
                                for item in content:
                                    if isinstance(item, dict) and 'text' in item:
                                        text_obj = item['text']
                                        if isinstance(text_obj, dict) and 'content' in text_obj:
                                            actual_content = text_obj['content']
                                            if actual_content and isinstance(actual_content, str):
                                                print(f"FastGPT成功返回内容(从列表解析): {actual_content[:100]}...")
                                                return actual_content.strip()
                                    elif isinstance(item, str) and item.strip():
                                        print(f"FastGPT成功返回内容(列表字符串): {item[:100]}...")
                                        return item.strip()
                            elif isinstance(content, str) and content.strip():
                                print(f"FastGPT成功返回内容: {content[:100]}...")
                                return content.strip()
                    
                    # 检查FastGPT特有格式
                    if 'data' in result:
                        for item in result['data']:
                            if 'value' in item and item['value']:
                                value = item['value']
                                # 处理可能的list格式value
                                if isinstance(value, list):
                                    # 如果是列表，提取第一个有效的文本内容
                                    for list_item in value:
                                        if isinstance(list_item, dict) and 'text' in list_item:
                                            text_obj = list_item['text']
                                            if isinstance(text_obj, dict) and 'content' in text_obj:
                                                actual_content = text_obj['content']
                                                if actual_content and isinstance(actual_content, str):
                                                    print(f"FastGPT返回数据(从列表解析): {actual_content[:100]}...")
                                                    return actual_content.strip()
                                        elif isinstance(list_item, str) and list_item.strip():
                                            print(f"FastGPT返回数据(列表字符串): {list_item[:100]}...")
                                            return list_item.strip()
                                elif isinstance(value, str):
                                    print(f"FastGPT返回数据: {value[:100]}...")
                                    return value.strip()
                            elif 'errorText' in item:
                                error_text = item['errorText']
                                print(f"FastGPT工作流错误: {error_text}")
                                if "AI_input_is_empty" in error_text:
                                    if attempt < max_retries - 1:
                                        print(f"AI输入为空，重试第 {attempt + 2} 次...")
                                        continue
                                    else:
                                        raise Exception(f"FastGPT API错误: {error_text}，已重试{max_retries}次")
                                else:
                                    raise Exception(f"FastGPT工作流错误: {error_text}")
                    
                    # 如果没有找到有效内容，重试
                    if attempt < max_retries - 1:
                        print(f"未获取到有效内容，重试第 {attempt + 2} 次...")
                        continue
                    else:
                        raise Exception(f"FastGPT API返回空内容，已重试{max_retries}次")
                        
                else:
                    error_msg = f"FastGPT API调用失败: {response.status_code} - {response.text}"
                    if attempt < max_retries - 1:
                        print(f"{error_msg}，重试第 {attempt + 2} 次...")
                        continue
                    else:
                        raise Exception(f"{error_msg}，已重试{max_retries}次")
                        
        except httpx.TimeoutException:
            if attempt < max_retries - 1:
                print(f"请求超时，重试第 {attempt + 2} 次...")
                continue
            else:
                raise Exception(f"FastGPT API请求超时，已重试{max_retries}次")
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"请求异常: {e}，重试第 {attempt + 2} 次...")
                continue
            else:
                print(f"FastGPT API调用最终失败: {e}")
                raise e
    
    raise Exception(f"FastGPT API调用失败，已重试{max_retries}次")


# 移除本地改写fallback函数，按用户要求只使用FastGPT
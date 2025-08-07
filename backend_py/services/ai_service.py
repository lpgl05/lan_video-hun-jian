import requests
from uuid import uuid4
from datetime import datetime

FASTGPT_API_URL = "https://api.fastgpt.in/api/v1/chat/completions"
FASTGPT_API_KEY = "fastgpt-dIZ13SeCXJOp0eCvGvwVaqR71Kq6qRHtDUkH1CqMpxIQCWvwV0qvT3p"
style_prompts = {
    'professional': '请用专业正式的语气改写以下文案，保持内容的准确性和权威性：',
    'casual': '请用轻松活泼的语气改写以下文案，让内容更加亲切自然：',
    'emotional': '请用富有情感的语气改写以下文案，增强内容的感染力：',
    'marketing': '请用营销导向的语气改写以下文案，突出产品卖点和价值主张：',
    '': '请改写以下文案，保持原意的同时让表达更加清晰有力：'
}
rewrite_style = 'professional'
style_prompt = style_prompts.get(rewrite_style, style_prompts[''])

async def generate_scripts_service(base_script: str, video_duration: int, video_count: int):
    scripts = []
    for i in range(video_count):
        response = call_fastGPT(base_script, video_duration, i)
        # 检查请求是否成功
        if response.status_code == 200:
            # 解析并打印返回值
            response_data = response.json()
            content = response_data['choices'][0]['message']['content']
            # 如果内容有多行，将其处理为一行
            content = ' '.join(content.splitlines()).strip()
            scripts.append(content)
        else:
            print(f"请求失败，状态码: {response.status_code}, 错误信息: {response.text}")
    return {"success": True, "data": scripts}

def call_fastGPT(base_script: str, video_duration: int, i: int):
    prompt = f"""{style_prompt}
原始文案：{base_script}

要求：
1. 改写后的文案适合{video_duration}秒的视频使用
2. 保持原意不变，但表达方式要更加吸引人
3. 内容长度控制在{video_duration * 3}字以内
5. 生成的内容有正确的标点符号和语法
5. 这是第{i+1}个改写版本，请确保与之前版本有所区别

请直接输出改写后的文案，不要添加任何解释，不要添加emoji、表情符号、特殊字符、乱码字符。
"""
    user_text = prompt.strip()
    response = requests.post(
        url=FASTGPT_API_URL,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {FASTGPT_API_KEY}"
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        },
        timeout=30
    )
    return response
from fastapi import APIRouter, Request
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime
import os
from openai import OpenAI

router = APIRouter()

API_KEY = "sk-AAA"
model_name = "deepseek-ai/DeepSeek-V2.5"
llm = OpenAI(
    base_url='https://api.siliconflow.cn/v1',
    api_key=API_KEY
)

class Script(BaseModel):
    id: str
    content: str
    selected: bool = False
    generatedAt: datetime

class GenerateScriptsRequest(BaseModel):
    baseScript: str

@router.post("/api/ai/generate-scripts")
async def generate_scripts(req: GenerateScriptsRequest):
    base_script = req.baseScript.strip()
    if not base_script:
        return {"success": False, "error": "请输入基础文案"}

    prompt = (
        f"基于以下基础文案，生成20个不同的变体文案，要求：\n"
        "1. 保持原意不变，但表达方式要多样化\n"
        "2. 适合短视频平台使用\n"
        "3. 语言简洁有力，有感染力\n"
        "4. 每个文案长度控制在50字以内\n"
        "5. 风格可以是：幽默、励志、温暖、专业等\n\n"
        f"基础文案：{base_script}\n\n"
        "请直接返回20个文案，每个文案一行，不要编号。"
    )

    print(prompt)

    try:

        # 发送带有流式输出的请求
        response = llm.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "你是一个专业的短视频文案创作助手，擅长创作吸引人的短视频文案。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.8,
        )
        content = response.choices[0].message.content if response.choices else ""
        script_lines = [line.strip() for line in content.split('\n') if 0 < len(line.strip()) <= 50][:20]
        while len(script_lines) < 20:
            script_lines.append(f"{base_script} - 变体{len(script_lines)+1}")
        scripts = [Script(id=str(uuid4()), content=txt, generatedAt=datetime.now()) for txt in script_lines]
        return {"success": True, "data": [s.dict() for s in scripts]}
    except Exception as e:
        fallback_scripts = [
            Script(id=str(uuid4()), content=base_script, generatedAt=datetime.now()),
            Script(id=str(uuid4()), content=f"{base_script} - 精彩版", generatedAt=datetime.now()),
            Script(id=str(uuid4()), content=f"{base_script} - 震撼版", generatedAt=datetime.now()),
            Script(id=str(uuid4()), content=f"{base_script} - 温馨版", generatedAt=datetime.now()),
            Script(id=str(uuid4()), content=f"{base_script} - 专业版", generatedAt=datetime.now()),
        ]
        return {
            "success": True,
            "data": [s.dict() for s in fallback_scripts],
            "message": "AI生成失败，返回基础变体"
        }

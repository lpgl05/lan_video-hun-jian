import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from routes.ai import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_generate_scripts_success():
    response = client.post(
        "/api/ai/generate-scripts",
        json={"baseScript": "一只小狗在田野中奔跑，阳光洒在它的毛发上，显得格外温暖。"}
    )
    assert response.status_code == 200
    data = response.json()
    print('======================================')
    assert data["success"] is True
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) == 20 or len(data["data"]) == 5  # 兜底情况
    for script in data["data"]:
        assert "id" in script
        assert "content" in script
        assert "generatedAt" in script
        print(f"生成文案: {script['content']}")


def test_generate_scripts_empty():
    response = client.post(
        "/api/ai/generate-scripts",
        json={"baseScript": ""}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert "error" in data

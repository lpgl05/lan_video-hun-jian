#!/usr/bin/env python3
"""
简化的视频生成测试脚本
用于测试基础功能是否正常工作
"""
import asyncio
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.clip_service import process_clips, parse_duration, generate_tts_audio
from models.oss_client import OSSClient

class MockRequest:
    """模拟请求对象"""
    def __init__(self):
        self.videoCount = 1
        self.duration = "15s"
        self.videos = []
        self.audios = []
        self.scripts = [MockScript()]
        self.style = {
            "title": {
                "fontSize": 40,
                "color": "#FFFFFF",
                "position": "top"
            },
            "subtitle": {
                "fontSize": 32,
                "color": "#FFFFFF",
                "position": "bottom"
            }
        }

class MockScript:
    """模拟脚本对象"""
    def __init__(self):
        self.content = "这是一个测试脚本"
        self.selected = True

async def test_basic_functions():
    """测试基础功能"""
    print("🧪 开始测试基础功能...")
    
    # 1. 测试时长解析
    print("1️⃣ 测试时长解析...")
    duration = parse_duration("15s")
    print(f"   ✅ 解析结果: {duration}秒")
    
    # 2. 测试TTS生成
    print("2️⃣ 测试TTS生成...")
    try:
        tts_path = "test_tts.wav"
        await generate_tts_audio("测试语音合成", tts_path)
        if os.path.exists(tts_path):
            print(f"   ✅ TTS生成成功: {tts_path}")
            os.remove(tts_path)  # 清理测试文件
        else:
            print("   ❌ TTS文件未生成")
    except Exception as e:
        print(f"   ❌ TTS生成失败: {e}")
    
    # 3. 测试OSS连接
    print("3️⃣ 测试OSS连接...")
    try:
        oss_client = OSSClient()
        test_data = b"test"
        url = await oss_client.upload_to_oss(
            file_buffer=test_data,
            original_filename="test.txt",
            folder="test"
        )
        print(f"   ✅ OSS上传成功: {url}")
    except Exception as e:
        print(f"   ❌ OSS连接失败: {e}")
    
    # 4. 测试目录创建
    print("4️⃣ 测试目录结构...")
    required_dirs = [
        "outputs/download_videos",
        "outputs/download_audios", 
        "outputs/clips",
        "outputs/tts_audio",
        "outputs/subtitle_images"
    ]
    
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            print(f"   📁 创建目录: {dir_path}")
        else:
            print(f"   ✅ 目录存在: {dir_path}")
    
    print("\n🎯 基础功能测试完成")

async def test_with_mock_data():
    """使用模拟数据测试流程（不涉及实际文件）"""
    print("\n🔬 开始模拟数据测试...")
    
    try:
        # 创建模拟请求
        mock_req = MockRequest()
        
        print("✅ 模拟请求创建成功")
        print(f"   视频数量: {mock_req.videoCount}")
        print(f"   时长: {mock_req.duration}")
        print(f"   脚本: {mock_req.scripts[0].content}")
        
        # 注意：这里不实际执行 process_clips，因为需要真实的视频文件
        print("⚠️  跳过实际处理（需要真实视频文件）")
        
    except Exception as e:
        print(f"❌ 模拟测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 开始视频生成组件测试...")
    print("=" * 50)
    
    asyncio.run(test_basic_functions())
    asyncio.run(test_with_mock_data())
    
    print("\n" + "=" * 50)
    print("📋 测试总结:")
    print("1. 如果所有基础功能测试通过，说明环境配置正常")
    print("2. 如果TTS或OSS测试失败，检查相关配置")
    print("3. 实际视频生成需要真实的视频和音频文件")

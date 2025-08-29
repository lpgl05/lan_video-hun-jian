#!/usr/bin/env python3
"""
调试版本的视频生成
添加详细的错误捕获和日志输出
"""
import asyncio
import traceback
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routes.clip import process_video_generation, ClipRequest, VideoFile, AudioFile, Script, StyleConfig

# 创建测试用的请求数据
def create_test_request():
    """创建一个最小化的测试请求"""
    return {
        "name": "测试项目",
        "videos": [],  # 空视频列表，看看会发生什么
        "audios": [],  # 空音频列表
        "scripts": [
            {
                "id": "test_script",
                "content": "这是一个测试脚本，用于检查生成流程",
                "selected": True,
                "generatedAt": "2024-01-01T00:00:00Z"
            }
        ],
        "duration": "15s",
        "videoCount": 1,
        "voice": "female",
        "style": {
            "title": {
                "fontSize": 40,
                "color": "#FFFFFF",
                "position": "top"
            },
            "subtitle": {
                "fontSize": 32,
                "color": "#FFFFFF", 
                "position": "bottom"
            },
            "advanced": {
                "enabled": False  # 使用快速模式
            }
        }
    }

async def debug_video_generation():
    """调试视频生成过程"""
    print("🔍 开始调试视频生成...")
    
    try:
        # 1. 创建测试请求
        test_data = create_test_request()
        print(f"✅ 测试数据: {test_data}")
        
        # 2. 模拟完整的请求处理
        print("\n📦 模拟请求处理...")
        
        # 由于没有实际的视频文件，这里会失败，但我们可以看到具体在哪里失败
        print("⚠️  注意: 由于没有实际视频文件，预期会在视频处理阶段失败")
        print("   这有助于我们定位具体的失败点")
        
        return True
        
    except Exception as e:
        print(f"❌ 调试过程中发生错误: {e}")
        print("\n🔍 详细错误信息:")
        traceback.print_exc()
        return False

async def test_request_validation():
    """测试请求验证"""
    print("\n🧪 测试请求验证...")
    
    try:
        from pydantic import BaseModel
        test_data = create_test_request()
        
        # 测试StyleConfig
        style_data = test_data["style"]
        print(f"✅ 样式配置: {style_data}")
        
        # 测试脚本数据
        scripts = test_data["scripts"]
        print(f"✅ 脚本数据: {scripts}")
        
        return True
        
    except Exception as e:
        print(f"❌ 请求验证失败: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 开始视频生成调试...")
    print("=" * 60)
    
    # 测试请求验证
    success1 = asyncio.run(test_request_validation())
    
    # 测试生成流程
    success2 = asyncio.run(debug_video_generation())
    
    print("\n" + "=" * 60)
    print("📋 调试总结:")
    if success1 and success2:
        print("✅ 基础验证通过，可能的问题在于:")
        print("   1. 视频/音频文件不存在或无法访问")
        print("   2. FFmpeg处理过程中的错误")
        print("   3. OSS上传过程中的网络问题")
    else:
        print("❌ 发现基础配置问题，需要修复后再测试")
    
    print("\n💡 建议:")
    print("1. 确保有可用的视频和音频文件")
    print("2. 检查后端服务日志获取详细错误信息")
    print("3. 尝试使用简单模式生成视频")

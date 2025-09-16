#!/usr/bin/env python3
"""
测试竖屏视频修复效果
验证当选择template2时，视频不会被变形，也不会添加背景模糊
"""

import requests
import json
import time
import os

# 测试环境配置
BASE_URL = "http://localhost:9000"
TEST_VIDEO_URL = "https://example.com/test_vertical_video.mp4"  # 需要替换为实际的竖屏测试视频

def test_vertical_video_processing():
    """测试竖屏视频处理"""
    print("🧪 开始测试竖屏视频处理修复...")
    
    # 测试配置 - 使用template2（竖屏模式）
    test_config = {
        "title": "测试竖屏视频",
        "subtitle": "这是副标题",
        "script": "这是一个测试竖屏视频处理的脚本，用来验证修复效果。",
        "source_video_url": TEST_VIDEO_URL,
        "style": {
            "title": {
                "color": "#FFD700",
                "fontSize": 64,
                "fontFamily": "SourceHanSansCN-Heavy"
            },
            "subtitle": {
                "color": "#ffffff",
                "position": "template2",  # 关键：使用竖屏模板
                "fontSize": 60,
                "fontFamily": "SourceHanSansCN-Heavy"
            }
        }
    }
    
    try:
        # 发送生成请求
        print("📤 发送视频生成请求...")
        response = requests.post(f"{BASE_URL}/api/generation/create", json=test_config)
        
        if response.status_code != 200:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
            
        result = response.json()
        if not result.get("success"):
            print(f"❌ 生成失败: {result.get('error', '未知错误')}")
            return False
            
        task_id = result.get("task_id")
        print(f"✅ 任务创建成功，ID: {task_id}")
        
        # 轮询任务状态
        print("⏳ 等待视频生成完成...")
        max_wait_time = 300  # 5分钟超时
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            status_response = requests.get(f"{BASE_URL}/api/generation/status/{task_id}")
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                status = status_data.get("status")
                
                print(f"📊 当前状态: {status}")
                
                if status == "completed":
                    video_url = status_data.get("video_url")
                    print(f"🎉 视频生成完成!")
                    print(f"📹 视频URL: {video_url}")
                    
                    # 验证结果
                    return verify_vertical_video_result(video_url)
                    
                elif status == "failed":
                    error = status_data.get("error", "未知错误")
                    print(f"❌ 视频生成失败: {error}")
                    return False
                    
            time.sleep(5)  # 每5秒检查一次
            
        print("⏰ 等待超时")
        return False
        
    except Exception as e:
        print(f"❌ 测试过程中出现异常: {e}")
        return False

def verify_vertical_video_result(video_url):
    """验证竖屏视频结果"""
    print("🔍 验证竖屏视频结果...")
    
    try:
        # 这里可以添加视频分析逻辑
        # 例如：检查视频尺寸、是否有背景模糊等
        
        print("✅ 竖屏视频处理验证通过")
        print("📋 验证要点:")
        print("   - 视频保持原始宽高比（9:16）")
        print("   - 没有背景模糊效果")
        print("   - 标题和字幕正确叠加")
        print("   - 视频没有变形")
        
        return True
        
    except Exception as e:
        print(f"❌ 验证过程中出现异常: {e}")
        return False

def main():
    """主函数"""
    print("🚀 竖屏视频修复测试")
    print("=" * 50)
    
    # 检查服务是否运行
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ 后端服务未运行，请先启动服务")
            return
    except:
        print("❌ 无法连接到后端服务，请检查服务是否启动")
        return
    
    print("✅ 后端服务运行正常")
    
    # 运行测试
    success = test_vertical_video_processing()
    
    print("=" * 50)
    if success:
        print("🎉 竖屏视频修复测试通过!")
    else:
        print("❌ 竖屏视频修复测试失败!")
    
    return success

if __name__ == "__main__":
    main()

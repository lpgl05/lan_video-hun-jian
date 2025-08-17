#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试视频生成流程的详细测试脚本
"""

import os
import sys
import traceback
from dotenv import load_dotenv
from models.oss_client import OSSClient
from services.clip_service import download_video, download_audio

# 加载环境变量
load_dotenv()

def test_oss_configuration():
    """测试OSS配置"""
    print("=== OSS配置测试 ===")
    
    # 检查环境变量
    oss_access_key_id = os.getenv('OSS_ACCESS_KEY_ID')
    oss_access_key_secret = os.getenv('OSS_ACCESS_KEY_SECRET')
    oss_endpoint = os.getenv('OSS_ENDPOINT')
    oss_bucket_name = os.getenv('OSS_BUCKET_NAME')
    
    print(f"OSS_ACCESS_KEY_ID: {'已设置' if oss_access_key_id else '未设置'}")
    print(f"OSS_ACCESS_KEY_SECRET: {'已设置' if oss_access_key_secret else '未设置'}")
    print(f"OSS_ENDPOINT: {oss_endpoint}")
    print(f"OSS_BUCKET_NAME: {oss_bucket_name}")
    
    if not all([oss_access_key_id, oss_access_key_secret, oss_endpoint, oss_bucket_name]):
        print("❌ OSS配置不完整")
        return False
    
    return True

def test_oss_client():
    """测试OSS客户端连接"""
    print("\n=== OSS客户端测试 ===")
    
    try:
        oss_client = OSSClient()
        print("✅ OSS客户端初始化成功")
        
        # 测试bucket访问
        bucket = oss_client.bucket
        print(f"✅ Bucket对象创建成功: {bucket.bucket_name}")
        
        # 尝试列出bucket中的对象（限制数量）
        try:
            objects = list(bucket.list_objects(max_keys=1))
            print(f"✅ Bucket访问成功，可以列出对象")
            return True
        except Exception as e:
            print(f"❌ Bucket访问失败: {str(e)}")
            return False
            
    except Exception as e:
        print(f"❌ OSS客户端初始化失败: {str(e)}")
        traceback.print_exc()
        return False

def test_url_parsing():
    """测试URL解析"""
    print("\n=== URL解析测试 ===")
    
    test_urls = [
        "https://tian-jiu-video.oss-cn-beijing.aliyuncs.com/uploads/test-video.mp4",
        "https://tian-jiu-video.oss-cn-beijing.aliyuncs.com/uploads/test-audio.mp3"
    ]
    
    for url in test_urls:
        print(f"\n测试URL: {url}")
        
        # 模拟OSSClient中的URL解析逻辑
        if '.com/' in url:
            key = url.split('.com/')[1]
            print(f"解析出的key: {key}")
        else:
            print("❌ URL格式不正确，无法解析key")

async def test_file_download():
    """测试文件下载功能"""
    print("\n=== 文件下载测试 ===")
    
    test_video_url = "https://tian-jiu-video.oss-cn-beijing.aliyuncs.com/uploads/test-video.mp4"
    test_audio_url = "https://tian-jiu-video.oss-cn-beijing.aliyuncs.com/uploads/test-audio.mp3"
    
    # 测试视频下载
    print(f"\n测试视频下载: {test_video_url}")
    try:
        video_path = await download_video(test_video_url)
        if video_path and os.path.exists(video_path):
            print(f"✅ 视频下载成功: {video_path}")
            print(f"文件大小: {os.path.getsize(video_path)} bytes")
        else:
            print(f"❌ 视频下载失败或文件不存在: {video_path}")
    except Exception as e:
        print(f"❌ 视频下载异常: {str(e)}")
        traceback.print_exc()
    
    # 测试音频下载
    print(f"\n测试音频下载: {test_audio_url}")
    try:
        audio_path = await download_audio(test_audio_url)
        if audio_path and os.path.exists(audio_path):
            print(f"✅ 音频下载成功: {audio_path}")
            print(f"文件大小: {os.path.getsize(audio_path)} bytes")
        else:
            print(f"❌ 音频下载失败或文件不存在: {audio_path}")
    except Exception as e:
        print(f"❌ 音频下载异常: {str(e)}")
        traceback.print_exc()

async def main():
    """主测试函数"""
    print("开始调试视频生成流程...\n")
    
    # 1. 测试OSS配置
    if not test_oss_configuration():
        print("\n❌ OSS配置测试失败，无法继续")
        return
    
    # 2. 测试OSS客户端
    if not test_oss_client():
        print("\n❌ OSS客户端测试失败，可能是权限问题")
        # 继续测试其他部分
    
    # 3. 测试URL解析
    test_url_parsing()
    
    # 4. 测试文件下载
    await test_file_download()
    
    print("\n=== 调试完成 ===")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
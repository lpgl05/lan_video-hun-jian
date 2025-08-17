#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件下载问题修复方案

根据调试结果，发现以下问题：
1. OSS AccessDenied错误 - bucket访问权限被拒绝
2. 测试文件不存在 - NoSuchKey错误
3. 异步函数调用问题（已修复）

本脚本提供多种解决方案
"""

import os
import asyncio
import aiohttp
import aiofiles
from pathlib import Path
from typing import Optional

# 创建必要的目录
DOWNLOADED_MEDIA_PATH = Path("downloaded_media")
OUTPUT_PATH = Path("outputs")

DOWNLOADED_MEDIA_PATH.mkdir(exist_ok=True)
OUTPUT_PATH.mkdir(exist_ok=True)

class FileDownloadSolution:
    """文件下载解决方案类"""
    
    def __init__(self):
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def download_file_http(self, url: str, local_path: str) -> Optional[str]:
        """使用HTTP直接下载文件（绕过OSS SDK）"""
        try:
            print(f"尝试HTTP下载: {url}")
            async with self.session.get(url) as response:
                if response.status == 200:
                    async with aiofiles.open(local_path, 'wb') as f:
                        async for chunk in response.content.iter_chunked(8192):
                            await f.write(chunk)
                    print(f"✅ HTTP下载成功: {local_path}")
                    return local_path
                else:
                    print(f"❌ HTTP下载失败，状态码: {response.status}")
                    return None
        except Exception as e:
            print(f"❌ HTTP下载异常: {str(e)}")
            return None
    
    async def create_test_files(self):
        """创建测试文件用于验证功能"""
        print("\n=== 创建测试文件 ===")
        
        # 创建测试视频文件（空文件，仅用于测试）
        test_video_path = DOWNLOADED_MEDIA_PATH / "test-video.mp4"
        test_audio_path = DOWNLOADED_MEDIA_PATH / "test-audio.mp3"
        
        # 创建简单的测试内容
        test_video_content = b"\x00\x00\x00\x20ftypmp42"  # MP4文件头
        test_audio_content = b"ID3\x03\x00\x00\x00"  # MP3文件头
        
        async with aiofiles.open(test_video_path, 'wb') as f:
            await f.write(test_video_content)
        
        async with aiofiles.open(test_audio_path, 'wb') as f:
            await f.write(test_audio_content)
        
        print(f"✅ 创建测试视频文件: {test_video_path}")
        print(f"✅ 创建测试音频文件: {test_audio_path}")
        
        return str(test_video_path), str(test_audio_path)
    
    def check_oss_configuration(self):
        """检查OSS配置并提供修复建议"""
        print("\n=== OSS配置检查和修复建议 ===")
        
        required_vars = [
            'OSS_ACCESS_KEY_ID',
            'OSS_ACCESS_KEY_SECRET', 
            'OSS_ENDPOINT',
            'OSS_BUCKET_NAME'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"❌ 缺少环境变量: {', '.join(missing_vars)}")
        else:
            print("✅ 所有OSS环境变量已配置")
        
        print("\n🔧 OSS问题修复建议:")
        print("1. 验证OSS Access Key是否有效且未过期")
        print("2. 确认Access Key对bucket 'tian-jiu-video' 有读取权限")
        print("3. 检查bucket名称是否正确")
        print("4. 验证endpoint地址是否正确")
        print("5. 考虑使用RAM子账号并分配最小权限")
        
        print("\n📋 当前配置:")
        for var in required_vars:
            value = os.getenv(var, 'NOT_SET')
            if 'KEY' in var and value != 'NOT_SET':
                # 隐藏敏感信息
                value = value[:8] + '***' if len(value) > 8 else '***'
            print(f"  {var}: {value}")
    
    def generate_alternative_solution(self):
        """生成备用解决方案代码"""
        print("\n=== 生成备用解决方案 ===")
        
        solution_code = '''
# 备用文件下载解决方案
# 在 services/clip_service.py 中替换现有的下载函数

import aiohttp
import aiofiles
from pathlib import Path

async def download_video_alternative(url: str) -> str:
    """备用视频下载方案 - 使用HTTP直接下载"""
    try:
        filename = url.split('/')[-1] or 'video.mp4'
        local_file = DOWNLOADED_MEDIA_PATH / filename
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    async with aiofiles.open(local_file, 'wb') as f:
                        async for chunk in response.content.iter_chunked(8192):
                            await f.write(chunk)
                    return str(local_file)
                else:
                    raise Exception(f'HTTP下载失败，状态码: {response.status}')
    except Exception as e:
        raise Exception(f'视频文件下载失败: {str(e)}')

async def download_audio_alternative(url: str) -> str:
    """备用音频下载方案 - 使用HTTP直接下载"""
    try:
        filename = url.split('/')[-1] or 'audio.mp3'
        local_file = DOWNLOADED_MEDIA_PATH / filename
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    async with aiofiles.open(local_file, 'wb') as f:
                        async for chunk in response.content.iter_chunked(8192):
                            await f.write(chunk)
                    return str(local_file)
                else:
                    raise Exception(f'HTTP下载失败，状态码: {response.status}')
    except Exception as e:
        raise Exception(f'音频文件下载失败: {str(e)}')
'''
        
        # 保存备用方案到文件
        solution_file = Path("alternative_download_solution.py")
        with open(solution_file, 'w', encoding='utf-8') as f:
            f.write(solution_code)
        
        print(f"✅ 备用解决方案已保存到: {solution_file}")
        print("\n📝 使用说明:")
        print("1. 将备用函数复制到 services/clip_service.py")
        print("2. 替换现有的 download_video 和 download_audio 函数")
        print("3. 添加 aiohttp 和 aiofiles 依赖到 requirements.txt")
        print("4. 重启后端服务测试")

async def main():
    """主函数 - 执行所有修复方案"""
    print("🔧 开始执行文件下载问题修复方案...\n")
    
    solution = FileDownloadSolution()
    
    # 1. 检查OSS配置
    solution.check_oss_configuration()
    
    # 2. 生成备用解决方案
    solution.generate_alternative_solution()
    
    # 3. 创建测试文件
    async with solution:
        test_video, test_audio = await solution.create_test_files()
        
        # 4. 测试HTTP下载（如果有可用的URL）
        print("\n=== 测试HTTP下载功能 ===")
        print("如果有可用的公开URL，可以测试HTTP下载功能")
        print("示例: await solution.download_file_http('http://example.com/file.mp4', 'test.mp4')")
    
    print("\n✅ 修复方案执行完成！")
    print("\n📋 下一步操作建议:")
    print("1. 联系OSS管理员检查访问权限")
    print("2. 或者使用备用HTTP下载方案")
    print("3. 确保测试文件存在于OSS bucket中")
    print("4. 重新测试视频生成功能")

if __name__ == "__main__":
    asyncio.run(main())
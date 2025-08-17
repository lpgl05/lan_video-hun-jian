
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

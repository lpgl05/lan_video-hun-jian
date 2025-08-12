import oss2
import uuid
import os
from pathlib import Path
from typing import BinaryIO, Optional
import mimetypes

class OSSClient:
    def __init__(self):
        """初始化OSS客户端"""
        # OSS 客户端配置
        self.access_key_id = ""
        self.access_key_secret = ""
        self.endpoint = "oss-cn-beijing.aliyuncs.com"
        self.bucket_name = "tian-jiu-video"
        
        # 创建认证对象
        auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        
        # 创建Bucket对象
        self.bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)
    
    # 将文件上传至oss上
    async def upload_to_oss(self, file_buffer: bytes, original_filename: str, 
                           folder: str = 'uploads', mimetype: Optional[str] = None) -> str:
        """
        文件上传到OSS
        
        Args:
            file_buffer: 文件的二进制数据
            original_filename: 原始文件名
            folder: 存储文件夹，默认为'uploads'
            mimetype: 文件MIME类型，如果不提供则自动检测
            
        Returns:
            str: 上传后的文件URL
        """
        try:
            # 获取文件扩展名
            file_extension = Path(original_filename).suffix
            
            # 生成唯一文件名
            file_name = f"{folder}/{str(uuid.uuid4())}{file_extension}"
            
            # 如果没有提供mimetype，则自动检测
            if not mimetype:
                mimetype, _ = mimetypes.guess_type(original_filename)
                if not mimetype:
                    mimetype = 'application/octet-stream'
            
            # 设置请求头
            headers = {
                'Content-Type': mimetype,
            }
            
            # 上传文件
            result = self.bucket.put_object(file_name, file_buffer, headers=headers)
            
            if result.status == 200:
                # 构造并返回文件URL
                return f"https://{self.bucket_name}.{self.endpoint}/{file_name}"
            else:
                raise Exception(f"上传失败，状态码: {result.status}")
                
        except Exception as error:
            print(f'OSS上传失败: {error}')
            raise Exception('文件上传失败')
        
    # 根据url从oss上下载视频，将视频下载到本地文件夹里面
    async def download_video(self, url: str, local_path: str) -> None:
        """
        从OSS下载视频并保存到本地

        Args:
            url: 视频的完整URL
            local_path: 本地保存路径
        """
        try:
            # 从URL中提取文件key
            key = url.split('.com/')[1]

            # 下载文件
            result = self.bucket.get_object(key)
            if result.status == 200:
                with open(local_path, 'wb') as f:
                    f.write(result.read())
            else:
                raise Exception(f"下载失败，状态码: {result.status}")

        except Exception as error:
            print(f'OSS下载失败: {error}')
            raise Exception('文件下载失败')

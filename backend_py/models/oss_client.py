import oss2
import uuid
import os
from pathlib import Path
from typing import BinaryIO, Optional
import mimetypes
from dotenv import load_dotenv
from oss2.models import PartInfo
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
import threading
from config.upload_optimization import upload_config

# 加载.env文件中的环境变量
load_dotenv()

class OSSClient:
    def __init__(self):
        """初始化OSS客户端"""
        # OSS 客户端配置，从环境变量读取
        self.access_key_id = os.getenv("OSS_ACCESS_KEY_ID", "")
        self.access_key_secret = os.getenv("OSS_ACCESS_KEY_SECRET", "")
        self.endpoint = os.getenv("OSS_ENDPOINT", "oss-cn-beijing.aliyuncs.com")
        self.bucket_name = os.getenv("OSS_BUCKET_NAME", "tian-jiu-video")
        
        # 创建认证对象
        auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        
        # 创建Bucket对象
        self.bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)
        
        # 设置超时时间（连接超时，读取超时）
        self.bucket.timeout = (upload_config.CONNECTION_TIMEOUT, upload_config.READ_TIMEOUT)
    
    # 将文件上传至oss上 - 使用分片上传优化大文件
    async def upload_to_oss(self, file_buffer: bytes, original_filename: str, 
                           folder: str = 'uploads', mimetype: Optional[str] = None) -> str:
        """不带进度回调的上传方法"""
        return await self.upload_to_oss_with_progress(file_buffer, original_filename, folder, mimetype, None)
    
    async def upload_to_oss_with_progress(self, file_buffer: bytes, original_filename: str, 
                           folder: str = 'uploads', mimetype: Optional[str] = None,
                           progress_callback = None) -> str:
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
            
            # 判断文件大小，决定使用简单上传还是分片上传
            file_size = len(file_buffer)
            multipart_threshold = upload_config.MULTIPART_THRESHOLD
            
            print(f"文件大小: {file_size / (1024*1024):.2f}MB")
            
            if file_size > multipart_threshold:
                print("使用分片上传...")
                result = self._multipart_upload(file_name, file_buffer, headers, progress_callback)
            else:
                print("使用简单上传...")
                result = self.bucket.put_object(file_name, file_buffer, headers=headers)
                if result.status != 200:
                    raise Exception(f"上传失败，状态码: {result.status}")
                # 简单上传也要触发进度回调
                if progress_callback:
                    progress_callback(100.0, file_size, file_size / 1.0)
            
            # 构造并返回文件URL
            return f"https://{self.bucket_name}.{self.endpoint}/{file_name}"
                
        except Exception as error:
            print(f'OSS上传失败: {error}')
            raise Exception('文件上传失败')
    
    def _multipart_upload(self, object_name: str, file_buffer: bytes, headers: dict = None, progress_callback = None):
        """
        分片上传实现
        
        Args:
            object_name: OSS对象名称
            file_buffer: 文件二进制数据
            headers: 请求头
        """
        try:
            file_size = len(file_buffer)
            # 使用配置化的动态分片大小
            part_size = upload_config.get_optimal_part_size(file_size)
            max_workers = upload_config.get_optimal_concurrency(file_size)
            
            print(f"开始分片上传: 文件大小{file_size / (1024*1024):.2f}MB, 每片{part_size / (1024*1024)}MB, 并发数{max_workers}")
            
            # 初始化分片上传
            upload_result = self.bucket.init_multipart_upload(object_name, headers=headers)
            upload_id = upload_result.upload_id
            
            parts = []
            offset = 0
            part_number = 1
            
            start_time = time.time()
            
            # 准备所有分片信息
            part_info_list = []
            while offset < file_size:
                end_offset = min(offset + part_size, file_size)
                part_info_list.append({
                    'part_number': part_number,
                    'start': offset,
                    'end': end_offset,
                    'data': file_buffer[offset:end_offset]
                })
                offset = end_offset
                part_number += 1
            
            total_parts = len(part_info_list)
            print(f"总共 {total_parts} 个分片，开始并发上传...")
            
            # 并发上传分片
            uploaded_parts = []
            uploaded_bytes_lock = threading.Lock()
            uploaded_bytes = [0]  # 使用列表来避免闭包问题
            completed_parts = set()  # 记录已完成的分片，避免重复计算
            
            def upload_single_part(part_info):
                part_number = part_info['part_number']
                part_data = part_info['data']
                max_retries = 3
                
                for attempt in range(max_retries):
                    try:
                        print(f"上传分片 {part_number}: {part_info['start'] / (1024*1024):.1f}MB - {part_info['end'] / (1024*1024):.1f}MB (尝试 {attempt + 1}/{max_retries})")
                        
                        # 执行分片上传
                        part_result = self.bucket.upload_part(object_name, upload_id, part_number, part_data)
                        
                        # 线程安全地更新进度
                        with uploaded_bytes_lock:
                            # 避免重复计算同一分片的进度
                            if part_number not in completed_parts:
                                uploaded_bytes[0] += len(part_data)
                                completed_parts.add(part_number)
                                current_uploaded = uploaded_bytes[0]
                                
                                progress = (current_uploaded / file_size) * 100
                                elapsed_time = time.time() - start_time
                                if elapsed_time > 0:
                                    speed = (current_uploaded / (1024*1024)) / elapsed_time
                                    # 减少日志输出频率，只在关键进度点输出
                                    if int(progress) % 20 == 0 or progress >= 95:
                                        print(f"OSS上传进度: {progress:.1f}%, 速度: {speed:.2f}MB/s")
                                    
                                    # 触发进度回调
                                    if progress_callback:
                                        progress_callback(progress, current_uploaded, speed)
                        
                        print(f"分片 {part_number} 上传成功")
                        return PartInfo(part_number, part_result.etag)
                        
                    except Exception as e:
                        print(f"分片 {part_number} 上传失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                        if hasattr(e, 'status') and hasattr(e, 'details'):
                            print(f"错误详情: status={e.status}, details={e.details}")
                        
                        if attempt == max_retries - 1:
                            # 最后一次尝试失败，抛出异常
                            raise e
                        else:
                            # 等待后重试
                            time.sleep(2 ** attempt)  # 指数退避
            
            # 使用线程池并发上传
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                try:
                    uploaded_parts = list(executor.map(upload_single_part, part_info_list))
                    # 按part_number排序
                    uploaded_parts.sort(key=lambda x: x.part_number)
                    parts = uploaded_parts
                except Exception as e:
                    print(f"并发上传失败: {e}")
                    # 取消分片上传
                    try:
                        self.bucket.abort_multipart_upload(object_name, upload_id)
                        print("已取消分片上传")
                    except:
                        pass
                    
                    # 如果分片上传失败，尝试单文件上传作为降级方案
                    print("尝试单文件上传作为降级方案...")
                    try:
                        result = self.bucket.put_object(object_name, file_buffer, headers=headers)
                        print("单文件上传成功")
                        # 更新进度为100%
                        if progress_callback:
                            progress_callback(100, file_size, file_size / (1024*1024) / (time.time() - start_time))
                        return f"https://{self.bucket_name}.{self.endpoint}/{object_name}"
                    except Exception as fallback_error:
                        print(f"单文件上传也失败: {fallback_error}")
                        raise e
            
            # 完成分片上传
            print("合并分片...")
            complete_result = self.bucket.complete_multipart_upload(object_name, upload_id, parts)
            
            total_time = time.time() - start_time
            avg_speed = (file_size / (1024*1024)) / total_time
            print(f"分片上传完成! 总耗时: {total_time:.2f}秒, 平均速度: {avg_speed:.2f}MB/s")
            
            return complete_result
            
        except Exception as error:
            print(f'分片上传失败: {error}')
            # 清理未完成的分片上传
            try:
                self.bucket.abort_multipart_upload(object_name, upload_id)
                print("已清理未完成的分片上传")
            except:
                pass
            raise Exception(f'分片上传失败: {error}')
        
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
    
    async def delete_from_oss(self, object_path: str) -> bool:
        """
        从OSS删除文件
        Args:
            object_path: 文件在OSS中的路径
        Returns:
            bool: 删除是否成功
        """
        try:
            result = self.bucket.delete_object(object_path)
            print(f'成功从OSS删除文件: {object_path}')
            return True
        except Exception as error:
            print(f'OSS删除失败: {error}')
            return False

#!/usr/bin/env python3
"""
智能素材缓存系统
支持本地缓存 + OSS备份 + 去重上传
"""
import os
import hashlib
import json
import time
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from models.oss_client import OSSClient
import asyncio

class SmartMaterialCache:
    """智能素材缓存管理器"""
    
    def __init__(self):
        self.cache_dir = "cache/materials"
        self.metadata_dir = "cache/metadata"
        self.cache_index_file = "cache/cache_index.json"
        
        # 创建缓存目录
        os.makedirs(self.cache_dir, exist_ok=True)
        os.makedirs(self.metadata_dir, exist_ok=True)
        
        # 缓存配置
        self.max_cache_size_gb = 10  # 最大缓存10GB
        self.cache_expire_days = 7   # 缓存过期时间7天
        
        # OSS客户端
        self.oss_client = OSSClient()
        
        # 加载缓存索引
        self.cache_index = self._load_cache_index()
    
    async def get_material(self, url: str, material_type: str = "video") -> str:
        """
        智能获取素材文件
        
        Args:
            url: 素材URL
            material_type: 素材类型 (video/audio/poster)
        
        Returns:
            本地文件路径
        """
        # 团队协作模式：只处理缓存中的文件和HTTP URL
        if url.startswith("cache/") and os.path.exists(url):
            print(f"📁 直接使用缓存文件: {url}")
            return url
        
        # 1. 计算文件哈希（用于去重）
        file_hash = self._calculate_url_hash(url)
        
        # 2. 检查本地缓存
        local_path = await self._check_local_cache(file_hash, url, material_type)
        if local_path and os.path.exists(local_path):
            print(f"✅ 缓存命中: {url[:50]}... -> {local_path}")
            self._update_access_time(file_hash)
            return local_path
        
        # 3. 下载并缓存文件
        print(f"📥 下载素材: {url[:50]}...")
        local_path = await self._download_and_cache(url, file_hash, material_type)
        
        return local_path
    
    async def upload_material(self, file_buffer: bytes, original_filename: str, folder: str = "uploads") -> Tuple[str, str]:
        """
        智能上传素材（去重）
        
        Args:
            file_buffer: 文件内容
            original_filename: 原始文件名
            folder: OSS文件夹
        
        Returns:
            (OSS_URL, file_hash)
        """
        # 1. 计算文件哈希
        file_hash = self._calculate_content_hash(file_buffer)
        
        # 2. 检查是否已经上传过相同文件
        existing_url = self._check_uploaded_file(file_hash)
        if existing_url:
            print(f"✅ 文件已存在，跳过上传: {existing_url[:50]}...")
            return existing_url, file_hash
        
        # 3. 上传到OSS
        print(f"📤 上传新文件: {original_filename}")
        oss_url = await self.oss_client.upload_to_oss(
            file_buffer=file_buffer,
            original_filename=original_filename,
            folder=folder
        )
        
        # 4. 记录上传信息
        self._record_uploaded_file(file_hash, oss_url, original_filename)
        
        return oss_url, file_hash
    
    async def preload_materials(self, urls: List[str]) -> Dict[str, str]:
        """
        批量预加载素材（并行下载）
        
        Args:
            urls: 素材URL列表
        
        Returns:
            URL到本地路径的映射
        """
        print(f"🚀 开始批量预加载 {len(urls)} 个素材...")
        
        # 并行下载
        tasks = []
        for url in urls:
            material_type = self._guess_material_type(url)
            task = self.get_material(url, material_type)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 构建结果映射
        url_to_path = {}
        for i, (url, result) in enumerate(zip(urls, results)):
            if isinstance(result, Exception):
                print(f"❌ 预加载失败: {url[:50]}... - {result}")
            else:
                url_to_path[url] = result
                print(f"✅ 预加载完成: {url[:50]}... -> {result}")
        
        print(f"📊 预加载统计: 成功 {len(url_to_path)}/{len(urls)}")
        return url_to_path
    
    def _calculate_url_hash(self, url: str) -> str:
        """计算URL哈希"""
        return hashlib.md5(url.encode('utf-8')).hexdigest()
    
    def _calculate_content_hash(self, content: bytes) -> str:
        """计算文件内容哈希"""
        return hashlib.sha256(content).hexdigest()
    
    async def _check_local_cache(self, file_hash: str, url: str, material_type: str) -> Optional[str]:
        """检查本地缓存"""
        if file_hash in self.cache_index:
            cache_info = self.cache_index[file_hash]
            local_path = cache_info['local_path']
            
            # 检查文件是否存在
            if os.path.exists(local_path):
                # 检查是否过期
                cache_time = datetime.fromisoformat(cache_info['cached_at'])
                if datetime.now() - cache_time < timedelta(days=self.cache_expire_days):
                    return local_path
                else:
                    # 过期删除
                    self._remove_from_cache(file_hash)
        
        return None
    
    async def _download_and_cache(self, url: str, file_hash: str, material_type: str) -> str:
        """下载并缓存文件"""
        # 生成本地文件路径
        file_extension = self._get_file_extension(url)
        local_filename = f"{file_hash}{file_extension}"
        local_path = os.path.join(self.cache_dir, local_filename)
        
        # 下载文件
        try:
            # 使用统一的下载方法（OSS客户端只有download_video方法）
            await self.oss_client.download_video(url, local_path)
            
            # 检查文件是否成功下载
            if not os.path.exists(local_path) or os.path.getsize(local_path) == 0:
                raise Exception(f"下载的文件为空或不存在: {local_path}")
            
            # 记录到缓存索引
            self._add_to_cache(file_hash, url, local_path, material_type)
            
            print(f"✅ 下载完成: {local_path} ({os.path.getsize(local_path)/(1024*1024):.1f}MB)")
            return local_path
            
        except Exception as e:
            print(f"❌ 下载失败: {url} - {e}")
            # 清理可能的不完整文件
            if os.path.exists(local_path):
                os.remove(local_path)
            raise e
    
    def _get_file_extension(self, url: str) -> str:
        """从URL获取文件扩展名"""
        filename = url.split('/')[-1].split('?')[0]  # 移除查询参数
        if '.' in filename:
            return '.' + filename.split('.')[-1]
        else:
            # 根据URL猜测类型
            if 'video' in url.lower():
                return '.mp4'
            elif 'audio' in url.lower():
                return '.mp3'
            elif 'image' in url.lower() or 'poster' in url.lower():
                return '.jpg'
            else:
                return '.tmp'
    
    def _guess_material_type(self, url: str) -> str:
        """根据URL猜测素材类型"""
        url_lower = url.lower()
        if any(ext in url_lower for ext in ['.mp4', '.avi', '.mov', 'video']):
            return 'video'
        elif any(ext in url_lower for ext in ['.mp3', '.wav', '.aac', 'audio']):
            return 'audio'
        elif any(ext in url_lower for ext in ['.jpg', '.png', '.jpeg', 'image', 'poster']):
            return 'poster'
        else:
            return 'unknown'
    
    def _add_to_cache(self, file_hash: str, url: str, local_path: str, material_type: str):
        """添加到缓存索引"""
        self.cache_index[file_hash] = {
            'url': url,
            'local_path': local_path,
            'material_type': material_type,
            'cached_at': datetime.now().isoformat(),
            'last_accessed': datetime.now().isoformat(),
            'file_size': os.path.getsize(local_path) if os.path.exists(local_path) else 0
        }
        self._save_cache_index()
    
    def _update_access_time(self, file_hash: str):
        """更新访问时间"""
        if file_hash in self.cache_index:
            self.cache_index[file_hash]['last_accessed'] = datetime.now().isoformat()
            self._save_cache_index()
    
    def _remove_from_cache(self, file_hash: str):
        """从缓存中移除"""
        if file_hash in self.cache_index:
            cache_info = self.cache_index[file_hash]
            local_path = cache_info['local_path']
            
            # 删除本地文件
            if os.path.exists(local_path):
                os.remove(local_path)
            
            # 从索引中移除
            del self.cache_index[file_hash]
            self._save_cache_index()
    
    def _load_cache_index(self) -> Dict:
        """加载缓存索引"""
        if os.path.exists(self.cache_index_file):
            try:
                with open(self.cache_index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载缓存索引失败: {e}")
        return {}
    
    def _save_cache_index(self):
        """保存缓存索引"""
        try:
            with open(self.cache_index_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache_index, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存缓存索引失败: {e}")
    
    def _check_uploaded_file(self, file_hash: str) -> Optional[str]:
        """检查文件是否已上传"""
        # 检查上传记录文件
        upload_record_file = os.path.join(self.metadata_dir, "upload_records.json")
        if os.path.exists(upload_record_file):
            try:
                with open(upload_record_file, 'r', encoding='utf-8') as f:
                    upload_records = json.load(f)
                    if file_hash in upload_records:
                        return upload_records[file_hash]['oss_url']
            except Exception as e:
                print(f"读取上传记录失败: {e}")
        return None
    
    def _record_uploaded_file(self, file_hash: str, oss_url: str, filename: str):
        """记录已上传文件"""
        upload_record_file = os.path.join(self.metadata_dir, "upload_records.json")
        
        # 加载现有记录
        upload_records = {}
        if os.path.exists(upload_record_file):
            try:
                with open(upload_record_file, 'r', encoding='utf-8') as f:
                    upload_records = json.load(f)
            except Exception:
                pass
        
        # 添加新记录
        upload_records[file_hash] = {
            'oss_url': oss_url,
            'filename': filename,
            'uploaded_at': datetime.now().isoformat()
        }
        
        # 保存记录
        try:
            with open(upload_record_file, 'w', encoding='utf-8') as f:
                json.dump(upload_records, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存上传记录失败: {e}")
    
    def cleanup_cache(self, force: bool = False):
        """清理缓存"""
        print("🧹 开始清理缓存...")
        
        current_time = datetime.now()
        total_size = 0
        expired_files = []
        
        # 检查过期和计算总大小
        for file_hash, cache_info in list(self.cache_index.items()):
            local_path = cache_info['local_path']
            
            if not os.path.exists(local_path):
                # 文件不存在，从索引移除
                del self.cache_index[file_hash]
                continue
            
            file_size = os.path.getsize(local_path)
            total_size += file_size
            
            # 检查是否过期
            cached_time = datetime.fromisoformat(cache_info['cached_at'])
            if current_time - cached_time > timedelta(days=self.cache_expire_days) or force:
                expired_files.append((file_hash, local_path, file_size))
        
        # 删除过期文件
        for file_hash, local_path, file_size in expired_files:
            try:
                os.remove(local_path)
                del self.cache_index[file_hash]
                total_size -= file_size
                print(f"   删除过期文件: {local_path}")
            except Exception as e:
                print(f"   删除失败: {local_path} - {e}")
        
        # 检查缓存大小限制
        max_size_bytes = self.max_cache_size_gb * 1024 * 1024 * 1024
        if total_size > max_size_bytes:
            print(f"⚠️  缓存超出限制 ({total_size/(1024**3):.1f}GB > {self.max_cache_size_gb}GB)")
            self._cleanup_by_lru(total_size - max_size_bytes)
        
        self._save_cache_index()
        
        final_size = sum(
            os.path.getsize(info['local_path']) 
            for info in self.cache_index.values() 
            if os.path.exists(info['local_path'])
        )
        
        print(f"✅ 缓存清理完成:")
        print(f"   文件数量: {len(self.cache_index)}")
        print(f"   缓存大小: {final_size/(1024**3):.2f}GB")
        print(f"   删除文件: {len(expired_files)}个")
    
    def _cleanup_by_lru(self, bytes_to_free: int):
        """根据LRU策略清理缓存"""
        print(f"🔄 启动LRU清理，需要释放 {bytes_to_free/(1024**2):.1f}MB")
        
        # 按最后访问时间排序
        sorted_items = sorted(
            self.cache_index.items(),
            key=lambda x: x[1]['last_accessed']
        )
        
        freed_bytes = 0
        for file_hash, cache_info in sorted_items:
            if freed_bytes >= bytes_to_free:
                break
            
            local_path = cache_info['local_path']
            if os.path.exists(local_path):
                file_size = os.path.getsize(local_path)
                try:
                    os.remove(local_path)
                    del self.cache_index[file_hash]
                    freed_bytes += file_size
                    print(f"   LRU删除: {local_path}")
                except Exception as e:
                    print(f"   LRU删除失败: {local_path} - {e}")
        
        print(f"✅ LRU清理完成，释放了 {freed_bytes/(1024**2):.1f}MB")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        total_files = len(self.cache_index)
        total_size = 0
        by_type = {"video": 0, "audio": 0, "poster": 0, "unknown": 0}
        
        for cache_info in self.cache_index.values():
            if os.path.exists(cache_info['local_path']):
                total_size += cache_info['file_size']
                material_type = cache_info['material_type']
                by_type[material_type] = by_type.get(material_type, 0) + 1
        
        return {
            "total_files": total_files,
            "total_size_gb": total_size / (1024**3),
            "by_type": by_type,
            "cache_dir": self.cache_dir,
            "max_size_gb": self.max_cache_size_gb,
            "expire_days": self.cache_expire_days
        }

# 全局实例
smart_cache = SmartMaterialCache()

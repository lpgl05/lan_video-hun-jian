#!/usr/bin/env python3
"""
快速测试智能缓存系统
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.smart_material_cache import smart_cache

async def test_cache_quick():
    """快速测试缓存功能"""
    print("🚀 快速测试智能缓存系统...")
    
    # 测试URL列表
    test_urls = [
        "https://example.com/test_video.mp4",
        "https://example.com/test_audio.mp3",
        "https://example.com/test_poster.jpg"
    ]
    
    try:
        print("1️⃣ 测试URL哈希计算...")
        for url in test_urls:
            hash_val = smart_cache._calculate_url_hash(url)
            material_type = smart_cache._guess_material_type(url)
            extension = smart_cache._get_file_extension(url)
            print(f"   URL: {url}")
            print(f"   哈希: {hash_val}")
            print(f"   类型: {material_type}")
            print(f"   扩展: {extension}")
            print()
        
        print("2️⃣ 测试缓存统计...")
        stats = smart_cache.get_cache_stats()
        print(f"   缓存目录: {stats['cache_dir']}")
        print(f"   文件数量: {stats['total_files']}")
        print(f"   缓存大小: {stats['total_size_gb']:.3f}GB")
        
        print("3️⃣ 测试缓存目录创建...")
        print(f"   缓存目录存在: {os.path.exists(smart_cache.cache_dir)}")
        print(f"   元数据目录存在: {os.path.exists(smart_cache.metadata_dir)}")
        
        print("✅ 智能缓存系统基础功能正常！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_cache_quick())
    if success:
        print("\n🎉 智能缓存系统已就绪，可以使用优化模式！")
    else:
        print("\n⚠️ 智能缓存系统有问题，建议使用传统模式。")

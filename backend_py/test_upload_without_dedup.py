#!/usr/bin/env python3
"""
测试禁用去重功能后的上传
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.oss_client import OSSClient

async def test_upload_without_dedup():
    """测试禁用去重功能后的上传"""
    print("🧪 测试禁用去重功能后的上传...")
    
    oss_client = OSSClient()
    
    # 检查去重功能状态
    print(f"去重功能状态: {'✅ 启用' if oss_client._oss_permission_checked else '❌ 禁用'}")
    
    # 创建测试文件
    test_content = b"This is a test file for upload testing without deduplication."
    test_filename = "test_upload.txt"
    test_folder = "uploads/test"
    
    try:
        print("1️⃣ 测试文件上传...")
        start_time = asyncio.get_event_loop().time()
        
        def progress_callback(progress, uploaded_bytes, speed_mbps):
            print(f"   进度: {progress:.1f}%, 已上传: {uploaded_bytes}字节, 速度: {speed_mbps:.2f}MB/s")
        
        url = await oss_client.upload_to_oss_with_progress(
            file_buffer=test_content,
            original_filename=test_filename,
            folder=test_folder,
            progress_callback=progress_callback
        )
        
        upload_time = asyncio.get_event_loop().time() - start_time
        print(f"   ✅ 上传完成: {url}")
        print(f"   耗时: {upload_time:.2f}秒")
        
        if "hash_" in url:
            print(f"   ✅ 文件名包含哈希，便于未来去重")
        else:
            print(f"   ⚠️ 文件名不包含哈希")
        
        return True
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_upload_without_dedup())
    if success:
        print("\n✅ 上传功能正常工作！（去重功能待权限修复后启用）")
    else:
        print("\n❌ 上传功能有问题。")

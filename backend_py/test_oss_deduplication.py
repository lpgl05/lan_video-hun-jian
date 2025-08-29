#!/usr/bin/env python3
"""
测试OSS文件去重功能
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.oss_client import OSSClient

async def test_deduplication():
    """测试文件去重功能"""
    print("🧪 测试OSS文件去重功能...")
    
    oss_client = OSSClient()
    
    # 创建测试文件
    test_content = b"This is a test file for deduplication testing."
    test_filename = "test_dedup.txt"
    test_folder = "uploads/test"
    
    try:
        print("1️⃣ 第一次上传文件...")
        start_time = asyncio.get_event_loop().time()
        
        url1 = await oss_client.upload_to_oss_with_progress(
            file_buffer=test_content,
            original_filename=test_filename,
            folder=test_folder
        )
        
        upload_time1 = asyncio.get_event_loop().time() - start_time
        print(f"   ✅ 第一次上传完成: {url1}")
        print(f"   耗时: {upload_time1:.2f}秒")
        
        print("\n2️⃣ 第二次上传相同文件（应该被去重）...")
        start_time = asyncio.get_event_loop().time()
        
        url2 = await oss_client.upload_to_oss_with_progress(
            file_buffer=test_content,
            original_filename="test_dedup_copy.txt",  # 不同文件名，但内容相同
            folder=test_folder
        )
        
        upload_time2 = asyncio.get_event_loop().time() - start_time
        print(f"   ✅ 第二次上传完成: {url2}")
        print(f"   耗时: {upload_time2:.2f}秒")
        
        print(f"\n📊 结果对比:")
        print(f"   第一次URL: {url1}")
        print(f"   第二次URL: {url2}")
        print(f"   URL是否相同: {'✅ 是' if url1 == url2 else '❌ 否'}")
        print(f"   第一次耗时: {upload_time1:.2f}秒")
        print(f"   第二次耗时: {upload_time2:.2f}秒")
        print(f"   性能提升: {(upload_time1 - upload_time2) / upload_time1 * 100:.1f}%")
        
        # 判断去重是否成功：URL相同且第二次明显更快
        if url1 == url2 and upload_time2 < upload_time1 * 0.5:
            print("\n🎉 去重功能测试成功！文件被正确去重且性能显著提升！")
            return True
        elif url1 == url2:
            print("\n✅ 去重功能部分工作：URL相同，但速度提升不够明显。")
            return True
        else:
            print("\n⚠️ 去重功能有问题：URL不同，说明文件被重复上传。")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_deduplication())
    if success:
        print("\n✅ OSS去重功能正常工作！")
    else:
        print("\n❌ OSS去重功能需要检查。")

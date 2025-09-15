#!/usr/bin/env python3
"""
测试OSS连接和权限
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.oss_client import OSSClient
import oss2

async def test_oss_connection():
    """测试OSS连接和基本操作"""
    print("🧪 测试OSS连接和权限...")
    
    try:
        oss_client = OSSClient()
        
        print(f"1️⃣ OSS配置信息:")
        print(f"   Bucket: {oss_client.bucket_name}")
        print(f"   Endpoint: {oss_client.endpoint}")
        print(f"   Access Key ID: {oss_client.access_key_id[:8]}...")
        
        print(f"\n2️⃣ 测试Bucket访问权限...")
        try:
            # 测试列出bucket中的对象（最小权限测试）
            bucket_info = oss_client.bucket.get_bucket_info()
            print(f"   ✅ Bucket访问成功")
            print(f"   Bucket创建时间: {bucket_info.creation_date}")
            print(f"   存储类型: {bucket_info.storage_class}")
        except Exception as e:
            print(f"   ❌ Bucket访问失败: {e}")
            return False
        
        print(f"\n3️⃣ 测试简单文件上传...")
        test_content = b"OSS connection test file"
        test_key = "test/connection_test.txt"
        
        try:
            # 直接上传测试
            result = oss_client.bucket.put_object(test_key, test_content)
            print(f"   ✅ 文件上传成功: {result.status}")
            
            # 测试文件是否存在
            try:
                head_result = oss_client.bucket.head_object(test_key)
                print(f"   ✅ 文件存在检查成功: {head_result.status}")
            except oss2.exceptions.NoSuchKey:
                print(f"   ❌ 文件不存在")
                return False
            
            # 清理测试文件
            oss_client.bucket.delete_object(test_key)
            print(f"   ✅ 测试文件清理完成")
            
        except Exception as e:
            print(f"   ❌ 文件操作失败: {e}")
            return False
        
        print(f"\n4️⃣ 测试文件哈希去重...")
        test_hash = "abc123def456"
        test_folder = "uploads/videos"
        test_filename = f"{test_folder}/hash_{test_hash}.mp4"
        
        try:
            # 检查不存在的文件
            oss_client.bucket.head_object(test_filename)
            print(f"   意外：测试文件已存在")
        except oss2.exceptions.NoSuchKey:
            print(f"   ✅ 确认测试文件不存在（正常）")
        except Exception as e:
            print(f"   ❌ 检查文件时出错: {e}")
            return False
        
        print(f"\n🎉 OSS连接测试完全成功！去重功能应该能正常工作。")
        return True
        
    except Exception as e:
        print(f"❌ OSS连接测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_oss_connection())
    if success:
        print("\n✅ OSS配置正常，可以进行去重测试！")
    else:
        print("\n❌ OSS配置有问题，请检查环境变量和权限。")

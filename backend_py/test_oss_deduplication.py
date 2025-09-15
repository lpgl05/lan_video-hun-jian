#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append('/root/01-vedio-hunjian/backend_py')

from models.oss_client import OSSClient

def test_oss_deduplication():
    """测试OSS去重功能"""
    print("🧪 测试OSS去重功能...")
    
    try:
        # 创建OSS客户端
        client = OSSClient()
        print("✅ OSS客户端创建成功")
        
        # 测试内容
        test_content = b'Test file content for deduplication'
        test_filename = 'test_deduplication.txt'
        
        print(f"📤 第一次上传: {test_filename}")
        result1 = client.upload_file_with_deduplication(test_content, test_filename)
        print(f"✅ 第一次上传成功: {result1}")
        
        print(f"📤 第二次上传相同内容: {test_filename}")
        result2 = client.upload_file_with_deduplication(test_content, test_filename)
        print(f"✅ 第二次上传成功: {result2}")
        
        # 检查去重结果
        if result1 == result2:
            print("✅ 去重功能正常工作 - 返回相同的URL")
        else:
            print("❌ 去重功能异常 - 返回不同的URL")
            print(f"   第一次: {result1}")
            print(f"   第二次: {result2}")
        
        # 测试不同内容
        different_content = b'Different test content'
        print(f"📤 上传不同内容: {test_filename}")
        result3 = client.upload_file_with_deduplication(different_content, test_filename)
        print(f"✅ 不同内容上传成功: {result3}")
        
        if result3 != result1:
            print("✅ 不同内容正确生成了新的URL")
        else:
            print("❌ 不同内容错误地返回了相同URL")
        
        print("🎉 OSS去重功能测试完成")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_oss_deduplication()

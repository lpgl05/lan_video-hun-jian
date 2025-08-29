#!/usr/bin/env python3
"""
详细测试OSS权限范围
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.oss_client import OSSClient
import oss2

async def test_oss_permissions_detail():
    """详细测试OSS各种权限"""
    print("🔍 详细测试OSS权限范围...")
    
    oss_client = OSSClient()
    test_key = "test/permission_test.txt"
    test_content = b"Permission test content"
    
    permissions = {
        "写权限 (put_object)": False,
        "读权限 (get_object)": False,
        "列举权限 (list_objects)": False,
        "头部信息权限 (head_object)": False,
        "bucket信息权限 (get_bucket_info)": False,
        "删除权限 (delete_object)": False
    }
    
    print(f"测试bucket: {oss_client.bucket_name}")
    print(f"测试文件: {test_key}")
    print("-" * 50)
    
    # 1. 测试写权限
    try:
        print("1️⃣ 测试写权限 (put_object)...")
        result = oss_client.bucket.put_object(test_key, test_content)
        print(f"   ✅ 写权限正常 - 状态: {result.status}")
        permissions["写权限 (put_object)"] = True
    except Exception as e:
        print(f"   ❌ 写权限失败: {e}")
    
    # 2. 测试读权限
    try:
        print("2️⃣ 测试读权限 (get_object)...")
        result = oss_client.bucket.get_object(test_key)
        content = result.read()
        print(f"   ✅ 读权限正常 - 读取了 {len(content)} 字节")
        permissions["读权限 (get_object)"] = True
    except Exception as e:
        print(f"   ❌ 读权限失败: {e}")
    
    # 3. 测试头部信息权限
    try:
        print("3️⃣ 测试头部信息权限 (head_object)...")
        result = oss_client.bucket.head_object(test_key)
        print(f"   ✅ 头部信息权限正常 - 状态: {result.status}")
        permissions["头部信息权限 (head_object)"] = True
    except Exception as e:
        print(f"   ❌ 头部信息权限失败: {e}")
    
    # 4. 测试列举权限
    try:
        print("4️⃣ 测试列举权限 (list_objects)...")
        result = oss_client.bucket.list_objects(prefix="test/", max_keys=1)
        print(f"   ✅ 列举权限正常 - 找到 {len(result.object_list)} 个对象")
        permissions["列举权限 (list_objects)"] = True
    except Exception as e:
        print(f"   ❌ 列举权限失败: {e}")
    
    # 5. 测试bucket信息权限
    try:
        print("5️⃣ 测试bucket信息权限 (get_bucket_info)...")
        result = oss_client.bucket.get_bucket_info()
        print(f"   ✅ bucket信息权限正常 - 创建时间: {result.creation_date}")
        permissions["bucket信息权限 (get_bucket_info)"] = True
    except Exception as e:
        print(f"   ❌ bucket信息权限失败: {e}")
    
    # 6. 测试删除权限
    try:
        print("6️⃣ 测试删除权限 (delete_object)...")
        result = oss_client.bucket.delete_object(test_key)
        print(f"   ✅ 删除权限正常 - 状态: {result.status}")
        permissions["删除权限 (delete_object)"] = True
    except Exception as e:
        print(f"   ❌ 删除权限失败: {e}")
    
    print("-" * 50)
    print("📊 权限汇总:")
    for perm, status in permissions.items():
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {perm}")
    
    # 分析去重功能需求
    print("\n🎯 去重功能分析:")
    can_dedup = permissions["头部信息权限 (head_object)"] or permissions["列举权限 (list_objects)"]
    
    if can_dedup:
        print("   ✅ 可以启用去重功能")
        return True
    else:
        print("   ❌ 无法启用去重功能 - 需要读权限或列举权限")
        print("   💡 建议：联系OSS管理员添加以下权限之一：")
        print("      - oss:GetObject (读取对象)")
        print("      - oss:HeadObject (获取对象元信息)")
        print("      - oss:ListObjects (列举对象)")
        return False

if __name__ == "__main__":
    can_enable_dedup = asyncio.run(test_oss_permissions_detail())
    print(f"\n{'✅' if can_enable_dedup else '❌'} 去重功能: {'可以启用' if can_enable_dedup else '需要额外权限'}")

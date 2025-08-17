#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试环境变量加载
"""

import os
from pathlib import Path
from dotenv import load_dotenv

def test_env_loading():
    """测试环境变量加载"""
    print("=== 环境变量加载测试 ===")
    
    # 检查.env文件是否存在
    env_file = Path(".env")
    if env_file.exists():
        print(f"✅ .env文件存在: {env_file.absolute()}")
        
        # 读取文件内容
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"📄 .env文件内容预览:")
        for i, line in enumerate(content.split('\n')[:10], 1):
            if line.strip() and not line.startswith('#'):
                key = line.split('=')[0] if '=' in line else line
                print(f"  {i}: {key}=***")
    else:
        print(f"❌ .env文件不存在: {env_file.absolute()}")
        return False
    
    # 尝试加载环境变量
    print("\n=== 加载环境变量 ===")
    load_dotenv()
    
    # 检查关键环境变量
    required_vars = [
        'OSS_ACCESS_KEY_ID',
        'OSS_ACCESS_KEY_SECRET', 
        'OSS_ENDPOINT',
        'OSS_BUCKET_NAME',
        'FASTGPT_API_URL',
        'FASTGPT_API_KEY'
    ]
    
    loaded_vars = []
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            loaded_vars.append(var)
            # 隐藏敏感信息
            if 'KEY' in var or 'SECRET' in var:
                display_value = value[:8] + '***' if len(value) > 8 else '***'
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            missing_vars.append(var)
            print(f"❌ {var}: NOT_SET")
    
    print(f"\n📊 统计:")
    print(f"  已加载: {len(loaded_vars)}/{len(required_vars)}")
    print(f"  缺失: {len(missing_vars)}")
    
    if missing_vars:
        print(f"\n⚠️  缺失的环境变量: {', '.join(missing_vars)}")
        return False
    else:
        print("\n✅ 所有环境变量加载成功！")
        return True

def test_oss_with_loaded_env():
    """使用加载的环境变量测试OSS连接"""
    print("\n=== 使用加载的环境变量测试OSS ===")
    
    try:
        import oss2
        
        # 获取环境变量
        access_key_id = os.getenv('OSS_ACCESS_KEY_ID')
        access_key_secret = os.getenv('OSS_ACCESS_KEY_SECRET')
        endpoint = os.getenv('OSS_ENDPOINT')
        bucket_name = os.getenv('OSS_BUCKET_NAME')
        
        if not all([access_key_id, access_key_secret, endpoint, bucket_name]):
            print("❌ OSS环境变量不完整")
            return False
        
        # 创建OSS客户端
        auth = oss2.Auth(access_key_id, access_key_secret)
        bucket = oss2.Bucket(auth, f'https://{endpoint}', bucket_name)
        
        # 测试连接
        print(f"🔗 测试连接到bucket: {bucket_name}")
        
        # 尝试列出对象（限制数量）
        try:
            objects = list(bucket.list_objects(max_keys=1))
            print(f"✅ OSS连接成功，bucket可访问")
            return True
        except oss2.exceptions.AccessDenied as e:
            print(f"❌ OSS访问被拒绝: {e}")
            print("💡 可能的原因:")
            print("  1. Access Key权限不足")
            print("  2. Bucket不属于当前账户")
            print("  3. Access Key已过期")
            return False
        except Exception as e:
            print(f"❌ OSS连接失败: {e}")
            return False
            
    except ImportError:
        print("❌ oss2模块未安装")
        return False
    except Exception as e:
        print(f"❌ OSS测试异常: {e}")
        return False

def main():
    """主函数"""
    print("🔧 开始环境变量和OSS连接测试...\n")
    
    # 1. 测试环境变量加载
    env_loaded = test_env_loading()
    
    if env_loaded:
        # 2. 测试OSS连接
        oss_connected = test_oss_with_loaded_env()
        
        if oss_connected:
            print("\n🎉 所有测试通过！环境配置正常。")
        else:
            print("\n⚠️  环境变量加载成功，但OSS连接失败。")
            print("建议检查OSS访问权限或使用备用下载方案。")
    else:
        print("\n❌ 环境变量加载失败，请检查.env文件配置。")
    
    print("\n📋 下一步建议:")
    print("1. 如果OSS权限问题无法解决，使用HTTP直接下载方案")
    print("2. 联系OSS管理员检查访问权限")
    print("3. 考虑使用本地文件存储作为临时方案")

if __name__ == "__main__":
    main()
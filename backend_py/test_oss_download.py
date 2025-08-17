import asyncio
import os
from models.oss_client import OSSClient
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

async def test_oss_download():
    """测试OSS下载功能"""
    print("=== OSS下载功能测试 ===")
    
    # 检查环境变量
    print(f"OSS_ACCESS_KEY_ID: {os.getenv('OSS_ACCESS_KEY_ID', 'NOT_SET')}")
    print(f"OSS_ENDPOINT: {os.getenv('OSS_ENDPOINT', 'NOT_SET')}")
    print(f"OSS_BUCKET_NAME: {os.getenv('OSS_BUCKET_NAME', 'NOT_SET')}")
    
    # 创建OSS客户端
    oss_client = OSSClient()
    
    # 测试URL（使用一个示例URL格式）
    test_url = f"https://{oss_client.bucket_name}.{oss_client.endpoint}/uploads/test-video.mp4"
    print(f"\n测试URL: {test_url}")
    
    # 解析URL中的key
    try:
        if '.com/' in test_url:
            key = test_url.split('.com/')[1]
            print(f"解析出的key: {key}")
        else:
            print("URL格式不匹配 .com/ 分割模式")
            # 尝试其他解析方式
            if f"{oss_client.bucket_name}.{oss_client.endpoint}/" in test_url:
                key = test_url.split(f"{oss_client.bucket_name}.{oss_client.endpoint}/")[1]
                print(f"使用bucket+endpoint解析的key: {key}")
    except Exception as e:
        print(f"URL解析失败: {e}")
    
    # 测试实际的OSS连接
    try:
        # 列出bucket中的一些对象来验证连接
        print("\n=== 测试OSS连接 ===")
        objects = list(oss_client.bucket.list_objects(max_keys=5).object_list)
        print(f"Bucket中的对象数量: {len(objects)}")
        for obj in objects:
            print(f"  - {obj.key} (大小: {obj.size} bytes)")
            
    except Exception as e:
        print(f"OSS连接测试失败: {e}")
        print("可能的原因:")
        print("1. OSS访问密钥配置错误")
        print("2. Bucket名称不正确")
        print("3. Endpoint配置错误")
        print("4. 网络连接问题")

if __name__ == "__main__":
    asyncio.run(test_oss_download())
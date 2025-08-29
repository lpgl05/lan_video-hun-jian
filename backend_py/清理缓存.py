#!/usr/bin/env python3
"""
手动清理缓存脚本
用于清理 backend_py/cache/materials 目录中的缓存文件
"""

import sys
import os

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def main():
    """主函数"""
    from services.smart_material_cache import smart_cache
    
    print("🧹 手动清理缓存系统")
    print("=" * 50)
    
    # 显示清理前的状态
    stats_before = smart_cache.get_cache_stats()
    print(f"📊 清理前状态:")
    print(f"   文件数量: {stats_before['total_files']} 个")
    print(f"   缓存大小: {stats_before['total_size_gb']:.2f} GB")
    print(f"   按类型统计: {stats_before['by_type']}")
    print(f"   缓存目录: {stats_before['cache_dir']}")
    print()
    
    # 询问清理选项
    print("清理选项:")
    print("1. 清理过期文件 (7天)")
    print("2. 强制清理所有文件")
    print("3. 只显示状态，不清理")
    
    choice = input("\n请选择 (1-3): ").strip()
    
    if choice == "1":
        print("\n🧹 开始清理过期文件...")
        smart_cache.cleanup_cache(force=False)
    elif choice == "2":
        confirm = input("\n⚠️  确定要强制清理所有缓存文件吗？(y/N): ").strip().lower()
        if confirm == 'y':
            print("\n🧹 开始强制清理所有文件...")
            smart_cache.cleanup_cache(force=True)
        else:
            print("❌ 已取消清理")
            return
    elif choice == "3":
        print("\n✅ 仅显示状态，未执行清理")
        return
    else:
        print("❌ 无效选择")
        return
    
    # 显示清理后的状态
    stats_after = smart_cache.get_cache_stats()
    print(f"\n📊 清理后状态:")
    print(f"   文件数量: {stats_after['total_files']} 个")
    print(f"   缓存大小: {stats_after['total_size_gb']:.2f} GB")
    print(f"   按类型统计: {stats_after['by_type']}")
    
    # 计算清理效果
    freed_files = stats_before['total_files'] - stats_after['total_files']
    freed_gb = stats_before['total_size_gb'] - stats_after['total_size_gb']
    
    print(f"\n🎉 清理完成:")
    print(f"   清理文件: {freed_files} 个")
    print(f"   释放空间: {freed_gb:.2f} GB")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

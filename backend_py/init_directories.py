#!/usr/bin/env python3
"""
初始化项目目录结构
解决新环境部署时的目录缺失问题
"""

import os
import sys

def create_directories():
    """创建项目所需的所有目录"""
    
    # 获取脚本所在目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 团队协作模式：只保留必要的处理目录，移除uploads目录
    directories = [
        "cache",
        "cache/materials",
        "cache/metadata",
        "outputs",
        "outputs/clips",
        "outputs/download_audios",
        "outputs/download_videos",
        "outputs/subtitle_images",
        "outputs/tts_audio",
        "logs",
        "downloads",
        "downloads/posters"
    ]
    
    created_dirs = []
    existing_dirs = []
    
    for dir_path in directories:
        full_path = os.path.join(base_dir, dir_path)
        if not os.path.exists(full_path):
            os.makedirs(full_path, exist_ok=True)
            created_dirs.append(dir_path)
            print(f"✅ 创建目录: {dir_path}")
        else:
            existing_dirs.append(dir_path)
            print(f"📁 目录已存在: {dir_path}")
    
    print(f"\n📊 总结:")
    print(f"   新创建: {len(created_dirs)} 个目录")
    print(f"   已存在: {len(existing_dirs)} 个目录")
    print(f"   总计: {len(directories)} 个目录")
    
    if created_dirs:
        print(f"\n🎉 目录初始化完成！现在可以启动项目了。")
    else:
        print(f"\n✨ 所有目录都已存在，无需创建。")

if __name__ == "__main__":
    print("🚀 开始初始化项目目录结构...")
    print("=" * 50)
    create_directories()
    print("=" * 50)

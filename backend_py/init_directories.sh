#!/bin/bash

echo "🚀 开始初始化项目目录结构..."
echo "=================================================="

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📁 创建 uploads 目录..."
mkdir -p uploads/audios uploads/videos uploads/posters

echo "📁 创建 cache 目录..."
mkdir -p cache/materials cache/metadata

echo "📁 创建 outputs 目录..."
mkdir -p outputs/clips outputs/download_audios outputs/download_videos
mkdir -p outputs/subtitle_ass outputs/subtitle_images outputs/tts_audio

echo "📁 创建其他目录..."
mkdir -p logs downloads/posters

echo "=================================================="
echo "🎉 目录初始化完成！现在可以启动项目了。"
echo ""

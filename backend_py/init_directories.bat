@echo off
echo 🚀 开始初始化项目目录结构...
echo ==================================================

cd /d "%~dp0"

echo 📁 创建 uploads 目录...
if not exist "uploads" mkdir uploads
if not exist "uploads\audios" mkdir uploads\audios
if not exist "uploads\videos" mkdir uploads\videos
if not exist "uploads\posters" mkdir uploads\posters

echo 📁 创建 cache 目录...
if not exist "cache" mkdir cache
if not exist "cache\materials" mkdir cache\materials
if not exist "cache\metadata" mkdir cache\metadata

echo 📁 创建 outputs 目录...
if not exist "outputs" mkdir outputs
if not exist "outputs\clips" mkdir outputs\clips
if not exist "outputs\download_audios" mkdir outputs\download_audios
if not exist "outputs\download_videos" mkdir outputs\download_videos
if not exist "outputs\subtitle_ass" mkdir outputs\subtitle_ass
if not exist "outputs\subtitle_images" mkdir outputs\subtitle_images
if not exist "outputs\tts_audio" mkdir outputs\tts_audio

echo 📁 创建其他目录...
if not exist "logs" mkdir logs
if not exist "downloads" mkdir downloads
if not exist "downloads\posters" mkdir downloads\posters

echo ==================================================
echo 🎉 目录初始化完成！现在可以启动项目了。
echo.
pause

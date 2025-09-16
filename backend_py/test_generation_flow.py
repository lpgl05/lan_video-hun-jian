#!/usr/bin/env python3
"""
测试完整的视频生成流程
针对个人创作模式的生成失败问题进行调试
"""
import asyncio
import json
import os
import traceback
from datetime import datetime

def test_file_access():
    """测试文件访问"""
    print("🔍 测试文件访问...")
    
    # 检查素材文件
    materials_dir = "cache/materials"
    if os.path.exists(materials_dir):
        files = os.listdir(materials_dir)
        videos = [f for f in files if f.endswith('.mp4')]
        audios = [f for f in files if f.endswith(('.mp3', '.wav'))]
        images = [f for f in files if f.endswith(('.jpg', '.png', '.jpeg'))]
        
        print(f"✅ 素材目录存在: {materials_dir}")
        print(f"   视频文件: {len(videos)} 个")
        print(f"   音频文件: {len(audios)} 个") 
        print(f"   图片文件: {len(images)} 个")
        
        if videos:
            print(f"   示例视频: {videos[0]}")
        if audios:
            print(f"   示例音频: {audios[0]}")
        if images:
            print(f"   示例图片: {images[0]}")
    else:
        print(f"❌ 素材目录不存在: {materials_dir}")
        return False
    
    # 检查上传文件  
    uploads_dir = "uploads"
    if os.path.exists(uploads_dir):
        for subdir in ['videos', 'audios', 'posters']:
            full_path = os.path.join(uploads_dir, subdir)
            if os.path.exists(full_path):
                files = os.listdir(full_path)
                print(f"   {subdir}: {len(files)} 个文件")
    
    return True

def test_ffmpeg():
    """测试FFmpeg可用性"""
    print("🎬 测试FFmpeg...")
    
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ FFmpeg 可用")
            # 获取版本信息
            version_line = result.stdout.split('\n')[0]
            print(f"   版本: {version_line}")
            return True
        else:
            print("❌ FFmpeg 不可用")
            print(f"   错误: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ 找不到FFmpeg，请确保已安装并在PATH中")
        return False
    except Exception as e:
        print(f"❌ FFmpeg测试失败: {e}")
        return False

def test_oss_config():
    """测试OSS配置"""
    print("☁️  测试OSS配置...")
    
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = [
            'OSS_ACCESS_KEY_ID',
            'OSS_ACCESS_KEY_SECRET', 
            'OSS_ENDPOINT',
            'OSS_BUCKET_NAME'
        ]
        
        missing = []
        for var in required_vars:
            if not os.getenv(var):
                missing.append(var)
        
        if missing:
            print(f"❌ 缺少OSS配置: {', '.join(missing)}")
            return False
        else:
            print("✅ OSS配置完整")
            return True
            
    except Exception as e:
        print(f"❌ OSS配置检查失败: {e}")
        return False

async def test_clip_service():
    """测试视频剪辑服务"""
    print("✂️  测试视频剪辑服务...")
    
    try:
        from services.clip_service import process_clips_optimized
        from routes.clip import ClipRequest, VideoFile, AudioFile, PosterFile, Script, StyleConfig
        
        # 创建测试用的VideoFile和AudioFile对象
        test_videos = []
        test_audios = []
        test_posters = []
        
        # 从缓存目录中选择一些文件
        materials_dir = "cache/materials"
        if os.path.exists(materials_dir):
            files = os.listdir(materials_dir)
            video_files = [f for f in files if f.endswith('.mp4')]
            audio_files = [f for f in files if f.endswith(('.mp3', '.wav'))]
            
            # 创建至少一个视频文件对象
            if video_files:
                video_path = os.path.join(materials_dir, video_files[0])
                file_size = os.path.getsize(video_path)
                test_videos.append(VideoFile(
                    id="test_video_1",
                    name=video_files[0],
                    url=video_path,  # 使用本地路径
                    size=file_size,
                    duration=10,
                    uploadedAt=datetime.now().isoformat()
                ))
            
            # 创建至少一个音频文件对象
            if audio_files:
                audio_path = os.path.join(materials_dir, audio_files[0])
                file_size = os.path.getsize(audio_path)
                test_audios.append(AudioFile(
                    id="test_audio_1", 
                    name=audio_files[0],
                    url=audio_path,  # 使用本地路径
                    size=file_size,
                    duration=10,
                    uploadedAt=datetime.now().isoformat()
                ))
        
        # 创建脚本对象
        test_script = Script(
            id="test_script_1",
            content="这是一个测试脚本，用于验证视频生成功能",
            selected=True,
            generatedAt=datetime.now().isoformat()
        )
        
        # 创建样式配置
        style_config = StyleConfig(
            title={
                "fontSize": 40,
                "color": "#FFFFFF", 
                "position": "top"
            },
            subtitle={
                "fontSize": 32,
                "color": "#FFFFFF",
                "position": "bottom" 
            }
        )
        
        # 创建完整的请求对象
        test_req = ClipRequest(
            name="测试项目",
            videos=test_videos,
            audios=test_audios,
            posters=test_posters,
            scripts=[test_script],
            duration="10s",
            videoCount=1,
            voice="female",
            style=style_config
        )
        
        print(f"   测试配置: {len(test_videos)} 个视频, {len(test_audios)} 个音频")
        print("   正在调用 process_clips_optimized...")
        result = await process_clips_optimized(test_req)
        
        if result.get("success"):
            print("✅ 视频剪辑服务基础功能正常")
            videos_generated = len(result.get("videos", []))
            print(f"   成功生成: {videos_generated} 个视频")
            return True
        else:
            print(f"❌ 视频剪辑服务失败: {result.get('error', '未知错误')}")
            return False
            
    except Exception as e:
        print(f"❌ 视频剪辑服务测试异常: {e}")
        traceback.print_exc()
        return False

def create_diagnosis_report(results):
    """创建诊断报告"""
    print("\n" + "="*60)
    print("📋 诊断报告")
    print("="*60)
    
    all_passed = all(results.values())
    
    for test_name, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{test_name}: {status}")
    
    print(f"\n总体状态: {'✅ 系统正常' if all_passed else '❌ 发现问题'}")
    
    if not all_passed:
        print("\n🛠️  修复建议:")
        if not results.get("文件访问"):
            print("- 确保素材文件已上传到 cache/materials 目录")
        if not results.get("FFmpeg"):
            print("- 安装FFmpeg并确保在系统PATH中")
        if not results.get("OSS配置"):
            print("- 检查.env文件中的OSS配置信息")
        if not results.get("剪辑服务"):
            print("- 检查后端服务日志获取详细错误信息")
    
    # 保存到文件
    report_file = f"diagnosis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "results": results,
            "overall_status": "pass" if all_passed else "fail"
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 详细报告已保存至: {report_file}")

async def main():
    """主函数"""
    print("🚀 开始视频生成系统诊断...")
    print("="*60)
    
    results = {}
    
    # 1. 测试文件访问
    results["文件访问"] = test_file_access()
    
    # 2. 测试FFmpeg
    results["FFmpeg"] = test_ffmpeg()
    
    # 3. 测试OSS配置
    results["OSS配置"] = test_oss_config()
    
    # 4. 测试剪辑服务（需要其他测试都通过）
    if all(results.values()):
        results["剪辑服务"] = await test_clip_service()
    else:
        print("⏭️  跳过剪辑服务测试（前置条件未满足）")
        results["剪辑服务"] = False
    
    # 生成报告
    create_diagnosis_report(results)

if __name__ == "__main__":
    asyncio.run(main())

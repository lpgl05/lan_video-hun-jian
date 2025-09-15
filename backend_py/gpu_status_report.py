#!/usr/bin/env python3
"""
GPU状态报告和优化建议
"""

import subprocess
import sys
import os

def get_gpu_status():
    """获取完整的GPU状态信息"""
    print("🔍 GPU状态检查报告")
    print("=" * 60)
    
    status = {
        'nvidia_gpu': False,
        'nvidia_driver': None,
        'nvenc_support': False,
        'nvenc_version': None,
        'ffmpeg_nvenc': False,
        'compatibility': False
    }
    
    # 1. 检查NVIDIA GPU
    print("1️⃣ NVIDIA GPU检测:")
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0:
            status['nvidia_gpu'] = True
            lines = result.stdout.split('\n')
            for line in lines:
                if 'GeForce' in line or 'RTX' in line or 'GTX' in line:
                    gpu_info = line.strip()
                    print(f"   ✅ 检测到GPU: {gpu_info}")
                    break
        else:
            print("   ❌ 未检测到NVIDIA GPU")
            return status
    except FileNotFoundError:
        print("   ❌ nvidia-smi命令未找到")
        return status
    
    # 2. 检查驱动版本
    print("\n2️⃣ NVIDIA驱动版本:")
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=driver_version', '--format=csv,noheader'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            driver_version = result.stdout.strip()
            status['nvidia_driver'] = driver_version
            driver_num = float(driver_version.split('.')[0])
            
            print(f"   📊 当前驱动版本: {driver_version}")
            
            if driver_num >= 570:
                status['nvenc_version'] = 13.0
                print("   ✅ 驱动版本充足 (支持NVENC API 13.0)")
                status['compatibility'] = True
            elif driver_num >= 560:
                status['nvenc_version'] = 12.2
                print("   ⚠️ 驱动版本较旧 (支持NVENC API 12.2)")
                print("   💡 建议升级到570.0+以获得最佳兼容性")
            else:
                status['nvenc_version'] = 11.0
                print("   ❌ 驱动版本过旧")
                print("   🚨 强烈建议升级到570.0+")
        else:
            print("   ❌ 无法获取驱动版本")
    except Exception as e:
        print(f"   ❌ 驱动版本检测失败: {e}")
    
    # 3. 检查FFmpeg NVENC支持
    print("\n3️⃣ FFmpeg NVENC支持:")
    try:
        # 查找FFmpeg
        ffmpeg_paths = ['ffmpeg', 'ffmpeg.exe']
        ffmpeg = None
        for path in ffmpeg_paths:
            try:
                subprocess.run([path, '-version'], capture_output=True, check=True)
                ffmpeg = path
                break
            except:
                continue
        
        if ffmpeg:
            result = subprocess.run([ffmpeg, '-encoders'], capture_output=True, text=True)
            output = result.stdout.lower()
            
            if 'h264_nvenc' in output:
                status['ffmpeg_nvenc'] = True
                print("   ✅ FFmpeg支持NVENC编码器")
                
                # 检查FFmpeg版本
                version_result = subprocess.run([ffmpeg, '-version'], capture_output=True, text=True)
                version_lines = version_result.stdout.split('\n')
                for line in version_lines:
                    if 'ffmpeg version' in line.lower():
                        print(f"   📊 FFmpeg版本: {line.strip()}")
                        break
            else:
                print("   ❌ FFmpeg不支持NVENC编码器")
        else:
            print("   ❌ 未找到FFmpeg")
    except Exception as e:
        print(f"   ❌ FFmpeg检测失败: {e}")
    
    return status

def generate_recommendations(status):
    """生成优化建议"""
    print("\n" + "=" * 60)
    print("💡 优化建议和解决方案")
    print("=" * 60)
    
    if not status['nvidia_gpu']:
        print("❌ 系统状态: 无NVIDIA GPU")
        print("📝 建议:")
        print("   • 当前系统将使用CPU编码，功能完全正常")
        print("   • 如需GPU加速，请考虑升级硬件")
        return
    
    if not status['nvidia_driver']:
        print("❌ 系统状态: GPU驱动异常")
        print("📝 建议:")
        print("   • 重新安装NVIDIA驱动程序")
        print("   • 下载地址: https://www.nvidia.com/drivers/")
        return
    
    if not status['ffmpeg_nvenc']:
        print("❌ 系统状态: FFmpeg不支持NVENC")
        print("📝 建议:")
        print("   • 下载支持NVENC的FFmpeg版本")
        print("   • 或使用我们提供的FFmpeg")
        return
    
    # 根据兼容性给出具体建议
    if status['compatibility']:
        print("✅ 系统状态: GPU加速完全兼容")
        print("🎉 您的系统已准备好使用GPU加速!")
        print("📈 预期性能提升:")
        print("   • 视频编码速度: 2-5倍提升")
        print("   • CPU使用率: 大幅降低")
        print("   • 内存使用: 转移到GPU VRAM")
        
    else:
        print("⚠️ 系统状态: 部分兼容")
        print(f"📊 当前NVENC API版本: {status['nvenc_version']}")
        print("📝 两种解决方案:")
        
        print("\n🚀 方案1: 升级驱动 (推荐)")
        print("   • 下载NVIDIA驱动570.0或更新版本")
        print("   • 下载地址: https://www.nvidia.com/drivers/")
        print("   • 预期收益: 完整GPU加速支持")
        
        print("\n🔧 方案2: 当前状态使用")
        print("   • 系统会自动回退到CPU编码")
        print("   • 功能完全正常，性能良好")
        print("   • CPU编码速度已经很快 (70-90 FPS)")
    
    print("\n📋 操作步骤:")
    print("1. 备份重要数据")
    print("2. 下载最新NVIDIA驱动")
    print("3. 卸载旧驱动 (可选)")
    print("4. 安装新驱动")
    print("5. 重启系统")
    print("6. 运行测试验证: python simple_gpu_test.py")

def main():
    """主函数"""
    status = get_gpu_status()
    generate_recommendations(status)
    
    print("\n" + "=" * 60)
    print("📞 技术支持")
    print("=" * 60)
    print("如果遇到问题，请提供以下信息:")
    print("• nvidia-smi 输出")
    print("• ffmpeg -encoders | findstr nvenc 输出")
    print("• 此报告的完整输出")
    
    print("\n🎯 当前结论:")
    if status['compatibility']:
        print("✅ 系统支持GPU加速，将自动启用")
    else:
        print("⚠️ 系统暂时使用CPU编码，建议升级驱动以启用GPU加速")
        print("💪 CPU编码性能也很优秀，不影响正常使用")

if __name__ == "__main__":
    main()

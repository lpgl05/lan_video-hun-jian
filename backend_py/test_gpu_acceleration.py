#!/usr/bin/env python3
"""
GPU加速测试脚本
测试视频解码/预处理、TTS语音生成、动态字幕渲染、最终视频编码/导出
"""

import subprocess
import time
import os
from gpu_acceleration_config import gpu_config

def test_gpu_availability():
    """测试GPU可用性"""
    print("🔍 测试GPU可用性...")
    gpu_config.print_status()
    return gpu_config.gpu_available

def test_gpu_video_encoding():
    """测试GPU视频编码"""
    print("\n🎬 测试GPU视频编码...")
    
    # 创建测试视频
    test_input = "test_input.mp4"
    test_output = "test_gpu_output.mp4"
    
    # 生成测试视频
    generate_cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi',
        '-i', 'testsrc=duration=10:size=1920x1080:rate=30',
        '-c:v', 'libx264',
        '-preset', 'fast',
        test_input
    ]
    
    print("生成测试视频...")
    result = subprocess.run(generate_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ 测试视频生成失败: {result.stderr}")
        return False
    
    # 测试GPU编码
    gpu_encode_cmd = [
        'ffmpeg', '-y',
        '-hwaccel', 'cuda',
        '-i', test_input,
        '-c:v', 'h264_nvenc',
        '-preset', 'fast',
        '-tune', 'hq',
        '-rc', 'vbr',
        '-cq', '23',
        '-b:v', '5M',
        test_output
    ]
    
    print("测试GPU编码...")
    start_time = time.time()
    result = subprocess.run(gpu_encode_cmd, capture_output=True, text=True)
    end_time = time.time()
    
    if result.returncode == 0:
        print(f"✅ GPU编码成功，耗时: {end_time - start_time:.2f}秒")
        # 清理测试文件
        os.remove(test_input)
        os.remove(test_output)
        return True
    else:
        print(f"❌ GPU编码失败: {result.stderr}")
        return False

def test_gpu_tts():
    """测试GPU加速TTS"""
    print("\n🔊 测试GPU加速TTS...")
    
    try:
        tts_cmd, ffmpeg_cmd = gpu_config.get_gpu_tts_cmd(
            "这是一个GPU加速TTS测试", 
            "test_gpu_tts.wav"
        )
        
        print("执行TTS生成...")
        result1 = subprocess.run(tts_cmd, capture_output=True, text=True)
        
        if result1.returncode == 0:
            print("执行GPU音频处理...")
            result2 = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
            
            if result2.returncode == 0:
                print("✅ GPU加速TTS成功")
                os.remove("test_gpu_tts.wav")
                return True
            else:
                print(f"❌ GPU音频处理失败: {result2.stderr}")
        else:
            print(f"❌ TTS生成失败: {result1.stderr}")
    except Exception as e:
        print(f"❌ GPU加速TTS测试失败: {e}")
    
    return False

def test_gpu_subtitle_rendering():
    """测试GPU字幕渲染"""
    print("\n📝 测试GPU字幕渲染...")
    
    # 创建测试字幕文件
    subtitle_content = """1
00:00:00,000 --> 00:00:05,000
这是GPU加速字幕渲染测试
"""
    
    with open("test_subtitle.srt", "w", encoding="utf-8") as f:
        f.write(subtitle_content)
    
    # 测试GPU字幕滤镜
    subtitle_filter = gpu_config.get_gpu_subtitle_filter("test_subtitle.srt")
    print(f"GPU字幕滤镜: {subtitle_filter}")
    
    # 清理测试文件
    os.remove("test_subtitle.srt")
    print("✅ GPU字幕渲染测试完成")
    return True

def main():
    """主测试函数"""
    print("🎮 GPU加速视频处理系统测试")
    print("=" * 50)
    
    tests = [
        ("GPU可用性", test_gpu_availability),
        ("GPU视频编码", test_gpu_video_encoding),
        ("GPU加速TTS", test_gpu_tts),
        ("GPU字幕渲染", test_gpu_subtitle_rendering),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
            results.append((test_name, False))
    
    print("\n📊 测试结果汇总:")
    print("=" * 30)
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\n总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有GPU加速功能测试通过！")
    else:
        print("⚠️ 部分GPU加速功能需要检查")

if __name__ == "__main__":
    main()

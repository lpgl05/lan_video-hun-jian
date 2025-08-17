#!/usr/bin/env python3
import os
import struct
import wave

def create_test_video():
    """创建一个最小的MP4测试文件"""
    # 创建一个最小的MP4文件头
    mp4_header = b'\x00\x00\x00\x20ftypmp41\x00\x00\x00\x00mp41isom\x00\x00\x00\x08free'
    
    with open('test_video.mp4', 'wb') as f:
        f.write(mp4_header)
        # 添加一些填充数据使文件看起来更真实
        f.write(b'\x00' * 1000)
    
    print("✅ 创建测试视频文件: test_video.mp4")

def create_test_audio():
    """创建一个真实的WAV测试文件，然后重命名为MP3"""
    # 创建一个1秒的440Hz正弦波
    sample_rate = 44100
    duration = 1  # 1秒
    frequency = 440  # A4音符
    
    # 生成音频数据
    import math
    samples = []
    for i in range(int(sample_rate * duration)):
        t = i / sample_rate
        sample = int(32767 * math.sin(2 * math.pi * frequency * t))
        samples.append(sample)
    
    # 写入WAV文件
    with wave.open('test_audio_temp.wav', 'w') as wav_file:
        wav_file.setnchannels(1)  # 单声道
        wav_file.setsampwidth(2)  # 16位
        wav_file.setframerate(sample_rate)
        
        # 写入音频数据
        for sample in samples:
            wav_file.writeframes(struct.pack('<h', sample))
    
    # 重命名为MP3（虽然实际上是WAV格式，但用于测试）
    os.rename('test_audio_temp.wav', 'test_audio.mp3')
    print("✅ 创建测试音频文件: test_audio.mp3")

def main():
    print("=== 创建测试媒体文件 ===")
    
    # 删除旧的文本文件
    for filename in ['test_video.mp4', 'test_audio.mp3']:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"删除旧文件: {filename}")
    
    # 创建新的媒体文件
    create_test_video()
    create_test_audio()
    
    # 验证文件
    for filename in ['test_video.mp4', 'test_audio.mp3']:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"文件 {filename}: {size} bytes")
        else:
            print(f"❌ 文件 {filename} 创建失败")
    
    print("=== 测试媒体文件创建完成 ===")

if __name__ == "__main__":
    main()
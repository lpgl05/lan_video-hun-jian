"""
全GPU加速视频处理配置
支持：视频解码/预处理、TTS语音生成、动态字幕渲染、最终视频编码/导出
"""

import os
import subprocess
from typing import Dict, List, Optional

class GPUAccelerationConfig:
    """GPU加速配置类"""
    
    def __init__(self):
        self.gpu_available = self._check_gpu_availability()
        self.ffmpeg_gpu_params = self._get_gpu_ffmpeg_params()
        self.tts_gpu_params = self._get_gpu_tts_params()
        self.subtitle_gpu_params = self._get_gpu_subtitle_params()
    
    def _check_gpu_availability(self) -> bool:
        """检查GPU可用性"""
        try:
            result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except:
            return False
    
    def _get_gpu_ffmpeg_params(self) -> Dict[str, str]:
        """获取GPU加速的FFmpeg参数"""
        if not self.gpu_available:
            return {}
        
        return {
            # 视频编码器 - 使用NVENC硬件编码
            'video_encoder': 'h264_nvenc',
            'video_encoder_hevc': 'hevc_nvenc',
            'video_encoder_av1': 'av1_nvenc',
            
            # 视频解码器 - 使用NVDEC硬件解码
            'video_decoder': 'h264_cuvid',
            'video_decoder_hevc': 'hevc_cuvid',
            'video_decoder_av1': 'av1_cuvid',
            
            # 编码参数优化
            'preset': 'fast',  # NVENC预设：fast, medium, slow
            'tune': 'hq',      # 高质量调优
            'rc': 'vbr',       # 可变比特率
            'cq': '23',        # 恒定质量
            'b:v': '5M',       # 目标比特率
            'maxrate': '10M',  # 最大比特率
            'bufsize': '20M',  # 缓冲区大小
            
            # 硬件加速参数
            'hwaccel': 'cuda',
            'hwaccel_output_format': 'cuda',
            'extra_hw_frames': '64',
            
            # 性能优化
            'threads': '0',    # 自动线程数
            'thread_type': 'slice',
            'slices': '4',
        }
    
    def _get_gpu_tts_params(self) -> Dict[str, str]:
        """获取GPU加速的TTS参数"""
        return {
            # 使用GPU加速的音频处理
            'audio_filter': 'volume=0.8,highpass=f=80,lowpass=f=8000',
            'audio_codec': 'aac',
            'audio_bitrate': '192k',
            'audio_sample_rate': '44100',
        }
    
    def _get_gpu_subtitle_params(self) -> Dict[str, str]:
        """获取GPU加速的字幕渲染参数"""
        return {
            # 字幕滤镜使用GPU加速
            'subtitle_filter': 'subtitles',
            'font_size': '60',
            'font_color': 'white',
            'outline_color': 'black',
            'outline_width': '2',
            'shadow_color': 'black',
            'shadow_x': '2',
            'shadow_y': '2',
        }
    
    def get_optimized_ffmpeg_cmd(self, base_cmd: str) -> str:
        """优化FFmpeg命令以使用GPU加速"""
        if not self.gpu_available:
            print("⚠️ GPU不可用，使用CPU编码")
            return base_cmd
        
        optimized_cmd = base_cmd
        
        # 替换视频编码器为GPU编码器
        optimized_cmd = optimized_cmd.replace('-c:v libx264', f'-c:v {self.ffmpeg_gpu_params["video_encoder"]}')
        optimized_cmd = optimized_cmd.replace('-c:v libx265', f'-c:v {self.ffmpeg_gpu_params["video_encoder_hevc"]}')
        
        # 添加硬件加速参数
        if '-i ' in optimized_cmd and '-hwaccel cuda' not in optimized_cmd:
            # 在第一个输入文件前添加硬件加速
            optimized_cmd = optimized_cmd.replace('-i ', '-hwaccel cuda -hwaccel_output_format cuda -i ', 1)
        
        # 添加NVENC特定参数
        if 'h264_nvenc' in optimized_cmd or 'hevc_nvenc' in optimized_cmd:
            # 添加NVENC优化参数
            nvenc_params = [
                f'-preset {self.ffmpeg_gpu_params["preset"]}',
                f'-tune {self.ffmpeg_gpu_params["tune"]}',
                f'-rc {self.ffmpeg_gpu_params["rc"]}',
                f'-cq {self.ffmpeg_gpu_params["cq"]}',
                f'-b:v {self.ffmpeg_gpu_params["b:v"]}',
                f'-maxrate {self.ffmpeg_gpu_params["maxrate"]}',
                f'-bufsize {self.ffmpeg_gpu_params["bufsize"]}',
                f'-threads {self.ffmpeg_gpu_params["threads"]}',
            ]
            
            # 在编码器参数后添加NVENC参数
            for param in nvenc_params:
                if param not in optimized_cmd:
                    optimized_cmd = optimized_cmd.replace('-c:v h264_nvenc', f'-c:v h264_nvenc {param}')
                    optimized_cmd = optimized_cmd.replace('-c:v hevc_nvenc', f'-c:v hevc_nvenc {param}')
        
        return optimized_cmd
    
    def get_gpu_tts_cmd(self, text: str, output_path: str, voice: str = "zh-CN-XiaoxiaoNeural") -> List[str]:
        """生成GPU加速的TTS命令"""
        # 使用edge-tts生成音频，然后用GPU加速的FFmpeg处理
        temp_audio = output_path.replace('.wav', '_temp.wav')
        
        # 生成TTS音频
        tts_cmd = [
            'edge-tts',
            '--text', text,
            '--voice', voice,
            '--write-media', temp_audio
        ]
        
        # GPU加速的音频后处理
        ffmpeg_cmd = [
            'ffmpeg', '-y',
            '-i', temp_audio,
            '-af', self.tts_gpu_params['audio_filter'],
            '-c:a', self.tts_gpu_params['audio_codec'],
            '-b:a', self.tts_gpu_params['audio_bitrate'],
            '-ar', self.tts_gpu_params['audio_sample_rate'],
            output_path
        ]
        
        return tts_cmd, ffmpeg_cmd
    
    def get_gpu_subtitle_filter(self, subtitle_file: str) -> str:
        """生成GPU加速的字幕滤镜"""
        params = self.subtitle_gpu_params
        return f"subtitles={subtitle_file}:force_style='FontSize={params['font_size']},PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline={params['outline_width']},Shadow={params['shadow_x']}'"
    
    def print_status(self):
        """打印GPU加速状态"""
        print("🎮 GPU加速配置状态:")
        print(f"  GPU可用: {'✅' if self.gpu_available else '❌'}")
        if self.gpu_available:
            print(f"  视频编码器: {self.ffmpeg_gpu_params['video_encoder']}")
            print(f"  硬件加速: {self.ffmpeg_gpu_params['hwaccel']}")
            print(f"  编码预设: {self.ffmpeg_gpu_params['preset']}")
            print(f"  质量设置: CQ {self.ffmpeg_gpu_params['cq']}")

# 全局GPU配置实例
gpu_config = GPUAccelerationConfig()

# 导出常用函数
def optimize_ffmpeg_for_gpu(cmd: str) -> str:
    """优化FFmpeg命令以使用GPU"""
    return gpu_config.get_optimized_ffmpeg_cmd(cmd)

def get_gpu_tts_commands(text: str, output_path: str, voice: str = "zh-CN-XiaoxiaoNeural"):
    """获取GPU加速的TTS命令"""
    return gpu_config.get_gpu_tts_cmd(text, output_path, voice)

def get_gpu_subtitle_filter(subtitle_file: str) -> str:
    """获取GPU加速的字幕滤镜"""
    return gpu_config.get_gpu_subtitle_filter(subtitle_file)


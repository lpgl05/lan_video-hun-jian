import os
import random
import requests
from uuid import uuid4
from models.oss_client import OSSClient

# 视频相关
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import TextClip, ColorClip
from moviepy.editor import CompositeVideoClip, concatenate_videoclips, ImageClip

# 音频相关
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import AudioClip, CompositeAudioClip, concatenate_audioclips

# 新增：使用 PIL 生成文字贴图，避免 ImageMagick 依赖
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# 语音合成
import edge_tts

DOWNLOAD_VIDEO_PATH = "outputs/download_videos"
DOWNLOAD_AUDIO_PATH = "outputs/download_audios"
OUTPUT_DIR = "outputs/clips"
tts_temp_dir = "outputs/tts_audio"
OSS_UPLOAD_FINAL_VEDIO = "uploads/final/videos"
os.makedirs(DOWNLOAD_VIDEO_PATH, exist_ok=True)
os.makedirs(DOWNLOAD_AUDIO_PATH, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(tts_temp_dir, exist_ok=True)
oss_client = OSSClient()

async def download_video(url):
    filename = url.split("/")[-1]
    print('---------------------------------------')
    print(url)
    print(filename)

    local_file = DOWNLOAD_VIDEO_PATH + "/" + filename
    print(local_file)
    await oss_client.download_video(url, local_file)
    return local_file

async def download_audio(url):
    filename = url.split("/")[-1]

    local_file = DOWNLOAD_AUDIO_PATH + "/" + filename
    print(local_file)
    await oss_client.download_video(url, local_file)
    return local_file

def random_cut(video_path, min_duration, max_duration, count):
    video = VideoFileClip(video_path)
    clips = []
    for _ in range(count):
        max_clip_duration = min(max_duration, int(video.duration) - 1)
        if max_clip_duration < min_duration:
            continue
        duration = random.randint(min_duration, max_clip_duration)
        start = random.uniform(0, video.duration - duration)
        clip = video.subclip(start, start + duration)
        clips.append(clip)
    return clips

def add_text(clip, text, style):
    # 使用 PIL 渲染文本，避免 TextClip 依赖 ImageMagick
    title_style = style.get("title", {}) if isinstance(style, dict) else {}
    fontsize = int(title_style.get("fontSize", 40))
    color = title_style.get("color", "#FFFFFF")
    position = title_style.get("position", "bottom")  # top | center | bottom

    banner_h = max(60, int(fontsize * 2))  # 简单设定高度
    img = Image.new("RGBA", (int(clip.w), banner_h), (0, 0, 0, 160))  # 半透明黑底
    draw = ImageDraw.Draw(img)

    # 优先使用支持中文的字体
    font = None
    chinese_fonts = [
        "C:\\Windows\\Fonts\\msyh.ttc",      # 微软雅黑
        "C:\\Windows\\Fonts\\simsun.ttc",   # 宋体
        "C:\\Windows\\Fonts\\simhei.ttf",   # 黑体
        "C:\\Windows\\Fonts\\simkai.ttf",   # 楷体
        "/System/Library/Fonts/PingFang.ttc",  # macOS
        "/System/Library/Fonts/Hiragino Sans GB.ttc",  # macOS
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",  # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # Linux备选
    ]
    
    for fp in chinese_fonts:
        try:
            font = ImageFont.truetype(fp, fontsize)
            break
        except Exception:
            continue
    
    if font is None:
        try:
            # 尝试使用系统默认字体，指定字体大小
            font = ImageFont.load_default()
        except Exception:
            # 如果都失败，创建一个简单的默认字体
            font = ImageFont.load_default()

    # 文本换行以适配宽度
    max_width = clip.w - 40
    if not text:
        text = ""
    
    # 改进文本换行逻辑，按词或字符分割
    lines = []
    words = text.split() if ' ' in text else list(text)  # 英文按词分割，中文按字符分割
    current = ""
    
    for word in words:
        test = current + (" " if current and ' ' in text else "") + word
        try:
            bbox = draw.textbbox((0, 0), test, font=font)
            text_width = bbox[2] - bbox[0]
        except Exception:
            text_width = len(test) * fontsize // 2  # 备选计算方法
            
        if text_width > max_width and current:
            lines.append(current)
            current = word
        else:
            current = test
    
    if current:
        lines.append(current)
    if not lines:
        lines = [""]  # 防止空文本异常

    # 居中绘制文本
    total_height = len(lines) * (fontsize + 4)
    y = max(0, (banner_h - total_height) // 2)
    
    for line in lines:
        try:
            bbox = draw.textbbox((0, 0), line, font=font)
            tw = bbox[2] - bbox[0]
        except Exception:
            tw = len(line) * fontsize // 2  # 备选计算方法
            
        x = max(0, (clip.w - tw) // 2)
        
        try:
            draw.text((x, y), line, font=font, fill=color)
        except Exception:
            # 如果绘制失败，尝试使用默认字体
            draw.text((x, y), line, fill=color)
            
        y += fontsize + 4

    # 生成 ImageClip 覆盖在视频上
    banner_clip = ImageClip(np.array(img)).set_duration(clip.duration)
    if position == "top":
        banner_clip = banner_clip.set_position(("center", "top"))
    elif position == "center":
        banner_clip = banner_clip.set_position(("center", "center"))
    else:
        banner_clip = banner_clip.set_position(("center", "bottom"))

    return CompositeVideoClip([clip, banner_clip])

def add_bgm(clip, bgm_path):
    bgm = AudioFileClip(bgm_path).volumex(0.2)
    if bgm.duration < clip.duration:
        bgm = bgm.audio_loop(duration=clip.duration)
    else:
        bgm = bgm.subclip(0, clip.duration)
    final_audio = bgm.set_duration(clip.duration)
    return clip.set_audio(final_audio)

def build_montage_clips(source_paths, target_duration, count):
    """
    为每个目标输出构建一个由多个源视频片段拼接而成的短视频，
    尽量保证每个输出都包含所有源视频的一部分。
    """
    if not source_paths:
        return []

    # 预加载源视频，避免重复打开
    sources = [VideoFileClip(p) for p in source_paths]
    outputs = []

    for _ in range(count):
        remaining = target_duration
        segments = []
        n = len(sources)
        # 基础分配：尽量均分给每个源视频
        base_share = max(1, target_duration // max(1, n))

        for idx, src in enumerate(sources):
            if remaining <= 0:
                break
            # 当前源视频可用最大片段时长（留 0.5s 余量避免溢出）
            src_max = max(0, int(src.duration) - 1)
            if src_max <= 0:
                continue

            # 最后一个源视频用剩余时长补齐
            alloc = base_share if idx < n - 1 else remaining
            seg_dur = min(max(1, int(alloc)), src_max)
            if seg_dur <= 0:
                continue

            start_max = max(0, src.duration - seg_dur - 0.1)
            start = random.uniform(0, start_max) if start_max > 0 else 0
            seg = src.subclip(start, start + seg_dur)
            segments.append(seg)
            remaining -= seg_dur

        # 如果还没凑够目标时长，循环从可用源视频再补片段
        safe_guard = 0
        while remaining > 0 and safe_guard < 10 * n:
            safe_guard += 1
            src = random.choice(sources)
            src_max = max(0, int(src.duration) - 1)
            if src_max <= 0:
                continue
            seg_dur = min(max(1, int(remaining)), src_max)
            if seg_dur <= 0:
                continue
            start_max = max(0, src.duration - seg_dur - 0.1)
            start = random.uniform(0, start_max) if start_max > 0 else 0
            seg = src.subclip(start, start + seg_dur)
            segments.append(seg)
            remaining -= seg_dur

        if not segments:
            continue

        # 拼接所有片段
        final = concatenate_videoclips(segments, method="compose")
        # 超出目标时长则裁剪
        if final.duration > target_duration:
            final = final.subclip(0, target_duration)
        outputs.append(final)

    # 注意：sources 由调用方统一在写文件后关闭
    return outputs

async def process_clips(req):
    video_count = req.videoCount
    duration_sec = parse_duration(req.duration)
    min_duration = duration_sec
    max_duration = duration_sec
    video_files = req.videos
    audio_files = req.audios
    scripts = [s for s in req.scripts if s.selected]
    style = req.style.dict() if hasattr(req.style, "dict") else req.style

    # 下载所有视频和音频到本地
    local_video_paths = [await download_video(v.url) for v in video_files]
    local_audio_paths = [await download_audio(a.url) for a in audio_files]

    print("=======================================")
    print(local_video_paths)
    print(local_audio_paths)
    print("=======================================")

    # 构建每个成品短视频（尽量包含每个源视频的片段）
    try:
        composed_clips = build_montage_clips(local_video_paths, duration_sec, video_count)
        if not composed_clips:
            return {"success": False, "error": "无可用视频片段"}

        result_videos = []
        for i, clip in enumerate(composed_clips):
            clip_id = str(uuid4())
            clip_name = f"clip_{clip_id}.mp4"
            clip_path = os.path.join(OUTPUT_DIR, clip_name)

            # 随机字幕
            script = random.choice(scripts).content if scripts else ""
            clip = add_text(clip, script, style)

            # 生成TTS语音文件
            tts_filename = f"tts_{clip_id}.wav"
            tts_path = os.path.join(tts_temp_dir, tts_filename)
            await generate_tts_audio(script, tts_path)

            # 随机BGM
            bgm_path = random.choice(local_audio_paths) if local_audio_paths else None
            if bgm_path and os.path.exists(bgm_path):
                clip = add_bgm_with_tts(clip, bgm_path, tts_path)
            elif bgm_path:
                # 如果TTS失败，至少添加BGM
                clip = add_bgm(clip, bgm_path)
                
            # 导出视频
            clip.write_videofile(clip_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)
            
            # 将导出的视频上传到oss上
            try:
                # 读取本地视频文件
                with open(clip_path, 'rb') as f:
                    video_content = f.read()
                
                # 上传到OSS
                oss_url = await oss_client.upload_to_oss(
                    file_buffer=video_content,
                    original_filename=clip_name,
                    folder=OSS_UPLOAD_FINAL_VEDIO
                )
                
                # 删除本地临时文件
                os.remove(clip_path)
                
                video_url = oss_url
                video_size = len(video_content)
                print(f"视频已上传到OSS: {oss_url}")
                
            except Exception as e:
                print(f"OSS上传失败: {str(e)}")
                # 如果OSS上传失败，使用本地路径
                video_url = f"/outputs/clips/{clip_name}"
                video_size = os.path.getsize(clip_path) if os.path.exists(clip_path) else 0

            result_videos.append({
                "id": clip_id,
                "name": clip_name,
                "url": video_url,
                "size": video_size,
                "duration": duration_sec,
                "uploadedAt": None
            })
        return {
            "success": True,
            "message": "视频剪辑处理完成",
            "videos": result_videos
        }
    finally:
        # 可在此处按需关闭、释放资源（如有必要）
        pass

async def generate_tts_audio(text: str, output_path: str, voice: str = "zh-CN-XiaoxiaoNeural"):
    """
    使用 edge_tts 生成语音文件
    
    Args:
        text: 要转换的文本
        output_path: 输出音频文件路径
        voice: 语音类型，默认使用中文女声
    """
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        print(f"TTS音频生成完成: {output_path}")
    except Exception as e:
        print(f"TTS生成失败: {e}")
        raise Exception("语音合成失败")
    
def add_bgm_with_tts(clip, bgm_path, tts_audio_path):
    """
    添加BGM和TTS语音，两者混合播放
    
    Args:
        clip: 视频片段
        bgm_path: 背景音乐路径
        tts_audio_path: TTS语音文件路径
    """
    try:
        # 加载TTS语音
        tts_audio = AudioFileClip(tts_audio_path)
        
        # 加载BGM并降低音量
        bgm = AudioFileClip(bgm_path).volumex(0.15)  # 降低BGM音量以突出语音
        
        # 调整TTS语音音量
        tts_audio = tts_audio.volumex(0.8)
        
        # 如果BGM时长小于视频时长，循环播放
        if bgm.duration < clip.duration:
            bgm = bgm.audio_loop(duration=clip.duration)
        else:
            bgm = bgm.subclip(0, clip.duration)
        
        # 如果TTS时长小于视频时长，在开头播放TTS，剩余时间只有BGM
        if tts_audio.duration < clip.duration:
            # 创建静音填充
            silence_duration = clip.duration - tts_audio.duration
            silence = AudioClip(lambda t: [0, 0], duration=silence_duration)
            tts_audio = concatenate_audioclips([tts_audio, silence])
        else:
            # 如果TTS更长，截取到视频长度
            tts_audio = tts_audio.subclip(0, clip.duration)
        
        # 混合两个音频轨道
        final_audio = CompositeAudioClip([bgm, tts_audio])
        final_audio = final_audio.set_duration(clip.duration)
        
        return clip.set_audio(final_audio)
        
    except Exception as e:
        print(f"音频混合失败: {e}")
        # 如果混合失败，至少保留原BGM
        return add_bgm(clip, bgm_path)


def parse_duration(duration_str):
    # 支持 '15s' | '30s' | '30-60s'
    if not duration_str:
        return 30
    s = duration_str.strip().lower()
    if s.endswith('s'):
        s = s[:-1]
    if '-' in s:
        try:
            a, b = s.split('-', 1)
            lo, hi = int(a), int(b)
            if lo > hi:
                lo, hi = hi, lo
            return random.randint(lo, hi)
        except Exception:
            return 30
    try:
        return int(s)
    except Exception:
        return 30
    except Exception:
        return 30

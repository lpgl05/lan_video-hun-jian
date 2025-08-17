import os
import random
import requests
from uuid import uuid4
from models.oss_client import OSSClient
import subprocess

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
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

DOWNLOAD_VIDEO_PATH = "outputs/download_videos"
DOWNLOAD_AUDIO_PATH = "outputs/download_audios"
OUTPUT_DIR = "outputs/clips"
tts_temp_dir = "outputs/tts_audio"
TTS_TEMP_DIR = "outputs/tts_audio"
SUBTITLE_TEMP_DIR = "outputs/subtitle_images"
OSS_UPLOAD_FINAL_VEDIO = "uploads/final/videos"
os.makedirs(DOWNLOAD_VIDEO_PATH, exist_ok=True)
os.makedirs(DOWNLOAD_AUDIO_PATH, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(tts_temp_dir, exist_ok=True)
os.makedirs(SUBTITLE_TEMP_DIR, exist_ok=True)
oss_client = OSSClient()

# 先从.env中读取字体要求
VIDEO_FONT = os.getenv("VIDEO_FONT", "msyh.ttc")
FONT_PATH = os.path.join("fonts", VIDEO_FONT)
print(f'指定的字体路径是: {FONT_PATH}')

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

def add_text(clip, text, style, font_path=None):
    # 使用 PIL 渲染文本，避免 TextClip 依赖 ImageMagick
    title_style = style.get("title", {}) if isinstance(style, dict) else {}
    fontsize = int(title_style.get("fontSize", 40))
    color = title_style.get("color", "#FFFFFF")
    position = title_style.get("position", "bottom")  # top | center | bottom

    banner_h = max(60, int(fontsize * 2))  # 简单设定高度
    img = Image.new("RGBA", (int(clip.w), banner_h), (0, 0, 0, 160))  # 半透明黑底
    draw = ImageDraw.Draw(img)

    # 优先使用用户指定的字体
    font = None
    if font_path and os.path.exists(font_path):
        try:
            print('本地文件已经存在........')
            font = ImageFont.truetype(font_path, fontsize)
        except Exception:
            font = None
    else:
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
            clip = add_text(clip, script, style, font_path=FONT_PATH)

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

def create_title_image(text, width=1080, height=1920, style=None):
    """生成标题字幕图片 - 单独的Title层"""
    if not text:
        # 创建1x1透明图片
        img = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
        return img
    
    title_style = style.get("title", {}) if style else {}
    fontsize = int(title_style.get("fontSize", 64))  # Title字体更大
    color = title_style.get("color", "#FFD700")  # Title默认金色
    
    # 计算实际需要的横幅尺寸
    target_width = 1080  # 视频宽度
    
    # 先创建临时画布来计算实际需要的高度
    temp_img = Image.new("RGBA", (target_width, 500), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    
    # 字体处理
    font = None

    chinese_fonts = [
        "C:\\Windows\\Fonts\\msyh.ttc",
        "C:\\Windows\\Fonts\\simsun.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/winfonts/msyh.ttc"
    ]
    
    for fp in chinese_fonts:
        try:
            font = ImageFont.truetype(fp, fontsize)
            break
        except:
            continue
    
    if font is None:
        font = ImageFont.load_default()

    # 文本换行 - Title通常较短，限制更严格
    max_width = target_width - 120  # 左右各留60像素边距
    lines = []
    current_line = ""
    
    for char in text:
        test_line = current_line + char
        try:
            bbox = temp_draw.textbbox((0, 0), test_line, font=font)
            text_width = bbox[2] - bbox[0]
        except:
            text_width = len(test_line) * fontsize // 2
            
        if text_width > max_width and current_line:
            lines.append(current_line)
            current_line = char
        else:
            current_line = test_line
    
    if current_line:
        lines.append(current_line)
    
    # 限制行数 - Title最多2行
    lines = lines[:2]
    
    # 计算实际需要的高度
    line_height = fontsize + 20  # Title行间距更大
    text_total_height = len(lines) * line_height
    padding_vertical = 60  # 上下各30像素内边距
    banner_h = text_total_height + padding_vertical
    
    # 确保最小高度
    banner_h = max(140, banner_h)  # Title最小140像素高度
    
    print(f"Title计算: 字体={fontsize}, 行数={len(lines)}, 横幅高度={banner_h}")

    # 创建实际的Title横幅 - 使用渐变背景或更显眼的背景
    img = Image.new("RGBA", (target_width, banner_h), (0, 0, 0, 220))  # 更不透明的背景
    draw = ImageDraw.Draw(img)

    # 绘制文本，垂直居中
    start_y = (banner_h - text_total_height) // 2
    
    for line in lines:
        try:
            bbox = draw.textbbox((0, 0), line, font=font)
            tw = bbox[2] - bbox[0]
        except:
            tw = len(line) * fontsize // 2
            
        x = (target_width - tw) // 2  # 水平居中
        try:
            # 添加文字阴影效果
            draw.text((x+2, start_y+2), line, font=font, fill=(0, 0, 0, 128))  # 阴影
            draw.text((x, start_y), line, font=font, fill=color)  # 主文字
        except:
            draw.text((x, start_y), line, fill=color)
        start_y += line_height

    return img

def create_9_16_video_with_title_ffmpeg(source_video, title_image, subtitle_image, tts_audio, bgm_audio, output_path, duration, title_position="top", subtitle_position="bottom"):
    """使用FFmpeg创建9:16视频，包含模糊背景、Title、Subtitle和音频混合"""
    ffmpeg = find_ffmpeg()
    
    target_width = 1080
    target_height = 1920
    
    # 计算Title位置
    title_margin = 200
    if title_position == "top":
        title_overlay_y = title_margin
        title_desc = "顶部"
    elif title_position == "center":
        title_overlay_y = f"(H-h)/2-100"  # 稍微偏上一些
        title_desc = "中部"
    else:  # bottom
        title_overlay_y = f"H-h-{title_margin}"
        title_desc = "底部"
    
    # 计算Subtitle位置
    subtitle_margin = 250
    if subtitle_position == "top":
        subtitle_overlay_y = subtitle_margin
        subtitle_desc = "顶部"
    elif subtitle_position == "center":
        subtitle_overlay_y = f"(H-h)/2+100"  # 稍微偏下一些
        subtitle_desc = "中部"
    else:  # bottom
        subtitle_overlay_y = f"H-h-{subtitle_margin}"
        subtitle_desc = "底部"
    
    print(f"Title位置设置: {title_desc} (overlay_y={title_overlay_y})")
    print(f"Subtitle位置设置: {subtitle_desc} (overlay_y={subtitle_overlay_y})")
    
    filter_complex = f"""
    [0:v]scale={target_width}:{target_height}:force_original_aspect_ratio=increase,crop={target_width}:{target_height}[bg];
    [bg]boxblur=luma_radius=50:chroma_radius=50:luma_power=3[bg_blur];
    [0:v]scale={target_width}:-1[fg_scale];
    [fg_scale]scale={target_width}:{target_width*9//16}[fg];
    [bg_blur][fg]overlay=(W-w)/2:(H-h)/2[bg_with_fg];
    [1:v]format=rgba[title];
    [2:v]format=rgba[subtitle];
    [bg_with_fg][title]overlay=0:{title_overlay_y}:format=auto[bg_with_title];
    [bg_with_title][subtitle]overlay=0:{subtitle_overlay_y}:format=auto,format=yuv420p[video_out];
    [3:a]volume=0.8[tts];
    [4:a]volume=0.15[bgm];
    [tts][bgm]amix=inputs=2:duration=first:dropout_transition=0[audio_out]
    """
    
    cmd = [
        ffmpeg, '-y',
        '-i', source_video,      # 输入0: 源视频
        '-i', title_image,       # 输入1: Title图片
        '-i', subtitle_image,    # 输入2: Subtitle图片
        '-i', tts_audio,         # 输入3: TTS音频
        '-i', bgm_audio,         # 输入4: BGM音频
        '-filter_complex', filter_complex,
        '-map', '[video_out]',   # 映射视频流
        '-map', '[audio_out]',   # 映射音频流
        '-t', str(duration),     # 设置时长
        '-preset', 'medium',
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-threads', str(os.cpu_count()),
        '-movflags', '+faststart',
        output_path
    ]
    
    try:
        print("开始FFmpeg处理...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"FFmpeg错误: {result.stderr}")
            return False
        print("FFmpeg处理完成")
        return True
    except Exception as e:
        print(f"FFmpeg执行失败: {e}")
        return False

async def process_clips001(req):
    """
    【FFmpeg版本】视频处理方法 - 高性能蒙太奇拼接版本
    使用FFmpeg命令行进行视频处理，支持多源视频蒙太奇拼接
    """
    import time

    video_count = req.videoCount
    duration_sec = parse_duration(req.duration)
    video_files = req.videos
    audio_files = req.audios
    scripts = [s for s in req.scripts if s.selected]
    style = req.style.dict() if hasattr(req.style, "dict") else req.style

    # 项目的标题和样式
    title = req.name
    title_fontsize = style.get("title", {}).get("fontSize", 64)
    title_color = style.get("title", {}).get("color", "#FFD700")
    title_position = style.get("title", {}).get("position", "top")
    
    # 字幕样式
    subtitle_position = style.get("subtitle", {}).get("position", "bottom")

    # 下载所有视频和音频到本地
    local_video_paths = [await download_video(v.url) for v in video_files]
    local_audio_paths = [await download_audio(a.url) for a in audio_files]

    print("=======================================")
    print("包含：Title + Subtitle + TTS语音 + 背景音乐")
    print(f"项目标题: {title}")
    print(f"Title位置: {title_position}")
    print(f"Subtitle位置: {subtitle_position}")
    print(f"视频源: {len(local_video_paths)}个")
    print(f"音频源: {len(local_audio_paths)}个")
    print("=======================================")

    if not local_video_paths:
        return {"success": False, "error": "找不到视频文件"}

    total_start_time = time.time()
    result_videos = []

    try:
        # 检查FFmpeg
        ffmpeg = find_ffmpeg()
        print(f"使用FFmpeg: {ffmpeg}")
        
        # 获取所有源视频信息
        video_infos = []
        for video_path in local_video_paths:
            if os.path.exists(video_path):
                info = get_video_info(video_path)
                video_infos.append(info)
                print(f"源视频: {video_path} -> {info['width']}x{info['height']}, {info['duration']:.1f}秒")

        if not video_infos:
            return {"success": False, "error": "无有效视频文件"}

        for i in range(video_count):
            clip_id = str(uuid4())[:8]
            
            # 1. 蒙太奇拼接 - 提取多个片段
            montage_start = time.time()
            temp_clips = []
            
            # 智能分配每个视频的时长
            n_videos = len(local_video_paths)
            base_duration = duration_sec // n_videos
            remaining_duration = duration_sec % n_videos
            
            print(f"蒙太奇分配: 每个视频基础{base_duration}秒，剩余{remaining_duration}秒")
            
            for idx, (video_path, video_info) in enumerate(zip(local_video_paths, video_infos)):
                segment_duration = base_duration
                if idx < remaining_duration:
                    segment_duration += 1
                
                if segment_duration <= 0:
                    continue
                    
                max_segment = min(segment_duration, int(video_info['duration']) - 1)
                if max_segment <= 0:
                    continue
                
                max_start = max(0, video_info['duration'] - max_segment - 0.5)
                start_time = random.uniform(0, max_start) if max_start > 0 else 0
                
                temp_clip_path = os.path.join(OUTPUT_DIR, f"temp_segment_{clip_id}_{idx}.mp4")
                
                if extract_random_clip_ffmpeg(video_path, temp_clip_path, start_time, max_segment):
                    temp_clips.append(temp_clip_path)
                    print(f"片段{idx+1}: {video_path} -> {max_segment}秒 (从{start_time:.1f}秒开始)")
                else:
                    print(f"片段{idx+1}提取失败")
            
            if not temp_clips:
                print("没有成功提取的片段，跳过")
                continue
            
            # 2. 使用FFmpeg拼接片段
            montage_clip_path = os.path.join(OUTPUT_DIR, f"montage_clip_{clip_id}.mp4")
            
            if len(temp_clips) == 1:
                import shutil
                shutil.copy2(temp_clips[0], montage_clip_path)
            else:
                if not concat_videos_ffmpeg(temp_clips, montage_clip_path):
                    print("视频拼接失败")
                    continue
            
            montage_time = time.time() - montage_start

            # 3. 生成Title图片
            title_start = time.time()
            title_image_path = os.path.join(SUBTITLE_TEMP_DIR, f"title_{clip_id}.png")
            title_img = create_title_image(title, 1080, 1920, style)
            title_img.save(title_image_path)
            title_time = time.time() - title_start
            print(f"Title生成: {title_time:.1f}秒")

            # 4. 生成Subtitle图片
            subtitle_start = time.time()
            script = random.choice(scripts).content if scripts else random.choice([
                '这是一段精彩的视频内容，展现了多个精彩瞬间的完美融合',
                '蒙太奇拼接技术让视频更加生动有趣',
                '多个视频源的巧妙组合创造出全新的视觉体验'
            ])
            
            subtitle_image_path = os.path.join(SUBTITLE_TEMP_DIR, f"subtitle_{clip_id}.png")
            subtitle_img = create_subtitle_image(script, 1080, 1920, style)
            subtitle_img.save(subtitle_image_path)
            subtitle_time = time.time() - subtitle_start
            print(f"Subtitle生成: {subtitle_time:.1f}秒")

            # 5. 生成TTS音频
            tts_start = time.time()
            tts_path = os.path.join(TTS_TEMP_DIR, f"tts_{clip_id}.wav")

            voice = 'zh-CN-YunxiNeural' if req.voice == 'male' else 'zh-CN-XiaoxiaoNeural'
            await generate_tts_audio(script, tts_path, voice)
            tts_time = time.time() - tts_start
            print(f"TTS生成: {tts_time:.1f}秒")

            # 6. FFmpeg最终合成（包含Title和Subtitle）
            compose_start = time.time()
            final_output = os.path.join(OUTPUT_DIR, f"ffmpeg_montage_{clip_id}.mp4")
            
            # BGM处理
            bgm_audio = random.choice(local_audio_paths) if local_audio_paths else None
            if not bgm_audio or not os.path.exists(bgm_audio):
                silence_path = os.path.join(TTS_TEMP_DIR, f"silence_{clip_id}.wav")
                create_silence_audio(duration_sec, silence_path)
                bgm_audio = silence_path
            
            success = create_9_16_video_with_title_ffmpeg(
                montage_clip_path,
                title_image_path,
                subtitle_image_path,
                tts_path,
                bgm_audio,
                final_output,
                duration_sec,
                title_position,
                subtitle_position
            )
            
            compose_time = time.time() - compose_start
            print(f"视频合成: {compose_time:.1f}秒")
            
            if success:
                # 上传到OSS
                try:
                    clip_name = f"ffmpeg_montage_{clip_id}.mp4"
                    with open(final_output, 'rb') as f:
                        video_content = f.read()
                    
                    oss_url = await oss_client.upload_to_oss(
                        file_buffer=video_content,
                        original_filename=clip_name,
                        folder=OSS_UPLOAD_FINAL_VEDIO
                    )
                    
                    video_url = oss_url
                    video_size = len(video_content)
                    print(f"视频已上传到OSS: {oss_url}")
                    
                    os.remove(final_output)
                    
                except Exception as e:
                    print(f"OSS上传失败: {str(e)}")
                    video_url = f"/outputs/clips/ffmpeg_montage_{clip_id}.mp4"
                    video_size = os.path.getsize(final_output) if os.path.exists(final_output) else 0

                # 清理临时文件
                for temp_file in temp_clips + [montage_clip_path, title_image_path, subtitle_image_path, tts_path]:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                
                result_videos.append({
                    "id": clip_id,
                    "name": f"ffmpeg_montage_{clip_id}.mp4",
                    "url": video_url,
                    "size": video_size,
                    "duration": duration_sec,
                    "uploadedAt": None
                })
                
                total_time = time.time() - total_start_time
                print(f'视频{i+1}完成，总耗时: {total_time:.1f}秒')
                print(f"📊 各阶段耗时占比:")
                print(f"   - Title生成: {(title_time/total_time)*100:.1f}%")
                print(f"   - Subtitle生成: {(subtitle_time/total_time)*100:.1f}%")
                print(f"   - TTS生成: {(tts_time/total_time)*100:.1f}%")
                print(f"   - 视频合成: {(compose_time/total_time)*100:.1f}%")
            else:
                print("❌ 视频合成失败")
                
        return {
            "success": True,
            "message": "FFmpeg蒙太奇视频处理完成",
            "videos": result_videos
        }
                
    except Exception as e:
        print(f"处理出错: {e}")
        return {"success": False, "error": str(e)}

def concat_videos_ffmpeg(video_paths, output_path):
    """
    使用FFmpeg拼接多个视频片段
    
    Args:
        video_paths: 视频文件路径列表
        output_path: 输出文件路径
    """
    if not video_paths:
        return False
        
    ffmpeg = find_ffmpeg()
    
    try:
        # 创建临时文件列表
        concat_file = os.path.join(OUTPUT_DIR, f"concat_list_{str(uuid4())[:8]}.txt")
        # concat_file = os.path.join(OUTPUT_DIR, f"concat_list_{uuid4()[:8]}.txt")
        
        with open(concat_file, 'w', encoding='utf-8') as f:
            for video_path in video_paths:
                # 使用相对路径或绝对路径
                abs_path = os.path.abspath(video_path)
                f.write(f"file '{abs_path}'\n")
        
        # FFmpeg拼接命令
        cmd = [
            ffmpeg, '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_file,
            '-c', 'copy',  # 复制流，最快
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # 清理临时文件
        if os.path.exists(concat_file):
            os.remove(concat_file)
            
        if result.returncode != 0:
            print(f"FFmpeg拼接错误: {result.stderr}")
            return False
            
        print(f"成功拼接{len(video_paths)}个片段")
        return True
        
    except Exception as e:
        print(f"视频拼接失败: {e}")
        return False

def find_ffmpeg():
    """查找FFmpeg可执行文件"""
    possible_paths = [
        'ffmpeg',  # 系统PATH中
        'ffmpeg.exe',
        r'C:\ffmpeg\bin\ffmpeg.exe',
        r'C:\Program Files\ffmpeg\bin\ffmpeg.exe',
        '/usr/bin/ffmpeg',
        '/usr/local/bin/ffmpeg'
    ]
    
    for path in possible_paths:
        try:
            subprocess.run([path, '-version'], capture_output=True, check=True)
            return path
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    raise Exception("未找到FFmpeg，请安装FFmpeg并添加到系统PATH")

def get_video_info(video_path):
    """获取视频信息"""
    ffmpeg = find_ffmpeg()
    cmd = [
        ffmpeg, '-i', video_path,
        '-f', 'null', '-'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        # 从stderr中解析视频信息
        output = result.stderr
        
        # 提取分辨率
        import re
        resolution_match = re.search(r'(\d+)x(\d+)', output)
        if resolution_match:
            width, height = map(int, resolution_match.groups())
        else:
            width, height = 1920, 1080  # 默认值
        
        # 提取时长
        duration_match = re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)', output)
        if duration_match:
            h, m, s = duration_match.groups()
            duration = int(h) * 3600 + int(m) * 60 + float(s)
        else:
            duration = 30.0  # 默认值
        
        return {
            'width': width,
            'height': height,
            'duration': duration
        }
    except Exception as e:
        print(f"获取视频信息失败: {e}")
        return {'width': 1920, 'height': 1080, 'duration': 30.0}

def create_subtitle_image(text, width=480, height=854, style=None):
    """生成字幕图片 - 只生成字幕横幅大小的图片"""
    if not text:
        # 创建1x1透明图片
        img = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
        return img
    
    subtitle_style = style.get("subtitle", {}) if style else {}
    fontsize = int(subtitle_style.get("fontSize", 48))
    color = subtitle_style.get("color", "#FFFFFF")
    
    # 计算实际需要的横幅尺寸
    target_width = 1080  # 视频宽度
    
    # 先创建临时画布来计算实际需要的高度
    temp_img = Image.new("RGBA", (target_width, 500), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    
    # 优先使用用户指定的字体
    font = None
    if FONT_PATH and os.path.exists(FONT_PATH):
        try:
            print('本地文件已经存在........')
            font = ImageFont.truetype(FONT_PATH, fontsize)
        except Exception:
            font = None
    else:
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

    # 文本换行
    max_width = target_width - 80  # 左右各留40像素边距
    lines = []
    current_line = ""
    
    for char in text:
        test_line = current_line + char
        try:
            bbox = temp_draw.textbbox((0, 0), test_line, font=font)
            text_width = bbox[2] - bbox[0]
        except:
            text_width = len(test_line) * fontsize // 2
            
        if text_width > max_width and current_line:
            lines.append(current_line)
            current_line = char
        else:
            current_line = test_line
    
    if current_line:
        lines.append(current_line)
    
    # 限制行数
    lines = lines[:3]
    
    # 计算实际需要的高度
    line_height = fontsize + 16  # 每行高度增加间距
    text_total_height = len(lines) * line_height
    padding_vertical = 40  # 上下各20像素内边距
    banner_h = text_total_height + padding_vertical
    
    # 确保最小高度
    banner_h = max(120, banner_h)  # 最小120像素高度
    
    print(f"字幕计算: 字体={fontsize}, 行数={len(lines)}, 横幅高度={banner_h}")

    # 创建实际的字幕横幅
    img = Image.new("RGBA", (target_width, banner_h), (0, 0, 0, 200))  # 增加背景不透明度
    draw = ImageDraw.Draw(img)

    # 绘制文本，垂直居中
    start_y = (banner_h - text_total_height) // 2
    
    for line in lines:
        try:
            bbox = draw.textbbox((0, 0), line, font=font)
            tw = bbox[2] - bbox[0]
        except:
            tw = len(line) * fontsize // 2
            
        x = (target_width - tw) // 2  # 水平居中
        try:
            draw.text((x, start_y), line, font=font, fill=color)
        except:
            draw.text((x, start_y), line, fill=color)
        start_y += line_height

    return img

async def generate_tts_audio(text: str, output_path: str, voice: str = "zh-CN-XiaoxiaoNeural"):
    """使用 edge_tts 生成语音文件"""
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        print(f"TTS音频生成完成: {output_path}, {voice}")
    except Exception as e:
        print(f"TTS生成失败: {e}")
        raise Exception("语音合成失败")

def extract_random_clip_ffmpeg(source_video, output_path, start_time, duration):
    """使用FFmpeg提取随机片段"""
    ffmpeg = find_ffmpeg()
    
    cmd = [
        ffmpeg, '-y',
        '-ss', str(start_time),  # 开始时间
        '-i', source_video,      # 输入视频
        '-t', str(duration),     # 持续时间
        '-c', 'copy',           # 复制流，不重新编码（最快）
        output_path
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"提取片段失败: {e}")
        return False

def create_9_16_video_ffmpeg(source_video, subtitle_image, tts_audio, bgm_audio, output_path, duration, subtitle_position="bottom"):
    """使用FFmpeg创建9:16视频，包含模糊背景、字幕和音频混合"""
    ffmpeg = find_ffmpeg()
    
    target_width = 1080
    target_height = 1920
    
    # 根据字幕位置参数计算overlay坐标
    subtitle_margin = 250  # 字幕距离边缘的边距
    
    if subtitle_position == "top":
        # 顶部：y = margin
        overlay_y = subtitle_margin
        position_desc = "顶部"
    elif subtitle_position == "center":
        # 中部：y = (视频高度 - 字幕高度) / 2
        overlay_y = f"(H-h)/2"
        position_desc = "中部"
    else:  # bottom
        # 底部：y = 视频高度 - 字幕高度 - margin
        overlay_y = f"H-h-{subtitle_margin}"
        position_desc = "底部"
    
    print(f"字幕位置设置: {position_desc} (overlay_y={overlay_y})")
    
    filter_complex = f"""
    [0:v]scale={target_width}:{target_height}:force_original_aspect_ratio=increase,crop={target_width}:{target_height}[bg];
    [bg]boxblur=luma_radius=50:chroma_radius=50:luma_power=3[bg_blur];
    [0:v]scale={target_width}:-1[fg_scale];
    [fg_scale]scale={target_width}:{target_width*9//16}[fg];
    [bg_blur][fg]overlay=(W-w)/2:(H-h)/2[bg_with_fg];
    [1:v]format=rgba[subtitle];
    [bg_with_fg][subtitle]overlay=0:{overlay_y}:format=auto,format=yuv420p[video_out];
    [2:a]volume=0.8[tts];
    [3:a]volume=0.15[bgm];
    [tts][bgm]amix=inputs=2:duration=first:dropout_transition=0[audio_out]
    """
    # 关键修改：
    # 1. overlay=0:H-h-{subtitle_bottom_margin} 将字幕精确放置在底部上方60像素处
    # 2. H-h 表示视频高度减去字幕图片高度，再减去边距
    # 3. 移除了不必要的透明度处理，保持字幕清晰

    cmd = [
        ffmpeg, '-y',
        '-i', source_video,      # 输入0: 源视频
        '-i', subtitle_image,    # 输入1: 字幕图片
        '-i', tts_audio,         # 输入2: TTS音频
        '-i', bgm_audio,         # 输入3: BGM音频
        '-filter_complex', filter_complex,  # 修复：使用正确的完整滤镜链
        '-map', '[video_out]',   # 映射视频流
        '-map', '[audio_out]',   # 映射音频流
        '-t', str(duration),     # 设置时长
        # 修改：提高视频质量参数
        '-preset', 'medium',      # 从ultrafast改为medium，提高质量
        '-c:v', 'libx264',
        '-crf', '23',            # 从28改为23，提高画质（数值越小质量越高）
        '-c:a', 'aac',
        '-b:a', '192k',          # 提高音频比特率从128k到192k
        '-threads', str(os.cpu_count()),
        '-movflags', '+faststart',
        output_path
    ]
    
    try:
        print("开始FFmpeg处理...")
        print(f"执行命令: {' '.join(cmd)}")  # 添加调试信息
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"FFmpeg错误: {result.stderr}")
            return False
        print("FFmpeg处理完成")
        return True
    except Exception as e:
        print(f"FFmpeg执行失败: {e}")
        return False

def create_silence_audio(duration, output_path):
    """创建静音音频文件"""
    ffmpeg = find_ffmpeg()
    
    cmd = [
        ffmpeg, '-y',
        '-f', 'lavfi',
        '-i', f'anullsrc=channel_layout=stereo:sample_rate=44100',
        '-t', str(duration),
        '-c:a', 'aac',
        output_path
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except:
        return False
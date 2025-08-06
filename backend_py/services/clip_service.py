import os
import random
import requests
from uuid import uuid4
from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip

OUTPUT_DIR = "outputs/clips"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_video(url):
    filename = url.split("/")[-1]
    local_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(local_path):
        return local_path
    r = requests.get(url, stream=True)
    with open(local_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            f.write(chunk)
    return local_path

def download_audio(url):
    filename = url.split("/")[-1]
    local_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(local_path):
        return local_path
    r = requests.get(url, stream=True)
    with open(local_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            f.write(chunk)
    return local_path

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
    fontsize = style.get("title", {}).get("fontSize", 40)
    color = style.get("title", {}).get("color", "white")
    txt = TextClip(text, fontsize=fontsize, color=color, bg_color='black', size=(clip.w, 100))
    txt = txt.set_duration(clip.duration).set_position(("center", "bottom"))
    return CompositeVideoClip([clip, txt])

def add_bgm(clip, bgm_path):
    bgm = AudioFileClip(bgm_path).volumex(0.2)
    if bgm.duration < clip.duration:
        bgm = bgm.audio_loop(duration=clip.duration)
    else:
        bgm = bgm.subclip(0, clip.duration)
    final_audio = bgm.set_duration(clip.duration)
    return clip.set_audio(final_audio)

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
    local_video_paths = [download_video(v.url) for v in video_files]
    local_audio_paths = [download_audio(a.url) for a in audio_files]

    # 合并所有视频为一个整体（简单拼接，实际可优化）
    all_clips = []
    for path in local_video_paths:
        clips = random_cut(path, min_duration, max_duration, video_count)
        all_clips.extend(clips)
    if not all_clips:
        return {"success": False, "error": "无可用视频片段"}

    # 随机选取 videoCount 个片段
    selected_clips = random.sample(all_clips, min(video_count, len(all_clips)))

    result_videos = []
    for i, clip in enumerate(selected_clips):
        clip_id = str(uuid4())
        clip_name = f"clip_{clip_id}.mp4"
        clip_path = os.path.join(OUTPUT_DIR, clip_name)

        # 随机字幕
        script = random.choice(scripts).content if scripts else ""
        clip = add_text(clip, script, style)

        # 随机BGM
        bgm_path = random.choice(local_audio_paths) if local_audio_paths else None
        if bgm_path:
            clip = add_bgm(clip, bgm_path)

        # 导出视频
        clip.write_videofile(clip_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)

        result_videos.append({
            "id": clip_id,
            "name": clip_name,
            "url": f"/outputs/clips/{clip_name}",
            "size": os.path.getsize(clip_path) if os.path.exists(clip_path) else 0,
            "duration": duration_sec,
            "uploadedAt": None
        })

    return {
        "success": True,
        "message": "视频剪辑处理完成",
        "videos": result_videos
    }

def parse_duration(duration_str):
    # 简单解析 '30s' -> 30
    if duration_str.endswith('s'):
        return int(duration_str[:-1])
    return 30

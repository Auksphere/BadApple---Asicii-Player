#!/usr/bin/env python3
"""
Bad Apple视频预处理器
将视频转换为JSON格式的ASCII帧数据，供HTML页面使用
"""

import cv2
import numpy as np
import json
import sys
import os

ASCII_CHARS = list(" .'`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$")

def frame_to_ascii_fast(frame, width, height, contrast=1.7, brightness=-30):
    """将视频帧转换为ASCII字符画"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = np.clip(contrast * gray + brightness, 0, 255).astype(np.uint8)
    resized = cv2.resize(gray, (width, height), interpolation=cv2.INTER_LINEAR)
    
    char_count = len(ASCII_CHARS)
    indices = (resized.astype(np.float32) * (char_count - 1) / 255.0).astype(np.int32)
    indices = np.clip(indices, 0, char_count - 1)
    
    ascii_chars_array = np.array(list(ASCII_CHARS))
    char_matrix = ascii_chars_array[indices]
    
    ascii_str = '\n'.join([''.join(row) for row in char_matrix])
    return ascii_str

def process_video(video_path, output_path, target_fps=24, max_width=100, max_height=40):
    """处理视频并生成ASCII帧数据"""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"无法打开视频: {video_path}")
        return False
    
    # 获取视频信息
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # 计算合适的ASCII尺寸
    video_aspect = video_width / video_height
    char_aspect_correction = 0.4
    
    if video_aspect * char_aspect_correction > max_width / max_height:
        width = max_width
        height = int(width / (video_aspect * char_aspect_correction))
    else:
        height = max_height
        width = int(height * video_aspect * char_aspect_correction)
    
    width = max(min(width, max_width), 60)
    height = max(min(height, max_height), 20)
    
    print(f"视频信息: {video_width}x{video_height} @ {video_fps}fps")
    print(f"ASCII尺寸: {width}x{height} @ {target_fps}fps")
    print(f"总帧数: {total_frames}")
    
    frame_interval = max(1, int(round(video_fps / target_fps))) if video_fps > 0 else 1
    frames_data = []
    
    frame_count = 0
    processed_count = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            if frame_count % frame_interval == 0:
                ascii_frame = frame_to_ascii_fast(frame, width, height)
                frames_data.append(ascii_frame)
                processed_count += 1
                
                if processed_count % 100 == 0:
                    print(f"已处理 {processed_count} 帧...")
            
            frame_count += 1
    
    except KeyboardInterrupt:
        print("处理被中断")
    finally:
        cap.release()
    
    # 保存数据为JSON
    output_data = {
        "fps": target_fps,
        "width": width,
        "height": height,
        "total_frames": len(frames_data),
        "frames": frames_data
    }
    
    print(f"正在保存到 {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, separators=(',', ':'))
    
    print(f"处理完成! 生成了 {len(frames_data)} 帧数据")
    print(f"文件大小: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
    return True

def main():
    if len(sys.argv) < 2:
        print("用法: python3 generate_frames.py <video_file> [output_file]")
        print("示例: python3 generate_frames.py BadApple.mp4 frames.json")
        return
    
    video_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "frames.json"
    
    if not os.path.exists(video_path):
        print(f"视频文件不存在: {video_path}")
        return
    
    success = process_video(video_path, output_path)
    if success:
        print("\n下一步:")
        print("1. 将生成的 frames.json 文件放在与 index.html 同一目录")
        print("2. 在浏览器中打开 index.html 即可播放")

if __name__ == "__main__":
    main()

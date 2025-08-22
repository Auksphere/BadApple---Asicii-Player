import sys
import cv2
import numpy as np
from PIL import Image
import time
import os
import shutil

ASCII_CHARS = list(" .'`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$")


def get_terminal_size():
    size = shutil.get_terminal_size((120, 40))
    # 获取可用的终端尺寸
    terminal_width = size.columns
    terminal_height = size.lines
    return terminal_width, terminal_height

def calculate_center_margins(ascii_width, ascii_height, terminal_width, terminal_height):
    """计算居中显示所需的边距"""
    horizontal_margin = max(0, (terminal_width - ascii_width) // 2)
    vertical_margin = max(0, (terminal_height - ascii_height) // 2)
    return horizontal_margin, vertical_margin

def center_ascii_frame(ascii_frame, horizontal_margin, vertical_margin):
    """将ASCII字符画居中显示"""
    lines = ascii_frame.split('\n')
    
    # 添加水平边距（左侧空格）
    centered_lines = [' ' * horizontal_margin + line for line in lines]
    
    # 添加垂直边距（顶部空行）
    top_padding = [' ' * (len(centered_lines[0]) if centered_lines else 0)] * vertical_margin
    
    # 组合最终输出
    return '\n'.join(top_padding + centered_lines)

def calculate_aspect_ratio_size(video_width, video_height, terminal_width, terminal_height):
    # 计算视频宽高比
    video_aspect = video_width / video_height
    # 字符的宽高比约为1:2，需要调整
    char_aspect_correction = 0.6
    
    # 为居中显示留出边距
    available_width = terminal_width - 4  # 左右各留2个字符
    available_height = terminal_height - 6  # 上下各留3行
    
    # 根据终端尺寸和视频比例计算最佳尺寸
    if video_aspect * char_aspect_correction > available_width / available_height:
        # 以宽度为准
        width = min(available_width, 100)  # 最大宽度限制
        height = int(width / (video_aspect * char_aspect_correction))
    else:
        # 以高度为准
        height = min(available_height, 80)  # 最大高度限制
        width = int(height * video_aspect * char_aspect_correction)
    
    # 确保最小尺寸
    width = max(width, 60)
    height = max(height, 20)
    
    return min(width, available_width), min(height, available_height)

def frame_to_ascii_fast(frame, width, height, contrast=1.5, brightness=0):
    # 直接使用OpenCV进行所有操作，避免PIL转换开销
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 对比度和亮度调整
    gray = np.clip(contrast * gray + brightness, 0, 255).astype(np.uint8)
    # 直接使用OpenCV resize，比PIL更快
    resized = cv2.resize(gray, (width, height), interpolation=cv2.INTER_LINEAR)
    
    # 预计算字符映射，避免重复计算
    char_count = len(ASCII_CHARS)
    # 使用numpy向量化操作，大幅提升速度
    indices = (resized.astype(np.float32) * (char_count - 1) / 255.0).astype(np.int32)
    indices = np.clip(indices, 0, char_count - 1)
    
    # 向量化字符映射
    ascii_chars_array = np.array(list(ASCII_CHARS))
    char_matrix = ascii_chars_array[indices]
    
    # 快速字符串拼接
    ascii_str = '\n'.join([''.join(row) for row in char_matrix])
    return ascii_str


def play_video_ascii(video_path, target_fps=30):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Cannot open video: {video_path}")
        return
    
    # 获取视频信息
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    delay = 1 / target_fps
    terminal_width, terminal_height = get_terminal_size()
    width, height = calculate_aspect_ratio_size(video_width, video_height, terminal_width, terminal_height)
    
    # 计算居中边距
    horizontal_margin, vertical_margin = calculate_center_margins(width, height, terminal_width, terminal_height)
    
    print(f"Video: {video_width}x{video_height} @ {video_fps}fps")
    print(f"ASCII: {width}x{height} @ {target_fps}fps")
    print(f"Terminal: {terminal_width}x{terminal_height}, Margins: H={horizontal_margin}, V={vertical_margin}")
    print("Press Ctrl+C to stop...")
    time.sleep(2)
    
    frame_interval = max(1, int(round(video_fps / target_fps))) if video_fps > 0 else 1
    
    # 预计算清屏序列，避免重复系统调用
    clear_screen = '\033[2J\033[H'
    
    try:
        frame_count = 0
        start_time = time.time()
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count % frame_interval == 0:
                # 计算实际应该的时间点
                target_time = start_time + (frame_count // frame_interval) * delay
                
                ascii_frame = frame_to_ascii_fast(frame, width, height, contrast=1.7, brightness=-30)
                centered_frame = center_ascii_frame(ascii_frame, horizontal_margin, vertical_margin)
                print(clear_screen + centered_frame, end='', flush=True)
                
                # 精确时间控制，避免累积误差
                current_time = time.time()
                sleep_time = target_time - current_time
                if sleep_time > 0:
                    time.sleep(sleep_time)
            frame_count += 1
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()



def debug_show_frame(video_path, frame_num=0):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Cannot open video: {video_path}")
        return
    
    # 获取视频信息
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if frame_num >= total:
        print(f"Frame number {frame_num} exceeds total frames {total}.")
        cap.release()
        return
        
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        print(f"Failed to read frame {frame_num}.")
        return
        
    terminal_width, terminal_height = get_terminal_size()
    width, height = calculate_aspect_ratio_size(video_width, video_height, terminal_width, terminal_height)
    
    horizontal_margin, vertical_margin = calculate_center_margins(width, height, terminal_width, terminal_height)
    
    ascii_frame = frame_to_ascii_fast(frame, width, height, contrast=1.7, brightness=-30)
    centered_frame = center_ascii_frame(ascii_frame, horizontal_margin, vertical_margin)
    print(f"--- Debug: Frame {frame_num} ASCII Art ({width}x{height}) Centered ---")
    print(centered_frame)

def main():
    if len(sys.argv) < 2:
        print("Usage: python play_ascii.py <video_file> [--debug [frame_num]]")
        return
    video_path = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "--debug":
        frame_num = 0
        if len(sys.argv) > 3:
            try:
                frame_num = int(sys.argv[3])
            except ValueError:
                print("Invalid frame number, using 0.")
        debug_show_frame(video_path, frame_num)
    else:
        play_video_ascii(video_path)

if __name__ == "__main__":
    main()

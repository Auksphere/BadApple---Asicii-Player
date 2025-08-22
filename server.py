#!/usr/bin/env python3
"""
简单的HTTP服务器，用于本地测试Bad Apple HTML播放器
"""

import http.server
import socketserver
import os
import sys
import webbrowser
from pathlib import Path

def start_server(port=8000):
    """启动HTTP服务器"""
    
    # 确保必要文件存在
    if not os.path.exists('index.html'):
        print("错误: index.html 文件不存在")
        return False
    
    if not os.path.exists('frames.json'):
        print("错误: frames.json 文件不存在")
        print("请先运行: python3 generate_frames.py BadApple.mp4")
        return False
    
    # 设置处理器
    class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            # 添加CORS头，允许本地访问
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
        
        def log_message(self, format, *args):
            # 简化日志输出
            print(f"[{self.address_string()}] {format % args}")
    
    try:
        with socketserver.TCPServer(("", port), MyHTTPRequestHandler) as httpd:
            print(f"🎬 Bad Apple ASCII Player Server")
            print(f"📁 服务目录: {os.getcwd()}")
            print(f"🌐 本地地址: http://localhost:{port}")
            print(f"📱 局域网地址: http://{get_local_ip()}:{port}")
            print(f"📄 直接访问: http://localhost:{port}/index.html")
            print()
            print("按 Ctrl+C 停止服务器")
            print("=" * 50)
            
            # 自动打开浏览器
            try:
                webbrowser.open(f'http://localhost:{port}/index.html')
                print("✅ 已自动在浏览器中打开 Bad Apple 播放器")
            except:
                print("⚠️  请手动在浏览器中打开: http://localhost:{port}/index.html")
            
            print("=" * 50)
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"端口 {port} 已被占用，尝试端口 {port + 1}")
            return start_server(port + 1)
        else:
            print(f"启动服务器失败: {e}")
            return False
    
    except KeyboardInterrupt:
        print("\n🛑 服务器已停止")
        return True

def get_local_ip():
    """获取本机IP地址"""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        return "127.0.0.1"

def main():
    print("🍎 Bad Apple ASCII Art Web Player Server")
    print("=" * 50)
    
    # 检查文件
    files_info = {
        'index.html': os.path.exists('index.html'),
        'frames.json': os.path.exists('frames.json'),
        'BadApple.mp4': os.path.exists('BadApple.mp4'),
        'generate_frames.py': os.path.exists('generate_frames.py')
    }
    
    print("📋 文件检查:")
    for filename, exists in files_info.items():
        status = "✅" if exists else "❌"
        size = ""
        if exists:
            try:
                size_bytes = os.path.getsize(filename)
                if size_bytes > 1024 * 1024:
                    size = f" ({size_bytes / 1024 / 1024:.1f} MB)"
                elif size_bytes > 1024:
                    size = f" ({size_bytes / 1024:.1f} KB)"
                else:
                    size = f" ({size_bytes} B)"
            except:
                pass
        print(f"  {status} {filename}{size}")
    
    print()
    
    if not files_info['frames.json']:
        print("⚠️  frames.json 不存在，需要先生成帧数据")
        if files_info['BadApple.mp4']:
            print("💡 运行以下命令生成帧数据:")
            print("   python3 generate_frames.py BadApple.mp4")
        else:
            print("❌ BadApple.mp4 视频文件也不存在")
        print()
        
        response = input("是否继续启动服务器? (y/N): ").lower().strip()
        if response != 'y':
            return
    
    # 启动服务器
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"无效端口号: {sys.argv[1]}，使用默认端口 8000")
    
    start_server(port)

if __name__ == "__main__":
    main()

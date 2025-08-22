# Bad Apple!! ASCII Art Player

一个将经典的《Bad Apple》视频转换为ASCII字符画并在终端和网页中播放的项目(使用Claude Sonnet4辅助完成）。

## 项目结构

```
BadApple/
├── BadApple.mp4           # 原视频文件
├── play_ascii.py          # 终端版播放器 (Python)
├── index.html             # 网页版播放器 (HTML/JS)
├── generate_frames.py     # 视频预处理脚本
├── frames.json            # 预处理的ASCII帧数据
├── server.py              # 本地测试服务器
└── README.md              # 说明文档
```

## 功能特性

### 🖥️ 终端版播放器 (`play_ascii.py`)
- **高性能渲染**: 使用NumPy向量化操作，播放流畅
- **自动居中显示**: 字符画在终端中自动居中
- **宽高比保持**: 保持原视频比例，画面不变形
- **自适应尺寸**: 根据终端大小自动调整字符画尺寸
- **调试模式**: 支持单帧调试和参数调整

### 🌐 网页版播放器 (`index.html`)
- **流畅播放**: 使用requestAnimationFrame实现平滑渲染
- **循环播放**: 打开网页自动开始循环播放
- **响应式设计**: 自动适应不同屏幕尺寸
- **播放控制**: 播放/暂停、重新开始、进度显示
- **键盘控制**: 空格键播放/暂停，R键重新开始，方向键快进/后退
- **时间显示**: 实时显示播放进度和总时长

## 使用方法

### 1. 终端版播放器

#### 依赖要求
```bash
pip install opencv-python numpy pillow
```

#### 基本播放
```bash
python3 play_ascii.py BadApple.mp4
```

#### 调试模式
```bash
# 显示第一帧
python3 play_ascii.py BadApple.mp4 --debug

# 显示指定帧（如第480帧）
python3 play_ascii.py BadApple.mp4 --debug 480
```

### 2. 网页版播放器

#### 文件准备
确保你有以下文件：
- `BadApple.mp4` - 视频文件

#### 步骤1: 生成帧数据
```bash
python3 generate_frames.py BadApple.mp4 frames.json
```

#### 步骤2: 启动本地服务器
```bash
python3 server.py
```

#### 步骤3: 在浏览器中访问
自动打开浏览器，或手动访问: `http://localhost:8000/index.html`

## 技术实现

### 核心算法
1. **视频解码**: 使用OpenCV读取视频帧
2. **图像处理**: 转换为灰度图并调整对比度/亮度
3. **尺寸缩放**: 保持宽高比的前提下缩放到适合显示的尺寸
4. **字符映射**: 将像素灰度值映射到ASCII字符集
5. **高性能渲染**: 使用requestAnimationFrame实现流畅播放
6. **性能优化**: 使用NumPy向量化操作替代循环

### ASCII字符集
```
" .'`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
```
从左到右按灰度递增排列，空格代表最暗（黑色），`@$`代表最亮（白色）。

### 渲染技术
- **requestAnimationFrame**: 提供浏览器优化的渲染循环
- **精确时间控制**: 避免累积误差，保持稳定帧率
- **内存优化**: 合理的缓存策略和数据结构

## 系统要求

### Python依赖
```bash
pip install opencv-python numpy pillow
```

### 浏览器要求
- 现代浏览器（Chrome, Firefox, Safari, Edge）
- 支持ES6和Fetch API
- 建议使用Chrome以获得最佳性能

## 控制方式

### 网页版键盘快捷键
- **空格键**: 播放/暂停
- **R键**: 重新开始
- **←→方向键**: 后退/前进10帧

### 终端版
- **Ctrl+C**: 停止播放

## 文件说明

### `play_ascii.py` - 终端播放器
- 实时视频处理和ASCII转换
- 支持调试模式和参数调整
- 自动适应终端尺寸

### `generate_frames.py` - 预处理脚本
- 将视频预处理为JSON格式的ASCII帧数据
- 减少网页版的实时计算负担
- 支持自定义输出参数

### `index.html` - 网页播放器
- 纯JavaScript实现，无需额外依赖
- 响应式设计，支持全屏播放
- 流畅的ASCII动画播放
- 丰富的播放控制功能

### `server.py` - 测试服务器
- 简单的HTTP服务器，用于本地测试
- 自动打开浏览器
- 支持跨域访问

## 注意事项

- 建议在较大的终端窗口中运行终端版以获得更好的效果
- 视频文件应为常见格式（mp4, avi等）
- 网页版播放效果取决于浏览器性能和屏幕分辨率

## 许可证

本项目仅供学习和娱乐用途。《Bad Apple》视频版权归原作者所有。

---


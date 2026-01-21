# 🚀 Enhanced Virtual Mouse

A next-generation hand gesture-controlled virtual mouse with advanced AI-powered gesture recognition, smooth tracking, and performance optimization.

## ✨ Key Features

### 🎯 **Enhanced Accuracy**
- **Adaptive gesture recognition** with confidence scoring
- **Smooth cursor tracking** with jitter reduction
- **Configurable sensitivity** for different users
- **Multi-gesture support** with intelligent conflict resolution

### ⚡ **Optimized Performance**
- **Real-time processing** at 30+ FPS
- **Low latency** (<20ms detection time)
- **Resource monitoring** and optimization
- **Configurable quality vs performance** trade-offs

### 🎮 **Easy to Use**
- **Interactive configuration wizard** for personalized settings
- **Visual feedback** with colored gesture indicators
- **On-screen instructions** and FPS counter
- **Multiple presets** (Beginner, Responsive, Precise)

### 🛠️ **Advanced Features**
- **Performance benchmarking** tools
- **Configuration management** system
- **Comprehensive logging** and diagnostics
- **Modular architecture** for easy customization

## 🖱️ Gesture Controls

| Gesture | Action | Visual Indicator |
|---------|--------|------------------|
| **Move Cursor** | Thumb + Index finger moderately close | Yellow + Purple dots |
| **Left Click** | Thumb + Index finger very close | Yellow + Purple dots flash |
| **Double Click** | Index + Middle fingers close | Yellow + Cyan dots flash |
| **Right Click** | Thumb + Index base close | Purple + Orange dots flash |
| **Scroll Up** | Thumb + Ring finger close | Purple + Green dots flash |
| **Scroll Down** | Thumb + Pinky finger close | Purple + Red dots flash |

## 🚀 Quick Start

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/vinaycraft/Virtual-Mouse-.git
cd Virtual-Mouse-

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration (Optional but Recommended)
```bash
# Run the configuration wizard
python config.py

# Or choose a preset directly:
# 1 = Precise (high accuracy)
# 2 = Responsive (balanced) 
# 3 = Beginner (forgiving)
```

### 3. Run the Application
```bash
# Enhanced version (recommended)
python virtual_mouse_enhanced.py

# Original version
python virtual_mouse.py
```

### 4. Performance Testing
```bash
# Run performance benchmark
python benchmark.py
```

## ⚙️ Configuration Options

### Preset Configurations
- **🎯 Precise**: High accuracy, less sensitive (for experienced users)
- **⚡ Responsive**: Balanced performance (recommended for most users)
- **👶 Beginner**: More forgiving gestures (for new users)

### Custom Settings
```python
# Distance thresholds (0.0-1.0, smaller = more sensitive)
click_threshold: 0.03
double_click_threshold: 0.02
right_click_threshold: 0.03
scroll_threshold: 0.03
move_threshold: 0.15

# Performance settings
smoothing_factor: 0.7  # 0.0-1.0, higher = smoother
action_cooldown: 0.3  # Seconds between actions
camera_fps: 30        # Camera frame rate
```

## 📊 Performance Metrics

The enhanced version includes real-time performance monitoring:
- **FPS Counter**: Displays current frame rate
- **CPU/Memory Usage**: Tracks resource consumption
- **Latency Measurement**: Detection processing time
- **Performance Score**: Overall system rating (0-100)

### Target Performance
- **FPS**: 30+ frames per second
- **Latency**: <20ms detection time
- **CPU Usage**: <20% average
- **Memory Usage**: <100MB

## 🛠️ Advanced Usage

### Custom Configuration
```python
from config import GestureConfig
from virtual_mouse_enhanced import VirtualMouse

# Create custom config
config = GestureConfig(
    click_threshold=0.025,
    smoothing_factor=0.8,
    camera_fps=60
)

# Run with custom config
mouse = VirtualMouse(config)
mouse.run()
```

### Performance Benchmarking
```python
from benchmark import PerformanceBenchmark

# Run comprehensive benchmark
benchmark = PerformanceBenchmark()
results = benchmark.run_full_benchmark()
benchmark.generate_report(results)
```

## 📁 File Structure

```
Virtual-Mouse-/
├── virtual_mouse_enhanced.py    # Main enhanced application
├── virtual_mouse.py             # Original version
├── config.py                    # Configuration system
├── benchmark.py                 # Performance testing
├── requirements.txt             # Dependencies
├── README.md                    # This file
└── virtual_mouse_config.json    # Generated configuration
```

## 🔧 System Requirements

- **Python**: 3.7 or higher
- **Operating System**: Windows, macOS, Linux
- **Camera**: USB webcam or built-in camera
- **Hardware**: Minimum 4GB RAM, dual-core CPU

### Recommended Hardware
- **CPU**: Intel i5 or AMD Ryzen 5 (or better)
- **RAM**: 8GB or more
- **Camera**: 720p webcam at 30fps
- **USB**: 3.0 port for camera

## 🐛 Troubleshooting

### Common Issues

**Camera not detected**
```bash
# Check camera devices
python -c "import cv2; print([i for i in range(10) if cv2.VideoCapture(i).read()[0]])"
```

**Low performance**
- Reduce camera resolution in config
- Lower confidence thresholds
- Close other applications

**Gesture recognition issues**
- Ensure good lighting
- Position hand 1-2 feet from camera
- Run configuration wizard for calibration

### Performance Optimization
```bash
# Use lower resolution for better performance
python config.py
# Choose "Responsive" preset or custom settings
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python benchmark.py

# Create new features
# 1. Fork the repository
# 2. Create a feature branch
# 3. Make your changes
# 4. Test with benchmark.py
# 5. Submit a pull request
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [MediaPipe](https://mediapipe.dev/) for hand tracking
- [OpenCV](https://opencv.org/) for computer vision
- [PyAutoGUI](https://pyautogui.readthedocs.io/) for mouse control

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section
2. Run the performance benchmark
3. Create an issue on GitHub
4. Include your system specs and benchmark results

---

**🚀 Experience the future of human-computer interaction!**

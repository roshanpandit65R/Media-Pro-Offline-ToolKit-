# Media Pro Offline Tool

A comprehensive GUI-based video and audio processing toolkit with AI-powered features and natural language command processing.

## 🎯 Overview

MediaForge Pro is a modern, user-friendly desktop application that provides professional-grade video and audio processing capabilities. Built with Python and Tkinter, it offers both traditional processing options and cutting-edge AI features like automatic noise reduction, subtitle generation, and natural language command processing.

## ✨ Key Features

### 📁 File Management
- Drag-and-drop interface for multiple file selection
- Batch processing support
- Folder scanning for media files
- Real-time file information display (size, format, duration)

### 🔄 Format Conversion
- Support for all major video formats (MP4, AVI, MOV, MKV, WMV, FLV)
- Audio format conversion (MP3, WAV, FLAC, AAC, OGG)
- Quality presets (High, Medium, Low)
- Smart compression with target file size

### ✂️ Trimming & Cropping
- Precise time-based trimming (HH:MM:SS format)
- Video cropping with custom dimensions and positioning
- Lossless copying for fast processing
- Real-time preview capabilities

### 🤖 AI-Powered Features
- **Noise Reduction**: Advanced AI-based audio denoising
- **Subtitle Generation**: Automatic transcription using OpenAI Whisper
- **Multi-language Support**: Auto-detection or manual language selection
- **Smart Compression**: Intelligent quality optimization

### 💬 Natural Language Processing
- Process files using plain English commands
- Examples:
  - "convert to mp3"
  - "trim from 00:30 to 01:30"
  - "compress to 50MB"
  - "extract audio"
  - "resize to 720x480"

### 📊 Professional Interface
- Modern dark theme with intuitive navigation
- Real-time progress tracking
- Comprehensive logging system
- Status updates and error handling

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- FFmpeg (required for video/audio processing)

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space for temporary files
- **CPU**: Multi-core processor recommended for faster processing

### Install FFmpeg

#### Windows
1. Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extract to a folder (e.g., `C:\ffmpeg`)
3. Add to system PATH: `C:\ffmpeg\bin`

#### macOS
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

### Install Python Dependencies
```bash
pip install openai-whisper moviepy librosa noisereduce pydub scipy
```

### Alternative: Install with requirements.txt
```bash
pip install -r requirements.txt
```

Create `requirements.txt`:
```
openai-whisper>=20230314
moviepy>=1.0.3
librosa>=0.10.0
noisereduce>=3.0.0
pydub>=0.25.1
scipy>=1.10.0
numpy>=1.24.0
```

## 🚀 Quick Start

1. **Launch the application**:
   ```bash
   python mediaforge_pro.py
   ```

2. **Select files**: Use the "Files" tab to add your media files

3. **Choose processing type**:
   - **Convert**: Change format or quality
   - **Trim/Crop**: Edit video dimensions or duration
   - **AI Process**: Use advanced AI features
   - **Natural Language**: Use plain English commands

4. **Monitor progress**: Check the "Logs" tab for detailed processing information

## 📋 Usage Examples

### Basic Conversion
1. Go to "Convert" tab
2. Select input file
3. Choose output format (MP3, MP4, etc.)
4. Set quality level
5. Click "Start Conversion"

### AI Noise Reduction
1. Go to "AI Process" tab
2. Select audio file
3. Click "Remove Audio Noise"
4. Wait for AI processing to complete

### Subtitle Generation
1. Go to "AI Process" tab
2. Select video file
3. Choose language (or auto-detect)
4. Click "Generate Subtitles"
5. SRT file will be created automatically

### Natural Language Commands
1. Go to "Natural Language" tab
2. Select input file
3. Type command like: "compress video to 100MB"
4. Click "Process Command"

## 🎛️ Advanced Features

### Smart Compression
The AI-powered smart compression feature analyzes your video content and applies optimal compression settings:
- **High Quality**: Preserves visual fidelity (CRF 18)
- **Balanced**: Good quality-to-size ratio (CRF 23)
- **Fast**: Quick processing with smaller file size (CRF 28)

### Batch Processing
Process multiple files simultaneously:
1. Select multiple files in the Files tab
2. Choose your processing options
3. The application will queue and process files automatically

### Custom Output Naming
Files are automatically renamed to prevent overwrites:
- `video_converted.mp4`
- `audio_denoised.wav`
- `video_trimmed.mp4`

## 🔧 Configuration

### Performance Optimization
- **CPU Usage**: The application automatically uses available CPU cores
- **Memory Management**: Large files are processed in chunks to prevent memory overflow
- **Temporary Files**: Automatically cleaned up after processing

### Quality Settings
Adjust processing quality based on your needs:
- **High**: Best quality, slower processing
- **Medium**: Balanced quality and speed
- **Low**: Fastest processing, smaller file size

## 📝 Troubleshooting

### Common Issues

**FFmpeg not found error**:
- Ensure FFmpeg is installed and added to system PATH
- Restart the application after installing FFmpeg

**Out of memory error**:
- Close other applications to free up RAM
- Process smaller files or reduce quality settings

**Slow processing**:
- Use "Fast" quality preset for quicker results
- Ensure your system meets minimum requirements

**Audio sync issues**:
- Use "copy" codec for trimming to avoid re-encoding
- Check that input file is not corrupted

### Error Logs
Check the "Logs" tab for detailed error information. Common error codes:
- **Exit code 1**: FFmpeg processing error
- **Permission denied**: Check file write permissions
- **Codec not supported**: Try different output format

## 🧪 Testing

The application includes comprehensive error handling and validation:
- Input file format validation
- Output directory write permissions
- FFmpeg availability check
- Memory usage monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

### Development Setup
```bash
git clone https://github.com/yourusername/mediaforge-pro.git
cd mediaforge-pro
pip install -r requirements.txt
python mediaforge_pro.py
```
## Images 
![alt text](<Screenshot 2025-08-29 123522.png>) ![alt text](<Screenshot 2025-08-29 123340.png>) ![alt text](<Screenshot 2025-08-29 123406.png>) ![alt text](<Screenshot 2025-08-29 123426.png>) ![alt text](<Screenshot 2025-08-29 123437.png>) ![alt text](<Screenshot 2025-08-29 123514.png>)
## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI Whisper**: For speech-to-text capabilities
- **FFmpeg**: For multimedia processing framework
- **MoviePy**: For video editing functionality
- **Librosa**: For audio analysis
- **NoiseReduce**: For audio denoising algorithms





---

**MediaPro** - Professional media processing made simple.

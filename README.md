# 🎬 Reddit Stories Video Generator

Automatically create engaging TikTok/YouTube Shorts-style videos from Reddit stories with AI-generated voiceovers and subtitles!

This tool scrapes stories from Reddit, converts them to speech using Text-to-Speech, overlays them on background video footage, and adds auto-generated subtitles - all with just one command.

## ✨ Features

- 🤖 **Automated Reddit Scraping** - Fetches trending stories from any subreddit (default: r/AmItheAsshole)
- 🎙️ **AI Text-to-Speech** - Converts text to natural-sounding voiceovers
- ⚡ **Audio Enhancement** - Automatically speeds up audio for better engagement
- 🎥 **Video Generation** - Combines background footage with generated audio
- 📝 **Auto Subtitles** - AI-powered subtitle generation using Whisper
- 🎨 **Professional Output** - Ready-to-upload vertical videos with burned-in captions

## 🎥 Demo

<!-- Add your demo video here -->
*Demo video coming soon!*

## 📋 Prerequisites

- **Python**: 3.9.0 to <3.12.0
- **SoX**: Audio processing library
- **FFmpeg**: Video encoding and subtitle burning
- **macOS/Linux**: (Windows users may need adjustments)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/lincolnkermit/reddit-stories.git
cd reddit-stories
```

### 2. Install System Dependencies

**macOS (using Homebrew):**
```bash
brew install sox ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install sox ffmpeg
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Background Video

Place your background video file at:
```
data/videos/sample.mp4
```

You can use any video (gaming footage, nature scenes, etc.). The script will randomly cut segments to match the audio length.
An example is already available.

### 5. Add Audio Ding (Optional)

The script uses a "ding" sound between the title and story. Place your ding sound at:
```
data/audio/ding.wav
```

## 🎯 Usage

### Quick Start

Simply run the main script:

```bash
cd src/
python3 main.py
```

The script will:
1. Fetch a story from r/AmItheAsshole
2. Generate TTS audio for title and content
3. Speed up the audio for better pacing
4. Combine audio with background video
5. Generate and burn subtitles into the video
6. Save the final video to `output/`

### Development Mode

To keep temporary files for debugging:

```bash
# Edit src/main.py and set:
dev_mode = True
```

### Customize Subreddit

To scrape from a different subreddit, edit [src/main.py](src/main.py#L78):

```python
run(dev_mode=dev_mode, theme="AmItheAsshole"):  # Change this at the line 78
```

## 📁 Project Structure

```
reddit-stories/
├── data/
│   ├── audio/          # Audio assets (ding.wav)
│   ├── videos/         # Background videos (sample.mp4)
│   └── stories/        # Scraped story data
├── output/             # Final generated videos
├── temp/               # Temporary processing files
├── src/
│   ├── main.py         # Main orchestration script
│   ├── reddit_scraper.py   # Reddit scraping logic
│   ├── reddit_story.py     # Story text extraction
│   ├── audio_editor.py     # TTS and audio processing
│   ├── video_editor.py     # Video creation and editing
│   ├── subtitles.py        # Subtitle generation
│   └── lib/YARS/       # Reddit scraping library
└── requirements.txt    # Python dependencies
```

## 🛠️ Configuration

### Python Version
Ensure you're using Python 3.9.0 to <3.12.0. Check with:
```bash
python3 --version
```

### Audio Speed
Adjust the audio speed multiplier in [src/audio_editor.py](src/audio_editor.py)

### Subtitle Styling
Customize subtitle appearance in [src/subtitles.py](src/subtitles.py)

## 🐛 Troubleshooting

### "SoX is not installed"
```bash
brew install sox  # macOS
sudo apt install sox  # Linux
```

### "ffmpeg must be installed"
```bash
brew install ffmpeg  # macOS
sudo apt install ffmpeg  # Linux
```

### Module Import Errors
Make sure you're in the `src/` directory when running:
```bash
cd src
python3 main.py
```

### Subtitle Generation Fails
Ensure ffmpeg is properly installed and accessible in your PATH:
```bash
ffmpeg -version
```

## 📝 Dependencies

- **requests** - HTTP requests for Reddit scraping
- **beautifulsoup4** - HTML parsing
- **TTS** - Text-to-Speech generation
- **moviepy** - Video editing and processing
- **pydub** - Audio manipulation
- **whisper** - AI subtitle generation
- **yt-dlp** - Video downloading utilities

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is for educational purposes. Respect Reddit's terms of service and content creators' rights when using this tool.

## ⚠️ Disclaimer

- Always credit original Reddit authors when posting content
- Follow subreddit rules and Reddit's API terms
- Use responsibly and ethically
- This tool is for educational and personal use

## 🙏 Credits

- **YARS** - Reddit scraping library
- **OpenAI Whisper** - Subtitle generation
- **Coqui TTS** - Text-to-Speech engine

---

Made with ❤️ for content creators




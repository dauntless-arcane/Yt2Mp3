# Yt2Mp3
YouTube to MP3 Converter 🎵
A lightweight web application to convert YouTube videos to MP3 audio files using Flask, `yt-dlp`, and FFmpeg.

## 🚀 Features

- Input a YouTube video URL
- Converts and downloads the audio as an MP3 file
- Simple and responsive HTML front-end (no React)
- Uses `yt-dlp` and `ffmpeg` for fast, high-quality conversions


## 🛠 Requirements

- Python 3.7+
- `yt-dlp`
- `ffmpeg`
- Flask

## ⚙️ Setup Instructions

1. **Clone the repo**

```bash
git clone https://github.com/yourusername/yt2mp3-flask.git
cd yt2mp3-flask
```

2. **Install dependencies**
   pip install flask yt-dlp

3. **Ensure ffmpeg is installed and added to your PATH**
    Download from: https://ffmpeg.org/download.html
    Or set ffmpeg_location in ydl_opts if not globally available.

4.**Run the Flask server**
    python server.py
    
5.**Access the app**
    Visit: http://127.0.0.1:5000/ in your browser

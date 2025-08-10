import os
import re
from flask import Flask, request, jsonify, send_from_directory, send_file
import yt_dlp


app = Flask(__name__)

# Directory to save the downloaded MP3 files
downloads_dir = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(downloads_dir):
    os.makedirs(downloads_dir)

def sanitize_filename(filename):
    # Remove forbidden characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Trim trailing spaces or dots (Windows disallows those)
    filename = filename.rstrip(' .')
    # Optional: replace spaces with underscores
    # filename = filename.replace(' ', '_')
    return filename

@app.route('/')
def home():
    return send_from_directory(os.path.join(os.getcwd(), 'static'), 'index.html')

@app.route('/convert', methods=['GET'])
def convert_to_mp3():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Please provide a YouTube URL'}), 400

    try:
        # yt-dlp options with MP3 conversion
        ydl_opts = {
            'format': 'bestaudio/best',  # Best audio format
            'extractaudio': True,  # Extract audio only
            'audioquality': 1,  # Best audio quality
            'outtmpl': os.path.join(downloads_dir, '%(title)s.%(ext)s'),  # Output path
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',  # Correct postprocessor key for audio conversion
                'preferredcodec': 'mp3',  # Convert to MP3
                'preferredquality': '192',  # Set MP3 quality
            }],
            'ffmpeg_location': r'C:\Users\tharu\Downloads\ffmpeg-7.1.1-essentials_build\bin',
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0'
            },
            # Uncomment the line below if you have a cookies.txt file
            # 'cookiefile': 'path/to/cookies.txt',  # Optional, if needed
        }

        # Download and convert the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = info_dict.get('title', 'unknown')
            sanitized_title = sanitize_filename(title)
            base_filename = ydl.prepare_filename(info_dict)  # full path with original extension
            mp3_filename = os.path.splitext(base_filename)[0] + '.mp3'


        return send_file(mp3_filename, as_attachment=True, download_name=f'{sanitized_title}.mp3')

    except yt_dlp.utils.DownloadError as e:
        return jsonify({'error': f'Download error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Serve the downloads folder
@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(downloads_dir, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)

import os
import re
from flask import Flask, request, jsonify, send_from_directory, send_file
import yt_dlp
import tempfile

app = Flask(__name__)

def sanitize_filename(filename):
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    return filename.rstrip(' .')
STATIC_DIR = os.path.join(os.path.dirname(__file__), '..', 'static')
@app.route('/')
def home():
    return send_from_directory(STATIC_DIR, 'index.html')

@app.route('/convert', methods=['GET'])
def convert_to_mp3():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Please provide a YouTube URL'}), 400

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'headers': {
                    'User-Agent': 'Mozilla/5.0'
                }
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                title = sanitize_filename(info_dict.get('title', 'unknown'))
                base_filename = ydl.prepare_filename(info_dict)
                mp3_filename = os.path.splitext(base_filename)[0] + '.mp3'

            return send_file(mp3_filename, as_attachment=True, download_name=f'{title}.mp3')

    except yt_dlp.utils.DownloadError as e:
        return jsonify({'error': f'Download error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Expose for Vercel
app = app

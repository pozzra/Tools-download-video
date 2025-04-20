import os
import yt_dlp
import instaloader
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # Handle Cross-Origin Resource Sharing

app = Flask(__name__)

# Enable CORS
CORS(app)

# Folder to save downloads
output_folder = "downloads"
os.makedirs(output_folder, exist_ok=True)

# Downloader class
class VideoDownloader:
    def __init__(self, output_folder=output_folder):
        self.output_folder = output_folder
        self.progress = 0
        self.update_callback = None

    def download_with_ytdlp(self, url, folder):
        download_folder = os.path.join(self.output_folder, folder)
        os.makedirs(download_folder, exist_ok=True)

        ydl_opts = {
            'outtmpl': f'{download_folder}/%(title)s.%(ext)s',
            'format': 'best',
            'progress_hooks': [self.progress_hook],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return info.get('title', 'Unknown Title')

    def download_instagram_post(self, url, folder):
        download_folder = os.path.join(self.output_folder, folder)
        os.makedirs(download_folder, exist_ok=True)

        loader = instaloader.Instaloader(dirname_pattern=download_folder, save_metadata=False)
        shortcode = url.rstrip('/').split('/')[-1]  # Fix splitting issue
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, target="instagram")
        return "Instagram Post"

    def download(self, platform, url, folder):
        platform = platform.lower()
        if platform in ["youtube", "facebook", "tiktok", "kuaishou"]:
            return self.download_with_ytdlp(url, folder)
        elif platform == "instagram":
            return self.download_instagram_post(url, folder)
        else:
            raise ValueError(f"Platform '{platform}' not supported.")

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            percent_str = d.get('_percent_str', '0%').strip().replace('%', '')
            try:
                self.progress = float(percent_str)
                if self.update_callback:
                    self.update_callback(self.progress)
            except ValueError:
                pass

    def set_progress_callback(self, callback):
        self.update_callback = callback

# Routes
@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    platform = data.get('platform')
    url = data.get('url')
    folder = data.get('folder', 'default')  # Default folder name if not given

    if not platform or not url:
        return jsonify({"error": "Platform and URL are required!"}), 400

    downloader = VideoDownloader()

    def progress_callback(progress):
        print(f"Download Progress: {progress}%")

    downloader.set_progress_callback(progress_callback)

    try:
        title = downloader.download(platform, url, folder)
        return jsonify({"status": "success", "title": title, "progress": downloader.progress})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(output_folder, filename)

# Start server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

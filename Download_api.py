import os
import yt_dlp
import instaloader
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

output_folder = "downloads"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

class VideoDownloader:
    def __init__(self, output_folder=output_folder):
        self.output_folder = output_folder
        self.progress = 0

    def download_with_ytdlp(self, url, folder):
        download_folder = os.path.join(self.output_folder, folder)
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        ydl_opts = {
            'outtmpl': f'{download_folder}/%(title)s.%(ext)s',
            'format': 'best',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return info.get('title', 'Unknown Title')

    def download_instagram_post(self, url, folder):
        download_folder = os.path.join(self.output_folder, folder)
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        loader = instaloader.Instaloader(dirname_pattern=download_folder, save_metadata=False)
        shortcode = url.split("/")[-2]
        loader.download_post(instaloader.Post.from_shortcode(loader.context, shortcode), target="instagram")
        return "Instagram Post"

    def download(self, platform, url, folder):
        if platform.lower() in ["youtube", "facebook", "tiktok", "kuaishou"]:
            return self.download_with_ytdlp(url, folder)
        elif platform.lower() == "instagram":
            return self.download_instagram_post(url, folder)
        else:
            raise ValueError(f"Platform {platform} not supported yet.")

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    platform = data.get('platform')
    url = data.get('url')
    folder = data.get('folder', '')

    if not platform or not url:
        return jsonify({"error": "Platform and URL are required!"}), 400

    downloader = VideoDownloader()

    try:
        title = downloader.download(platform, url, folder)
        return jsonify({"status": "success", "title": title})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(output_folder, filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

import os
import yt_dlp
import instaloader
from flask import Flask, request, jsonify, send_from_directory, Response, stream_with_context
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

output_folder = "downloads"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

class VideoDownloader:
    def __init__(self, output_folder=output_folder):
        self.output_folder = output_folder
        self.progress = 0  # Progress as a percentage
        self.update_callback = None  # A callback function for progress updates

    def download_with_ytdlp(self, url, folder):
        download_folder = os.path.join(self.output_folder, folder)
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        ydl_opts = {
            'outtmpl': f'{download_folder}/%(title)s.%(ext)s',
            'format': 'best',
            'progress_hooks': [self.progress_hook],  # Hook for tracking progress
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

    def progress_hook(self, d):
        """
        A hook function to update the download progress.
        """
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0%').strip()
            percent = percent.replace('%', '').strip()
            try:
                self.progress = float(percent)
                if self.update_callback:
                    self.update_callback(self.progress)
            except ValueError:
                pass

    def set_progress_callback(self, callback):
        self.update_callback = callback


@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    platform = data.get('platform')
    url = data.get('url')
    folder = data.get('folder', '')

    if not platform or not url:
        return jsonify({"error": "Platform and URL are required!"}), 400

    downloader = VideoDownloader()

    def progress_callback(progress):
        # Here you can store the progress in a global variable or send periodic updates
        print(f"Download Progress: {progress}%")

    downloader.set_progress_callback(progress_callback)

    try:
        title = downloader.download(platform, url, folder)
        return jsonify({"status": "success", "title": title, "progress": downloader.progress})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/download_file/<filename>', methods=['GET'])
def download_file(filename):
    # Send the file as a response (this will trigger the file download on the client)
    return send_from_directory(output_folder, filename, as_attachment=True)


@app.route('/progress', methods=['GET'])
def get_progress():
    # This endpoint can be used for progress tracking (example: check the progress of a current download)
    # Here we can store progress in a shared variable or use a more complex method to track multiple downloads
    # Currently it returns the last download progress, which might need to be adjusted for multiple concurrent downloads.
    downloader = VideoDownloader()  # You could make this a global object if tracking progress for a specific file
    return jsonify({"progress": downloader.progress})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)  # Allow frontend (JS) to connect without CORS issues

# Home route - Show success page
@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Server Running!</title>
      <style>
        body {
          background: linear-gradient(135deg, #00c6ff, #0072ff);
          color: white;
          font-family: 'Arial', sans-serif;
          text-align: center;
          padding-top: 100px;
          height: 100vh;
          margin: 0;
          overflow: hidden;
        }
        h1 {
          font-size: 3em;
          margin-bottom: 20px;
          animation: pop 0.6s ease;
        }
        p {
          font-size: 1.5em;
        }
        @keyframes pop {
          0% { transform: scale(0); opacity: 0; }
          100% { transform: scale(1); opacity: 1; }
        }
        .bubbles {
          position: absolute;
          width: 100%;
          height: 100%;
          top: 0;
          left: 0;
          overflow: hidden;
          z-index: 0;
        }
        .bubble {
          position: absolute;
          bottom: -100px;
          width: 40px;
          height: 40px;
          background: rgba(255, 255, 255, 0.15);
          border-radius: 50%;
          animation: rise 10s infinite ease-in;
        }
        @keyframes rise {
          0% {
            transform: translateY(0) scale(1);
            opacity: 1;
          }
          100% {
            transform: translateY(-1200px) scale(0.5);
            opacity: 0;
          }
        }
      </style>
    </head>
    <body>
      <div class="bubbles">
        <div class="bubble" style="left:10%; animation-duration:8s;"></div>
        <div class="bubble" style="left:20%; animation-duration:9s;"></div>
        <div class="bubble" style="left:25%; animation-duration:7s;"></div>
        <div class="bubble" style="left:40%; animation-duration:11s;"></div>
        <div class="bubble" style="left:55%; animation-duration:10s;"></div>
        <div class="bubble" style="left:70%; animation-duration:8s;"></div>
        <div class="bubble" style="left:80%; animation-duration:12s;"></div>
      </div>
      <h1>✅ Server is Running Successfully!</h1>
      <p>Listening on <b>http://127.0.0.1:5000</b></p>
      <p>Ready to accept video downloads 🎥</p>
    </body>
    </html>
    ''')

# Download route - API
@app.route('/download', methods=['POST'])
def download_video():
    try:
        data = request.get_json()
        platform = data.get('platform')
        url = data.get('url')
        quality = data.get('quality')

        if not url:
            return jsonify({"error": "URL is required."}), 400

        print(f"Downloading from {platform} - {url} at {quality} quality...")
        time.sleep(2)  # simulate download delay

        return jsonify({
            "message": "Download successful",
            "title": f"Video from {platform} ({quality})"
        }), 200

    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

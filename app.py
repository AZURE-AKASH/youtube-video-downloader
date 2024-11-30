from flask import Flask, request, render_template, send_file
import yt_dlp
import os

app = Flask(__name__)

def download_video(url):
    # Set up options for yt-dlp
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save the file in a downloads folder
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    download_video(url)
    # Assuming the file is downloaded in the downloads folder
    # Get the latest file in the downloads directory
    files = os.listdir('downloads')
    latest_file = max([os.path.join('downloads', f) for f in files], key=os.path.getctime)
    return send_file(latest_file, as_attachment=True)

if __name__ == "__main__":
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)
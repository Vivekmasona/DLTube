# type: ignore
from flask import Flask, render_template, request, send_file
import os
import yt_dlp as youtube_dl
import re
from pytz import timezone
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    invalid_url = False
    if request.method == "POST":
        youtube_url = request.form["youtube_url"]
        selected_format = request.form["format"]
        if is_valid_url(youtube_url):
            file = download_media(youtube_url, selected_format)
            try:
                return send_file(file, as_attachment=True)
            except:
                return render_template("index.html", invalid_url=True)
            finally:
                os.remove(file)
        else:
            invalid_url = True
    else:
        invalid_url = False
    return render_template("index.html", invalid_url=invalid_url)

def is_valid_url(url):
    youtube_regex = r"(?:https?:\/\/(?:www\.)?)?(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})"
    match = re.match(youtube_regex, url)
    if match:
        return True
    return False

def download_media(url, selected_format):
    ydl_opts = {
        "format": "bestaudio" if selected_format == "mp3" else "best",
        "outtmpl": "%(title)s.%(ext)s",
        "no_playlist": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "160"
            }
        ] if selected_format == "mp3" else []
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        media_file = ydl.prepare_filename(info_dict)
        base, ext = os.path.splitext(media_file)
        output_file = base + f".{selected_format}"

    return output_file

def get_login_time(tz: str) -> str:
    return f"\nLogged in at {datetime.now(timezone(tz)).strftime('%m/%d/%Y, %I:%M:%S %p')}\nTimezone: {tz}\n"

print(get_login_time('US/Eastern'))
app.run(host='0.0.0.0', port=80)

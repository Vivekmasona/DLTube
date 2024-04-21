# type: ignore
from flask import Flask, render_template, request, send_file
import os
import re
import subprocess
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
    process = ['yt-dlp', '-x', '--audio-format', selected_format, '--no-playlist', '-o', '%(title)s.%(ext)s', url] if selected_format == 'mp3' else ['yt-dlp', '-f', 'best', '--no-playlist', '-o', '%(title)s.%(ext)s', url]
    subprocess.run(process)

    new_files = [file for file in os.listdir('.') if file.endswith(".mp3")] if selected_format == "mp3" else [file for file in os.listdir('.') if file.endswith(".mp4")]
    output_file = new_files[0]
    return output_file

def get_login_time(tz: str) -> str:
    return f"\nLogged in at {datetime.now(timezone(tz)).strftime('%m/%d/%Y, %I:%M:%S %p')}\nTimezone: {tz}\n"

print(get_login_time('US/Eastern'))
app.run(host='0.0.0.0', port=80)

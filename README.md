# DLTube
Simple YouTube -> MP3/4 Downloader written in Flask framework. Deployed [here](https://dltube.onrender.com), but the requirements and instructions below are for if you want to host this application locally.

# Requirements
1. [Python](https://www.python.org/downloads/) (install the latest version)
2. [ffmpeg](https://www.hostinger.com/tutorials/how-to-install-ffmpeg) (Install the latest version)

# Instructions
1. `git clone` this repository in your Terminal
2. `cd` to this repository in Terminal
3. `pip install -r requirements.txt` in Terminal
4. At line 47 of `main.py`, add a line inside the `ydl_opts` dictionary to point to your ffmpeg installation. Should look something like `'ffmpeg_location': 'path/to/ffmpeg/installation/'`
5. `python3 main.py` in Terminal
6. The terminal should have generated an IP address at which your `localhost` is live. Enter that IP address in your browser search bar.
7. `Ctrl+C` in Terminal when finished with your downloading. Alternatively, just leave your Terminal session open for theoretical 24/7 access to the site.

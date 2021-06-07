from math import trunc
from flask import Flask, jsonify, send_file, render_template,Response
import os
import youtube_dl
from youtubesearchpython import VideosSearch,Video
import pafy


ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
# Add all the available extractors
ydl.add_default_info_extractors()


app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Welcome"


@app.route('/youtube-data/<string:n>')
def youtubeMusic(n):
    videosSearch = VideosSearch(n, limit=20)

    videos = videosSearch.result()
    videos1 = videos['result']
    return jsonify(videos1)


@app.route('/mp3/<string:s>')
def mp3Down(s):
    result = ydl.extract_info(f'https://www.youtube.com/watch?v={s}'
,   download=False # We just want to extract the info
    )

    if 'entries' in result:
    # Can be a playlist or a list of videos
        Video = result ['entries'] [0]
    else:
    # Just a video
        video = result



    # url=f"https://www.youtube.com/watch?v={s}"
    # video =  pafy.new(url)
    # audiostreams=video.audiostreams
    # # print(audiostreams[3].url)
    return jsonify(video['formats'][0]['url'])


@app.route('/delete/<string:file>')
def after_request_func(file):

    os.remove(file)
    return "done"


if __name__ == "__main__":
    app.run(debug=True, port=5000)

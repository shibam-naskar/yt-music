from math import trunc
from flask import Flask, jsonify, send_file, render_template,Response
import os
import youtube_dl
from youtubesearchpython import VideosSearch,Video


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],

}



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


@app.route('/mp3/<string:s>/<string:n>')
def mp3Down(s, n):
    listning = os.walk('.')
    n1 = ""
    if(n[-1]=="|"):
        n1 = n[:-1]
    else:
        n1 = n
    n1 = n1.replace("|", "_")
    n1 = n1.replace(":"," -")
    n1 = n1.replace("amp;","")
    path = str(n1)+"-"+str(s)+".mp3"
    for root_path, directories, files in listning:
        if path in files:
            def generate():
                with open(path, "rb") as fwav:
                    data = fwav.read(1024)
                    while data:
                        yield data
                        data = fwav.read(1024)
            return Response(generate(), mimetype="audio/mp3")
        else:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download(['https://www.youtube.com/watch?v={}'.format(s)])

                def generate():
                    with open(path, "rb") as fwav:
                        data = fwav.read(1024)
                        while data:
                            yield data
                            data = fwav.read(1024)
                return Response(generate(), mimetype="audio/mp3")



@app.route('/delete/<string:file>')
def after_request_func(file):

    os.remove(file)
    return "done"


if __name__ == "__main__":
    app.run(debug=True, port=5000)

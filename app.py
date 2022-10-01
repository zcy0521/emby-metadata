from flask import Flask, render_template, request

import metadata2
from jav import FANZA

app = Flask(__name__)


# https://flask.palletsprojects.com/en/2.1.x/quickstart/
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/poster")
def poster():
    video_no = request.args.get('video_no')
    if video_no is None:
        return render_template('poster.html', video_no='')

    videos = []
    for number in video_no.upper().split(','):
        video = metadata2.get_jav(number.strip())
        if video is not None:
            video = {'number': video_no, 'poster_url': video.get_poster_url()}
            videos.append(video)

    return render_template('poster.html', video_no=video_no, videos=videos)


@app.route("/fanart")
def fanart():
    video_no = request.args.get('video_no')
    if video_no is None:
        return render_template('fanart.html', video_no='')

    videos = []
    for number in video_no.upper().split(','):
        video = metadata2.get_jav(number.strip())
        if video is not None:
            video = {'number': video_no, 'fanart_url': video.get_fanart_url()}
            videos.append(video)

    return render_template('fanart.html', video_no=video_no, videos=videos)


@app.route("/movie")
def movie():
    video_no = request.args.get('video_no')
    if video_no is None:
        return render_template('movie.html', video_no='')

    videos = []
    for number in video_no.upper().split(','):
        video = metadata2.get_jav(number.strip())
        if video is not None:
            video = {'number': video_no, 'movie_url': video.get_movie_url(), 'fanart_url': video.get_fanart_url()}
            videos.append(video)

    return render_template('movie.html', video_no=video_no, videos=videos)


@app.route("/fanza")
def fanza():
    #
    video_no = request.args.get('video_no')
    if video_no is None:
        return render_template('fanza.html', video_no='')

    videos = FANZA.search_videos(video_no)
    print('查询完成')
    return render_template('fanza.html', video_no=video_no, videos=videos)


@app.route("/magnet")
def magnet():
    video_no = request.args.get('video_no')
    return render_template('magnet.html', video_no=video_no,)

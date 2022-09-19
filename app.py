from flask import Flask, render_template, request

import metadata2

app = Flask(__name__)


# https://flask.palletsprojects.com/en/2.1.x/quickstart/
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/poster")
def poster():
    video_no = request.args.get('video_no')
    if video_no is not None:
        video_no = video_no.upper()

    # 查询编号为空
    if video_no is None:
        return render_template('poster.html', video_no='', posters=[])

    # 循环处理编号
    videos = []
    for number in video_no.split(','):
        video = metadata2.get_jav(number)
        if video is None:
            videos.append(Video('', '', '', ''))
        else:
            videos.append(Video(number, video.poster_url, '', ''))

    return render_template('poster.html', video_no=video_no, videos=videos)


@app.route("/fanart")
def fanart():
    video_no = request.args.get('video_no')
    if video_no is not None:
        video_no = video_no.upper()

    # 查询编号为空
    if video_no is None:
        return render_template('fanart.html', video_no='', posters=[])

    # 循环处理编号
    videos = []
    for number in video_no.split(','):
        video = metadata2.get_jav(number)
        if video is None:
            videos.append(Video('', '', '', ''))
        else:
            videos.append(Video(number, '', video.fanart_url, ''))

    return render_template('fanart.html', video_no=video_no, videos=videos)


@app.route("/movie")
def movie():
    video_no = request.args.get('video_no')
    if video_no is not None:
        video_no = video_no.upper()

    # 查询编号为空
    if video_no is None:
        return render_template('movie.html', video_no='', posters=[])

    # 循环处理编号
    videos = []
    for number in video_no.split(','):
        video = metadata2.get_jav(number)
        if video is None:
            videos.append(Video('', '', '', ''))
        else:
            videos.append(Video(number, '', '', video.movie_url))

    return render_template('movie.html', video_no=video_no, videos=videos)


@app.route("/magnet")
def magnet():
    video_no = request.args.get('video_no')
    return render_template('magnet.html')


class Video:
    def __init__(self, number, poster, fanart, movie):
        self.number = number
        self.poster = poster
        self.fanart = fanart
        self.movie = movie

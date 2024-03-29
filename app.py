from flask import Flask, render_template, request

import metadata2
from jav import FANZA, SOD, Prestige, MGS

app = Flask(__name__)


# https://flask.palletsprojects.com/en/2.1.x/quickstart/
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/poster")
def poster():
    video_no = request.args.get('video_no')

    if video_no is None:
        return render_template('poster.html')

    videos = []
    for number in video_no.upper().split(','):
        video = metadata2.get_jav(number.strip())
        if video is not None:
            video = {'number': video.video_no, 'url': video.detail_url, 'poster_url': video.poster_url,
                     'fanart_url': video.fanart_url}
            videos.append(video)
    return render_template('poster.html', video_no=video_no, videos=videos)


@app.route("/fanart")
def fanart():
    video_no = request.args.get('video_no')

    if video_no is None:
        return render_template('fanart.html')

    videos = []
    for number in video_no.upper().split(','):
        video = metadata2.get_jav(number.strip())
        if video is not None:
            video = {'number': video.video_no, 'url': video.detail_url, 'fanart_url': video.fanart_url}
            videos.append(video)
    return render_template('fanart.html', video_no=video_no, videos=videos)


@app.route("/movie")
def movie():
    video_no = request.args.get('video_no')

    if video_no is None:
        return render_template('movie.html')

    videos = []
    for number in video_no.upper().split(','):
        video = metadata2.get_jav(number.strip())
        if video is not None:
            video = {'number': video.video_no, 'url': video.detail_url, 'fanart_url': video.fanart_url,
                     'movie_url': video.movie_url}
            videos.append(video)
    return render_template('movie.html', video_no=video_no, videos=videos)


@app.route("/fanza")
def fanza():
    actress = request.args.get('actress')
    series = request.args.get('series')

    if actress is not None and actress:
        videos = FANZA.search_actress(actress)
        print('查询完成')
        return render_template('fanza.html', actress=actress, videos=videos)
    elif series is not None and series:
        videos = FANZA.search_series(series)
        print('查询完成')
        return render_template('fanza.html', series=series, videos=videos)

    return render_template('fanza.html')


@app.route("/sod")
def sod():
    actress = request.args.get('actress')
    series = request.args.get('series')

    if actress is not None and actress:
        videos = SOD.search_actress(actress)
        print('查询完成')
        return render_template('sod.html', actress=actress, videos=videos)
    elif series is not None and series:
        videos = SOD.search_series(series)
        print('查询完成')
        return render_template('sod.html', series=series, videos=videos)

    return render_template('sod.html')


@app.route("/prestige")
def prestige():
    actress = request.args.get('actress')
    series = request.args.get('series')

    if actress is not None and actress:
        videos = Prestige.search_actress(actress)
        print('查询完成')
        return render_template('prestige.html', actress=actress, videos=videos)
    elif series is not None and series:
        videos = Prestige.search_series(series)
        print('查询完成')
        return render_template('prestige.html', series=series, videos=videos)

    return render_template('prestige.html')


@app.route("/mgstage")
def mgstage():
    actress = request.args.get('actress')
    series = request.args.get('series')

    if actress is not None and actress:
        videos = MGS.search_actress(actress)
        print('查询完成')
        return render_template('mgstage.html', actress=actress, videos=videos)
    elif series is not None and series:
        videos = MGS.search_series(series)
        print('查询完成')
        return render_template('mgstage.html', series=series, videos=videos)

    return render_template('mgstage.html')


@app.route("/magnet")
def magnet():
    video_no = request.args.get('video_no')
    return render_template('magnet.html', video_no=video_no, )


if __name__ == '__main__':
    app.run()

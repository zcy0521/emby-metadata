from flask import Flask, render_template, request

import metadata2
from jav.Fanza import Fanza
from jav.MGS import MGS
from jav.Prestige import Prestige


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

    items = []
    for number in video_no.upper().split(','):
        item = metadata2.get_jav(number.strip())
        if item is not None:
            items.append(item)
    return render_template('poster.html', video_no=video_no, items=items)


@app.route("/backdrop")
def fanart():
    video_no = request.args.get('video_no')

    if video_no is None:
        return render_template('backdrop.html')

    items = []
    for number in video_no.upper().split(','):
        item = metadata2.get_jav(number.strip())
        if item is not None:
            items.append(item)
    return render_template('backdrop.html', video_no=video_no, items=items)


@app.route("/trailer")
def movie():
    video_no = request.args.get('video_no')

    if video_no is None:
        return render_template('trailer.html')

    items = []
    for number in video_no.upper().split(','):
        item = metadata2.get_jav(number.strip())
        if item is not None:
            items.append(item)
    return render_template('trailer.html', video_no=video_no, items=items)


@app.route("/fanza")
def fanza():
    actress = request.args.get('actress')
    series = request.args.get('series')

    if actress is not None and actress:
        items = Fanza.search_actress(actress)
        print(f'{actress} 查询完成')
        return render_template('fanza.html', actress=actress, items=items)
    elif series is not None and series:
        items = Fanza.search_series(series)
        print(f'{series} 查询完成')
        return render_template('fanza.html', series=series, items=items)

    return render_template('fanza.html')


@app.route("/prestige")
def prestige():
    actress = request.args.get('actress')
    series = request.args.get('series')

    if actress is not None and actress:
        items = Prestige.search_actress(actress)
        print('查询完成')
        return render_template('prestige.html', actress=actress, items=items)
    elif series is not None and series:
        items = Prestige.search_series(series)
        print('查询完成')
        return render_template('prestige.html', series=series, items=items)

    return render_template('prestige.html')


@app.route("/mgs")
def mgs():
    actress = request.args.get('actress')
    series = request.args.get('series')

    if actress is not None and actress:
        items = MGS.search_actress(actress)
        print('查询完成')
        return render_template('mgs.html', actress=actress, items=items)
    elif series is not None and series:
        items = MGS.search_series(series)
        print('查询完成')
        return render_template('mgs.html', series=series, items=items)

    return render_template('mgs.html')


@app.route("/idope")
def magnet():
    video_no = request.args.get('video_no')

    if video_no is None:
        return render_template('idope.html')

    items = []
    return render_template('idope.html', video_no=video_no, items=items)


if __name__ == '__main__':
    app.run()

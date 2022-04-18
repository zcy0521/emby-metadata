#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from utils import http


class TameikeGoro(object):
    site_url = 'https://www.tameikegoro.jp/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }

    def __init__(self, video_no):
        self.video_no = video_no = video_no.lower().replace('-', '')

        # 详情页
        url = 'https://www.tameikegoro.jp/works/detail/' + video_no + '/'
        response = http.get(url, self.headers)
        html = response.text
        soup = BeautifulSoup(html, features="html.parser")

        # poster
        self.poster_url = soup.find(attrs={"property": "og:image"})['content']
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # fanart
        self.fanart_url = self.site_url.rstrip('/') + soup.find('div', id="wrap-detail-slider").find('img')['src']
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

    def download_poster(self):
        response = http.get(self.poster_url, self.headers)
        return response.content

    def download_fanart(self):
        response = http.get(self.fanart_url, self.headers)
        return response.content

    def get_poster_ext(self):
        return self.poster_ext

    def get_fanart_ext(self):
        return self.fanart_ext


if __name__ == '__main__':
    # https://www.tameikegoro.jp/works/detail/meyd532/
    tameike_goro = TameikeGoro('MEYD-532')

    print(tameike_goro.poster_url)
    print(tameike_goro.fanart_url)

    print(tameike_goro.poster_ext)
    print(tameike_goro.fanart_ext)

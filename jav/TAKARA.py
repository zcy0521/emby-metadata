#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from jav import FANZA
from utils import http_util

site_url = 'https://www.takara-tv.jp/'


class TAKARA(object):
    def __init__(self, video_no):
        # 番号
        self.video_no = video_no

        # 详情页
        self.detail_url = 'https://www.takara-tv.jp/dvd_detail.php?code={video_no}'.format(video_no=video_no)
        detail_html = http_util.get(self.detail_url)
        detail_soup = BeautifulSoup(detail_html, features="html.parser")

        # poster
        self.poster_url = site_url.rstrip('/') + detail_soup.find('div', id="area").find('img')['src'].lstrip('.')
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # fanart
        self.fanart_url = site_url.rstrip('/') + detail_soup.find('div', id="area").find('img')['src'].lstrip('.')
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

        # movie
        self.movie_url = FANZA.get_movie_url(video_no)
        self.movie_name = os.path.basename(self.movie_url)
        self.movie_ext = os.path.splitext(self.movie_name)[1]

    def get_video_no(self):
        return self.video_no

    def get_detail_url(self):
        return self.detail_url

    def get_poster_url(self):
        return self.poster_url

    def get_fanart_url(self):
        return self.fanart_url

    def get_movie_url(self):
        return self.movie_url

    def get_poster_ext(self):
        return self.poster_ext

    def get_fanart_ext(self):
        return self.fanart_ext

    def get_movie_ext(self):
        return self.movie_ext

    def download_poster(self):
        return http_util.download(self.poster_url)

    def download_fanart(self):
        return http_util.download(self.fanart_url)

    def download_movie(self):
        return http_util.download(self.movie_url)


if __name__ == '__main__':
    # https://www.takara-tv.jp/dvd_detail.php?code=CEMN-003
    takara = TAKARA('CEMN-003')

    print(takara.get_poster_url())
    print(takara.get_fanart_url())
    print(takara.get_movie_url())

    print(takara.get_poster_ext())
    print(takara.get_fanart_ext())
    print(takara.get_movie_ext())

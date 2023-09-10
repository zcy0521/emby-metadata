#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from jav import FANZA
from utils import http_util

site_url = 'https://befreebe.com/'


class AURORA(object):
    def __init__(self, video_no):
        # 番号
        self.video_no = video_no

        # 详情页
        detail_url = 'https://www.aurora-pro.com/shop/-/product/p/goods_id={video_no}/'.format(video_no=video_no)
        detail_html = http_util.get(detail_url)
        detail_soup = BeautifulSoup(detail_html, features="html.parser")

        # fanart
        self.fanart_url = detail_soup.find('img', id='main_pkg')['src']
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

        # poster
        self.poster_url = self.fanart_url.replace('open_xl', 'close_m')
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # movie
        self.movie_url = FANZA.get_movie_url(video_no)
        self.movie_name = os.path.basename(self.movie_url)
        self.movie_ext = os.path.splitext(self.movie_name)[1]

    def get_video_no(self):
        return self.video_no

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
    # https://www.aurora-pro.com/shop/-/product/p/goods_id=APAA-405/
    aurora = AURORA('APAA-405')

    print(aurora.get_poster_url())
    print(aurora.get_fanart_url())
    print(aurora.get_movie_url())

    print(aurora.get_poster_ext())
    print(aurora.get_fanart_ext())
    print(aurora.get_movie_ext())

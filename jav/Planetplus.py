#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from jav import FANZA
from utils import http_util

site_url = 'http://planetplus.jp/'


class Planetplus(object):
    def __init__(self, video_no):
        # 番号
        self.video_no = video_no

        # 搜索列表
        list_url = 'http://planetplus.jp/wp01/?s={video_no}'.format(video_no=video_no)
        list_html = http_util.get(list_url)
        list_soup = BeautifulSoup(list_html, features="html.parser")

        # poster
        self.poster_url = list_soup.find('article').find('img')['data-src']
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # 详情页
        url = list_soup.find('article').find('a')['href']
        html = http_util.get(url)
        soup = BeautifulSoup(html, features="html.parser")

        # fanart
        self.fanart_url = soup.find('div', class_="execphpwidget").find('a')['href']
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

        # movie
        self.movie_url = FANZA.get_movie_by_video_no(video_no)
        self.movie_name = os.path.basename(self.movie_url)
        self.movie_ext = os.path.splitext(self.movie_name)[1]

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
        return http.download(self.poster_url)

    def download_fanart(self):
        return http.download(self.fanart_url)

    def download_movie(self):
        return http.download(self.movie_url)


if __name__ == '__main__':
    # http://planetplus.jp/wp01/?s=NACR-387
    planetplus = Planetplus('NACR-387')

    print(planetplus.get_poster_url())
    print(planetplus.get_fanart_url())
    print(planetplus.get_movie_url())

    print(planetplus.get_poster_ext())
    print(planetplus.get_fanart_ext())
    print(planetplus.get_movie_ext())

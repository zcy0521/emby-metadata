#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from jav import FANZA
from utils import http_util

site_url = 'https://hakusuiriki.tv/'


class Hakusuiriki(object):
    def __init__(self, video_no):
        # 番号
        self.video_no = video_no

        # 详情页
        detail_url = 'https://hakusuiriki.tv/dl_detail.php?code={video_no}'.format(video_no=video_no)
        detail_html = http_util.get(detail_url)
        detail_soup = BeautifulSoup(detail_html, features="html.parser")

        # poster
        poster_url = detail_soup.find('div', id='newmovies').find('tr').find('th').find('img')['src']
        self.poster_url = site_url + poster_url.lstrip('./')
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # fanart
        fanart_url = detail_soup.find('div', id='newmovies').find('tr').find('th').find('a')['href']
        self.fanart_url = site_url + fanart_url.lstrip('./')
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

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
    # https://hakusuiriki.tv/dl_detail.php?code=CEAD-465
    hakusuiriki = Hakusuiriki('CEAD-465')

    print(hakusuiriki.get_poster_url())
    print(hakusuiriki.get_fanart_url())
    print(hakusuiriki.get_movie_url())

    print(hakusuiriki.get_poster_ext())
    print(hakusuiriki.get_fanart_ext())
    print(hakusuiriki.get_movie_ext())

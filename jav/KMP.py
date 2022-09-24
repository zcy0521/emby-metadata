#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from utils import http

# K.M.Produce
site_url = 'https://www.km-produce.com/'
post_url = 'https://www.km-produce.com/img/title0/{video_no}.jpg'

# 宇宙企画
uchu_site_url = 'http://uchu.co.jp/'


class KMP(object):
    def __init__(self, video_no):
        self.video_no = video_no = video_no.lower()

        # poster
        self.poster_url = post_url.format(video_no=video_no)
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # 详情页
        url = 'https://www.km-produce.com/works/' + video_no
        html = http.get(url)
        soup = BeautifulSoup(html, features="html.parser")

        # fanart
        self.fanart_url = site_url.rstrip('/') + soup.find('div', class_="details").find('a')['href']
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

        # TODO movie
        self.movie_url = ''
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
    # https://www.km-produce.com/works/mdtm-515
    kmp = KMP('MDTM-515')

    print(kmp.get_poster_url())
    print(kmp.get_fanart_url())
    print(kmp.get_movie_url())

    print(kmp.get_poster_ext())
    print(kmp.get_fanart_ext())
    print(kmp.get_movie_ext())

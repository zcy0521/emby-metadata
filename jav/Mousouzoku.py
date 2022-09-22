#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from utils import http

site_url = 'https://www.mousouzoku-av.com/'


class Mousouzoku(object):
    def __init__(self, video_no):
        self.video_no = video_no = video_no.lower().replace('-', '')

        # 详情页
        url = 'https://www.mousouzoku-av.com/works/detail/' + video_no + '/'
        html = http.get(url)
        soup = BeautifulSoup(html, features="html.parser")

        # poster
        poster_url = site_url.rstrip('/') + soup.find('div', class_="bx-side-content bx-side-content-buy").find('img')[
            'src']
        self.poster_url = poster_url.split('?')[0]
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # fanart
        fanart_url = site_url.rstrip('/') + soup.find('div', class_="bx-pake js-photo_swipe").find('img')['src']
        self.fanart_url = fanart_url.split('?')[0]
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

    def download_poster(self):
        return http.download(self.poster_url)

    def download_fanart(self):
        return http.download(self.fanart_url)

    def get_poster_ext(self):
        return self.poster_ext

    def get_fanart_ext(self):
        return self.fanart_ext


if __name__ == '__main__':
    # https://www.mousouzoku-av.com/works/detail/bijn195/
    mousouzoku = Mousouzoku('BIJN-195')

    print(mousouzoku.poster_url)
    print(mousouzoku.fanart_url)

    print(mousouzoku.poster_ext)
    print(mousouzoku.fanart_ext)

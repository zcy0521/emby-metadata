#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from utils import http


class Mousouzoku(object):
    site_url = 'https://www.mousouzoku-av.com/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }

    def __init__(self, video_no):
        self.video_no = video_no = video_no.lower().replace('-', '')

        # 详情页
        url = 'https://www.mousouzoku-av.com/works/detail/' + video_no + '/'
        response = http.get(url, self.headers)
        html = response.text
        soup = BeautifulSoup(html, features="html.parser")

        # poster
        self.poster_url = self.site_url.rstrip('/') + soup.find('div', class_="bx-side-content bx-side-content-buy").find('img')['src']
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # fanart
        self.fanart_url = self.site_url.rstrip('/') + soup.find('div', class_="bx-pake js-photo_swipe").find('img')['src']
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
    # https://www.mousouzoku-av.com/works/detail/bijn195/
    mousouzoku = Mousouzoku('BIJN-195')

    print(mousouzoku.poster_url)
    print(mousouzoku.fanart_url)

    print(mousouzoku.poster_ext)
    print(mousouzoku.fanart_ext)
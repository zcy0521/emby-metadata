#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from utils import http

site_url = 'https://www.prestige-av.com/'


class Prestige(object):
    def __init__(self, video_no):
        self.video_no = video_no = video_no.lower()

        # 年龄认证Cookie
        headers = {'cookie': '__age_auth__=true'}

        # 详情页
        url = 'https://www.prestige-av.com/goods/goods_detail.php?sku=' + video_no
        html = http.get(url, headers)
        soup = BeautifulSoup(html, features="html.parser")

        # poster
        poster_url = soup.find('div', class_="c-ratio-image").find('img')['src']
        self.poster_url = poster_url.split('?')[0]
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # fanart
        self.fanart_url = self.poster_url.replace('pf_', 'pb_')
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

        # movie
        movie_url = 'https://www.prestige-av.com/api/media/movie/{number}.mp4'
        self.movie_url = movie_url.format(number=video_no.upper())
        self.movie_name = os.path.basename(self.movie_url)
        self.movie_ext = os.path.splitext(self.movie_name)[1]

    def download_poster(self):
        response = http.get(self.poster_url)
        return response.content

    def download_fanart(self):
        response = http.get(self.fanart_url)
        return response.content

    def download_movie(self):
        response = http.get(self.movie_url)
        return response.content

    def get_poster_ext(self):
        return self.poster_ext

    def get_fanart_ext(self):
        return self.fanart_ext

    def get_movie_ext(self):
        return self.movie_ext


if __name__ == '__main__':
    # https://www.prestige-av.com/goods/goods_detail.php?sku=abp-721
    prestige = Prestige('ABP-721')

    print(prestige.poster_url)
    print(prestige.fanart_url)
    print(prestige.movie_url)

    print(prestige.poster_ext)
    print(prestige.fanart_ext)
    print(prestige.movie_ext)

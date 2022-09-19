#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from utils import http


class TMA(object):
    site_url = 'https://www.tma.co.jp/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }

    def __init__(self, video_no):
        # 详情页
        url = 'https://www.tma.co.jp/products/' + video_no.lower()
        response = http.get(url, self.headers)
        html = response.text
        soup = BeautifulSoup(html, features="html.parser")

        # poster
        poster_url = 'https:' + soup.find('a', class_="product-gallery__image product-gallery__image-1")['href']
        self.poster_url = poster_url.split('?')[0]
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # fanart
        fanart_url = 'https:' + soup.find('a', class_="product-gallery__image product-gallery__image-2")['href']
        self.fanart_url = fanart_url.split('?')[0]
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

        # movie
        self.movie_url = soup.find('div', class_="product-info").find('video')['src']
        self.movie_name = os.path.basename(self.movie_url)
        self.movie_ext = os.path.splitext(self.movie_name)[1]

    def download_poster(self):
        response = http.get(self.poster_url, self.headers)
        return response.content

    def download_fanart(self):
        response = http.get(self.fanart_url, self.headers)
        return response.content

    def download_movie(self):
        response = http.get(self.movie_url, self.headers)
        return response.content

    def get_poster_ext(self):
        return self.poster_ext

    def get_fanart_ext(self):
        return self.fanart_ext

    def get_movie_ext(self):
        return self.movie_ext


if __name__ == '__main__':
    # https://www.tma.co.jp/products/aoz-310z
    tma = TMA('AOZ-310z')

    print(tma.poster_url)
    print(tma.fanart_url)
    print(tma.movie_url)

    print(tma.poster_ext)
    print(tma.fanart_ext)
    print(tma.movie_ext)

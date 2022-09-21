#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from utils import http


class Shark(object):
    site_url = 'https://shark2012-av.com/'

    def __init__(self, video_no):
        # 详情页
        url = 'https://shark2012-av.com/products/index.php?pn=' + video_no
        html = http.get(url)
        soup = BeautifulSoup(html, features="html.parser")

        # poster
        self.poster_url = self.site_url + soup.find('div', class_="works-detail").find('img')['src']
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # fanart
        self.fanart_url = self.site_url + soup.find('div', class_="works-detail").find('a')['href']
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

    def download_poster(self):
        response = http.get(self.poster_url)
        return response.content

    def download_fanart(self):
        response = http.get(self.fanart_url)
        return response.content

    def get_poster_ext(self):
        return self.poster_ext

    def get_fanart_ext(self):
        return self.fanart_ext


if __name__ == '__main__':
    # https://shark2012-av.com/products/index.php?pn=MACB-006
    shark = Shark('MACB-006')

    print(shark.poster_url)
    print(shark.fanart_url)

    print(shark.poster_ext)
    print(shark.fanart_ext)

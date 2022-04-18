#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from utils import http


class SOD(object):
    site_url = 'https://ec.sod.co.jp/'

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }

    def __init__(self, video_no):
        self.video_no = video_no

        # 年龄检查
        http.get('https://ec.sod.co.jp/prime/_ontime.php', self.headers)

        # 详情页
        url = 'https://ec.sod.co.jp/prime/videos/?id=' + video_no
        response = http.get(url, self.headers)
        html = response.text
        soup = BeautifulSoup(html, features="html.parser")

        # poster
        self.poster_url = soup.find('img', class_="sam160")['src']
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # fanart
        self.fanart_url = soup.find('a', class_="popup-image")['href']
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
    # https://ec.sod.co.jp/prime/videos/?id=STARS-212
    sod = SOD('STARS-212')

    print(sod.poster_url)
    print(sod.fanart_url)

    print(sod.poster_ext)
    print(sod.fanart_ext)

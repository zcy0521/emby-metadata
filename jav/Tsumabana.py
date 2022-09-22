#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from utils import http

# 人妻花園劇場
site_url = 'http://www.tsumabana.com/'
post_url = 'http://www.tsumabana.com/images/portfolio/{video_no}.jpg'


class Tsumabana(object):
    def __init__(self, video_no):
        self.video_no = video_no = video_no.lower().replace('-', '')

        # poster
        self.poster_url = post_url.format(video_no=video_no)
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # 详情页
        url = 'http://www.tsumabana.com/' + video_no + '.php'
        html = http.get(url)
        soup = BeautifulSoup(html, features="html.parser")

        # fanart
        self.fanart_url = site_url + soup.find('article', class_="post").find('a')['href']
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
    # http://www.tsumabana.com/hzgd116.php
    tsumabana = Tsumabana('HZGD-116')

    print(tsumabana.poster_url)
    print(tsumabana.fanart_url)

    print(tsumabana.poster_ext)
    print(tsumabana.fanart_ext)

#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

import requests
from bs4 import BeautifulSoup

from utils import http


class KMP(object):
    # K.M.Produce
    site_url = 'https://www.km-produce.com/'
    post_url = 'https://www.km-produce.com/img/title0/{video_no}.jpg'

    # 宇宙企画
    uchu_site_url = 'http://uchu.co.jp/'

    def __init__(self, video_no):
        self.video_no = video_no = video_no.lower()
        self.session = session = requests.Session()
        self.headers = headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

        # 详情页
        url = 'https://www.km-produce.com/works/' + video_no
        # response = session.get(url, headers=headers)
        response = http.proxy_get(session, url, headers)
        html = response.text
        soup = BeautifulSoup(html, features="html.parser")

        # poster
        self.poster_url = self.post_url.format(video_no=video_no)
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # fanart
        self.fanart_url = self.site_url.rstrip('/') + soup.find('div', class_="details").find('a')['href']
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

    def download_poster(self):
        # response = self.session.get(self.poster_url, headers=self.headers)
        response = http.proxy_get(self.session, self.poster_url, self.headers)
        return response.content

    def download_fanart(self):
        # response = self.session.get(self.fanart_url, headers=self.headers)
        response = http.proxy_get(self.session, self.fanart_url, self.headers)
        return response.content

    def get_poster_ext(self):
        return self.poster_ext

    def get_fanart_ext(self):
        return self.fanart_ext


if __name__ == '__main__':
    # https://www.km-produce.com/works/mdtm-515
    kmp = KMP('MDTM-515')

    print(kmp.poster_url)
    print(kmp.fanart_url)

    print(kmp.poster_ext)
    print(kmp.fanart_ext)

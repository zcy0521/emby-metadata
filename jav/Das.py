#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

import requests
from bs4 import BeautifulSoup


class Das(object):
    site_url = 'https://www.dasdas.jp/'

    def __init__(self, video_no):
        self.video_no = video_no = video_no.lower().replace('-', '')
        self.session = session = requests.Session()
        self.headers = headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

        # 详情页
        url = 'https://www.dasdas.jp/works/detail/' + video_no + '/'
        response = session.get(url, headers=headers)
        html = response.text
        soup = BeautifulSoup(html, features="html.parser")

        # poster
        self.poster_url = soup.find(attrs={"property": "og:image"})['content']
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # fanart
        self.fanart_url = self.site_url.rstrip('/') + soup.find('div', class_="wrap-package-image js-photo-swipe-target").find('img')['src']
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

    def download_poster(self):
        response = self.session.get(self.poster_url, headers=self.headers)
        return response.content

    def download_fanart(self):
        response = self.session.get(self.fanart_url, headers=self.headers)
        return response.content

    def get_poster_ext(self):
        return self.poster_ext

    def get_fanart_ext(self):
        return self.fanart_ext


if __name__ == '__main__':
    # https://www.dasdas.jp/works/detail/dasd542/
    das = Das('DASD-542')

    print(das.poster_url)
    print(das.fanart_url)

    print(das.poster_ext)
    print(das.fanart_ext)

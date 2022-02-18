#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

import requests
from bs4 import BeautifulSoup

from utils import http


class Prestige(object):
    site_url = 'https://www.prestige-av.com/'

    def __init__(self, video_no):
        self.video_no = video_no = video_no.lower()
        self.session = session = requests.Session()
        self.headers = headers = {
            'cookie': 'coc=1; age_auth=1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

        # 详情页
        url = 'https://www.prestige-av.com/goods/goods_detail.php?sku=' + video_no
        # response = session.get(url, headers=headers)
        response = http.proxy_get(session, url, headers)
        html = response.text
        soup = BeautifulSoup(html, features="html.parser")

        # poster
        self.poster_url = self.site_url.rstrip('/') + soup.find('p', class_="package_layout").find('img', class_='border_image')['src']
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # fanart
        self.fanart_url = self.site_url.rstrip('/') + soup.find('p', class_="package_layout").find('a', class_='sample_image')['href']
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
    # https://www.prestige-av.com/goods/goods_detail.php?sku=abp-721
    prestige = Prestige('ABP-721')

    print(prestige.poster_url)
    print(prestige.fanart_url)

    print(prestige.poster_ext)
    print(prestige.fanart_ext)

#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

import requests
from bs4 import BeautifulSoup

from utils import http


class HHH(object):
    site_url = 'https://www.hhh-av.com/'

    def __init__(self, video_no):
        self.video_no = video_no = video_no.lower().replace('-', '')
        self.session = session = requests.Session()
        self.headers = headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

        # 搜索列表
        list_url= 'https://www.hhh-av.com/search/list/?q=' + video_no
        # list_response = session.get(list_url, headers=headers)
        list_response = http.proxy_get(session, list_url, headers)
        list_html = list_response.text
        list_soup = BeautifulSoup(list_html, features="html.parser")

        # poster
        self.poster_url = self.site_url.rstrip('/') + list_soup.find('ul', class_="lst-works").find('img')['src']
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # 详情页
        url = self.site_url.rstrip('/') + list_soup.find('ul', class_="lst-works").find('a')['href']
        # response = session.get(url, headers=headers)
        response = http.proxy_get(session, url, headers)
        html = response.text
        soup = BeautifulSoup(html, features="html.parser")

        # fanart
        self.fanart_url = self.site_url.rstrip('/') + soup.find('div', class_="area-sample").find('img')['src']
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
    hhh = HHH('OYC-278')

    print(hhh.poster_url)
    print(hhh.fanart_url)

    print(hhh.poster_ext)
    print(hhh.fanart_ext)

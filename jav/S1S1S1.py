#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

import requests
from bs4 import BeautifulSoup

from utils import http


class S1S1S1(object):
    site_url = 'https://www.s1s1s1.com/'

    def __init__(self, video_no):
        self.video_no = video_no = video_no.lower().replace('-', '')
        self.session = session = requests.Session()
        self.headers = headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

        # 搜索列表
        list_url = 'https://s1s1s1.com/search/list?keyword=' + video_no
        # list_response = session.get(list_url, headers=headers)
        list_response = http.proxy_get(session, list_url, headers)
        list_html = list_response.text
        list_soup = BeautifulSoup(list_html, features="html.parser")
        # print(list_soup)

        # poster
        self.poster_url = list_soup.find('div', class_="c-card").find('img')['data-src']
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # 详情页
        url = 'https://www.s1s1s1.com/works/detail/' + video_no + '/'
        # response = session.get(url, headers=headers)
        response = http.proxy_get(session, url, headers)
        html = response.text
        soup = BeautifulSoup(html, features="html.parser")
        # print(info_soup)

        # fanart
        self.fanart_url = soup.find('div', class_="swiper-wrapper").find('img')['data-src']
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
    # https://www.s1s1s1.com/works/detail/ssni939/
    s1s1s1 = S1S1S1('SSNI-939')

    print(s1s1s1.poster_url)
    print(s1s1s1.fanart_url)

    print(s1s1s1.poster_ext)
    print(s1s1s1.fanart_ext)

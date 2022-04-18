#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from utils import http


class Das(object):
    site_url = 'https://www.dasdas.jp/'

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }

    def __init__(self, video_no):
        self.video_no = video_no = video_no.lower().replace('-', '')

        # 搜索列表
        list_url = 'https://www.dasdas.jp/search/list/?q=' + video_no
        list_response = http.get(list_url, self.headers)
        list_html = list_response.text
        list_soup = BeautifulSoup(list_html, features="html.parser")

        # poster
        self.poster_url = self.site_url.rstrip('/') + list_soup.find('div', class_="wrap-works-list-item--work").find('img')['src']
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # 详情页
        url = self.site_url.rstrip('/') + list_soup.find('div', class_="wrap-works-list-item-info--work").find('a')['href']
        response = http.get(url, self.headers)
        html = response.text
        soup = BeautifulSoup(html, features="html.parser")

        # fanart
        self.fanart_url = self.site_url.rstrip('/') + soup.find('div', class_="wrap-package-image js-photo-swipe-target").find('img')['src']
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
    # https://www.dasdas.jp/works/detail/dasd542/
    das = Das('DASD-542')

    print(das.poster_url)
    print(das.fanart_url)

    print(das.poster_ext)
    print(das.fanart_ext)

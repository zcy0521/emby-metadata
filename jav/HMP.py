#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from utils import http

site_url = 'https://smt.hmp.jp/'


class HMP(object):
    def __init__(self, video_no):
        self.video_no = video_no

        # 搜索列表
        list_url = 'https://smt.hmp.jp/list.php'
        list_html = http.post(list_url, {'key': video_no})
        list_soup = BeautifulSoup(list_html, features="html.parser")

        # poster
        self.poster_url = site_url.rstrip('/') + list_soup.find('p', class_="mainImg").find('img')['data-original']
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # 详情页
        url = site_url.rstrip('/') + list_soup.find('p', class_="mainImg").find('a')['href']
        html = http.get(url)
        soup = BeautifulSoup(html, features="html.parser")

        # fanart
        self.fanart_url = site_url.rstrip('/') + soup.find('p', class_="mainImg").find('img')['src']
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
    hmp = HMP('HODV-21402')

    print(hmp.poster_url)
    print(hmp.fanart_url)

    print(hmp.poster_ext)
    print(hmp.fanart_ext)

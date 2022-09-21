#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from utils import http


class HHH(object):
    site_url = 'https://www.hhh-av.com/'

    def __init__(self, video_no):
        self.video_no = video_no = video_no.lower().replace('-', '')

        # 搜索列表
        list_url= 'https://www.hhh-av.com/search/list/?q=' + video_no
        list_html = http.get(list_url)
        list_soup = BeautifulSoup(list_html, features="html.parser")

        # poster
        self.poster_url = self.site_url.rstrip('/') + list_soup.find('ul', class_="lst-works").find('img')['src']
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # 详情页
        url = self.site_url.rstrip('/') + list_soup.find('ul', class_="lst-works").find('a')['href']
        html = http.get(url)
        soup = BeautifulSoup(html, features="html.parser")

        # fanart
        self.fanart_url = self.site_url.rstrip('/') + soup.find('div', class_="area-sample").find('img')['src']
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
    hhh = HHH('OYC-278')

    print(hhh.poster_url)
    print(hhh.fanart_url)

    print(hhh.poster_ext)
    print(hhh.fanart_ext)

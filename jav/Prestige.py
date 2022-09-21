#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from utils import http


class Prestige(object):
    site_url = 'https://www.prestige-av.com/'

    def __init__(self, video_no):
        self.video_no = video_no = video_no.lower()

        # 详情页
        url = 'https://www.prestige-av.com/goods/goods_detail.php?sku=' + video_no
        html = http.get(url)
        # TODO 年龄认证
        print(html)
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
    # https://www.prestige-av.com/goods/goods_detail.php?sku=abp-721
    prestige = Prestige('ABP-721')

    print(prestige.poster_url)
    print(prestige.fanart_url)

    print(prestige.poster_ext)
    print(prestige.fanart_ext)

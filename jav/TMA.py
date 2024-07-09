#!/usr/bin/envpython3
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup

from utils import http_util


class TMA(object):
    # 官网
    SITE_URL = 'https://www.tma.co.jp/'
    DETAIL_URL = 'https://www.tma.co.jp/products/{video_no}'

    def __init__(self, video_no):
        self.video_no = video_no

        # 详情页
        detail_url = TMA.DETAIL_URL.format(video_no=video_no.lower())
        detail_html = http_util.get(detail_url)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        poster_url = self.detail_soup.find('a', class_="product-gallery__image product-gallery__image-1")['href']
        return 'https:' + poster_url.split('?')[0]

    def get_backdrop_url(self):
        backdrop_url = self.detail_soup.find('a', class_="product-gallery__image product-gallery__image-2")['href']
        return 'https:' + backdrop_url.split('?')[0]

    def get_trailer_url(self):
        return self.detail_soup.find('div', class_="product-info").find('video')['src']


if __name__ == '__main__':
    # https://www.tma.co.jp/products/aoz-310z
    tma = TMA('AOZ-310z')
    print(tma.get_poster_url())
    print(tma.get_backdrop_url())
    print(tma.get_trailer_url())

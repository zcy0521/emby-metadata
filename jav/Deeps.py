#!/usr/bin/envpython3
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup

from jav.Fanza import Fanza
from utils import http_util


class Deeps(object):
    # 官网
    SITE_URL = 'https://deeps.net/'
    DETAIL_URL = 'https://deeps.net/product/{video_no}/'

    def __init__(self, video_no):
        self.video_no = video_no

        # 详情页
        detail_url = Deeps.DETAIL_URL.format(video_no=video_no.lower())
        detail_html = http_util.get(detail_url)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        return self.detail_soup.find('div', id='item').find('figure').find_all('img', class_='sp')[0]['src']

    def get_backdrop_url(self):
        return self.detail_soup.find('div', id='item').find('figure').find('img', class_='pc')['src']

    def get_trailer_url(self):
        fanza = Fanza(self.video_no)
        return fanza.get_trailer_url()


if __name__ == '__main__':
    # https://deeps.net/product/dvrt-024/
    deeps = Deeps('DVRT-024')
    print(deeps.get_poster_url())
    print(deeps.get_backdrop_url())
    print(deeps.get_trailer_url())

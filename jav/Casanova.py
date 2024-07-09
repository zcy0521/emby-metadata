#!/usr/bin/envpython3
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup

from jav.Fanza import Fanza
from utils import http_util


class Casanova(object):
    # 官网
    SITE_URL = 'http://casanova-vr.com/'
    DETAIL_URL = 'http://casanova-vr.com/items/detail/{video_no}'

    def __init__(self, video_no):
        self.video_no = video_no

        # 详情页
        detail_url = Casanova.DETAIL_URL.format(video_no=video_no)
        detail_html = http_util.get(detail_url)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        poster_url = self.detail_soup.find('div', class_="img").find('img')['src']
        return poster_url.lstrip('.')

    def get_backdrop_url(self):
        backdrop_url = self.detail_soup.find('div', class_="img").find('img')['src']
        return backdrop_url.lstrip('.')

    def get_trailer_url(self):
        fanza = Fanza(self.video_no)
        return fanza.get_trailer_url()


if __name__ == '__main__':
    # http://casanova-vr.com/items/detail/CAFR-001
    casanova = Casanova('CAFR-001')
    print(casanova.get_poster_url())
    print(casanova.get_backdrop_url())
    print(casanova.get_trailer_url())

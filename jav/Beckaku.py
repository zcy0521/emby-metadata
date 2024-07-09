#!/usr/bin/envpython3
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup

from jav.Fanza import Fanza
from utils import http_util


class Beckaku(object):
    # 官网
    SITE_URL = 'http://beckaku.com'
    DETAIL_URL = 'http://beckaku.com/detail.html?item={video_no}'

    def __init__(self, video_no):
        self.video_no = video_no

        # 详情页
        detail_url = 'http://beckaku.com/detail.html?item={video_no}'.format(video_no=video_no)
        detail_html = http_util.get(detail_url, {'cookie': 'check=true'})
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        poster_url = self.detail_soup.find('div', id="item-info02").find('img')['src']
        return Beckaku.SITE_URL + poster_url.lstrip('.')

    def get_backdrop_url(self):
        backdrop_url = self.detail_soup.find('div', id="item-info02").find('a')['href']
        return Beckaku.SITE_URL + backdrop_url.lstrip('.')

    def get_trailer_url(self):
        fanza = Fanza(self.video_no)
        return fanza.get_trailer_url()


if __name__ == '__main__':
    # http://beckaku.com/detail.html?item=BKKG-019
    backau = Beckaku('BKKG-019')
    print(backau.get_poster_url())
    print(backau.get_backdrop_url())
    print(backau.get_trailer_url())

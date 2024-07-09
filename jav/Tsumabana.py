#!/usr/bin/envpython3
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup

from jav.Fanza import Fanza
from utils import http_util


class Tsumabana(object):
    # 人妻花園劇場 官网
    SITE_URL = 'http://www.tsumabana.com/'
    DETAIL_URL = 'http://www.tsumabana.com/{video_no}.php'
    POSTER_URL = 'http://www.tsumabana.com/images/portfolio/{video_no}.jpg'

    def __init__(self, video_no):
        self.video_no = video_no

        # 详情页
        detail_url = Tsumabana.DETAIL_URL.format(video_no=video_no.lower().replace('-', ''))
        detail_html = http_util.get(detail_url)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        return Tsumabana.POSTER_URL.format(video_no=self.video_no.lower().replace('-', ''))

    def get_backdrop_url(self):
        backdrop_url = self.detail_soup.find('article', class_="post").find('a')['href']
        return Tsumabana.SITE_URL + backdrop_url

    def get_trailer_url(self):
        fanza = Fanza(self.video_no)
        return fanza.get_trailer_url()


if __name__ == '__main__':
    # http://www.tsumabana.com/hzgd116.php
    tsumabana = Tsumabana('HZGD-116')
    print(tsumabana.get_poster_url())
    print(tsumabana.get_backdrop_url())
    print(tsumabana.get_trailer_url())

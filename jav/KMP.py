#!/usr/bin/envpython3
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup

from jav.Fanza import Fanza
from utils import http_util


class KMP(object):
    # K.M.Produce
    SITE_URL = 'https://www.km-produce.com'
    DETAIL_URL = 'https://www.km-produce.com/works/{video_no}'
    POSTER_URL = 'https://www.km-produce.com/img/title0/{video_no}.jpg'

    # 宇宙企画
    UCHU_SITE_URL = 'http://uchu.co.jp/'

    def __init__(self, video_no):
        self.video_no = video_no

        # 详情页
        detail_url = KMP.DETAIL_URL.format(video_no=video_no.lower())
        detail_html = http_util.get(detail_url)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        return KMP.POSTER_URL.format(video_no=self.video_no.lower())

    def get_backdrop_url(self):
        backdrop_url = self.detail_soup.find('div', class_="details").find('a')['href']
        return KMP.SITE_URL + backdrop_url

    def get_trailer_url(self):
        fanza = Fanza(self.video_no)
        return fanza.get_trailer_url()


if __name__ == '__main__':
    # https://www.km-produce.com/works/mdtm-515
    kmp = KMP('REAL-820')
    print(kmp.get_poster_url())
    print(kmp.get_backdrop_url())
    print(kmp.get_trailer_url())

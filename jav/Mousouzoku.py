#!/usr/bin/envpython3
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup

from jav.Fanza import Fanza
from utils import http_util


class Mousouzoku(object):
    # AVS collector’s 官网
    SITE_URL = 'https://www.mousouzoku-av.com'
    DETAIL_URL = 'https://www.mousouzoku-av.com/works/detail/{video_no}/'

    def __init__(self, video_no):
        self.video_no = video_no

        # 详情页
        detail_url = Mousouzoku.DETAIL_URL.format(video_no=video_no.lower().replace('-', ''))
        detail_html = http_util.get(detail_url)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        poster_url = self.detail_soup.find('div', class_="bx-side-content bx-side-content-buy").find('img')['src']
        poster_url = Mousouzoku.SITE_URL + poster_url
        return poster_url.split('?')[0]

    def get_backdrop_url(self):
        backdrop_url = self.detail_soup.find('div', class_="bx-pake js-photo_swipe").find('img')['src']
        backdrop_url = Mousouzoku.SITE_URL + backdrop_url
        return backdrop_url.split('?')[0]

    def get_trailer_url(self):
        fanza = Fanza(self.video_no)
        return fanza.get_trailer_url()


if __name__ == '__main__':
    # https://www.mousouzoku-av.com/works/detail/bijn195/
    mousouzoku = Mousouzoku('BIJN-195')
    print(mousouzoku.get_poster_url())
    print(mousouzoku.get_backdrop_url())
    print(mousouzoku.get_trailer_url())

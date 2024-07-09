#!/usr/bin/envpython3
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup

from jav.Fanza import Fanza
from utils import http_util


class TAKARA(object):
    # 官网
    SITE_URL = 'https://www.takara-tv.jp'
    DETAIL_URL = 'https://www.takara-tv.jp/dvd_detail.php?code={video_no}'

    def __init__(self, video_no):
        self.video_no = video_no

        # 详情页
        detail_url = TAKARA.DETAIL_URL.format(video_no=video_no)
        detail_html = http_util.get(detail_url)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")
        print(self.detail_soup)

    def get_poster_url(self):
        poster_url = self.detail_soup.find('div', id="area").find('img')['src']
        return TAKARA.SITE_URL + poster_url.lstrip('.')

    def get_backdrop_url(self):
        backdrop_url = self.detail_soup.find('div', id="area").find('a')['href']
        return TAKARA.SITE_URL + backdrop_url.lstrip('.')

    def get_trailer_url(self):
        fanza = Fanza(self.video_no)
        return fanza.get_trailer_url()


if __name__ == '__main__':
    # https://www.takara-tv.jp/dvd_detail.php?code=CEMN-003
    takara = TAKARA('CEMN-003')
    print(takara.get_poster_url())
    print(takara.get_backdrop_url())
    print(takara.get_trailer_url())

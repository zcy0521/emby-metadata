#!/usr/bin/envpython3
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup

from jav.Fanza import Fanza
from utils import http_util


class PlanetPlus(object):
    # 官网
    SITE_URL = 'https://planetplus.jp/'
    SEARCH_URL = 'https://planetplus.jp/wp01/?s={video_no}'

    def __init__(self, video_no):
        self.video_no = video_no

        # 搜索列表
        list_url = PlanetPlus.SEARCH_URL.format(video_no=video_no)
        list_html = http_util.get(list_url)
        self.list_soup = BeautifulSoup(list_html, features="html.parser")

        # 详情页
        detail_url = self.list_soup.find('article').find('a')['href']
        detail_html = http_util.get(detail_url)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        return self.list_soup.find('article').find('img')['data-src']

    def get_backdrop_url(self):
        return self.detail_soup.find('div', class_="execphpwidget").find('a')['href']

    def get_trailer_url(self):
        fanza = Fanza(self.video_no)
        return fanza.get_trailer_url()


if __name__ == '__main__':
    # https://planetplus.jp/wp01/?s=NACR-348
    # https://planetplus.jp/wp01/?s=NACR-356
    # https://planetplus.jp/wp01/?s=NACR-501
    # https://planetplus.jp/wp01/?s=NACR-558
    planetPlus = PlanetPlus('NACR-501')
    print(planetPlus.get_poster_url())
    print(planetPlus.get_backdrop_url())
    print(planetPlus.get_trailer_url())

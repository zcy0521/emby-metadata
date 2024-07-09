#!/usr/bin/envpython3
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup

from utils import http_util


class NaturalHigh(object):
    # 官网
    SITE_URL = 'https://www.naturalhigh.co.jp/'
    DETAIL_URL = 'https://www.naturalhigh.co.jp/all/{video_no}/'

    def __init__(self, video_no):
        # 番号
        self.video_no = video_no

        # 视频详情页html
        detail_url = NaturalHigh.DETAIL_URL.format(video_no=video_no.lower())
        detail_html = http_util.get(detail_url)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        return self.detail_soup.find('div', class_="single_main_image").find('img')['data-lazy-src']

    def get_backdrop_url(self):
        return self.detail_soup.find('div', class_="single_main_image").find('a')['href']

    def get_trailer_url(self):
        return self.detail_soup.find('div', class_="sample_movie").find('div', class_='movie_area').find('video')['src']


if __name__ == '__main__':
    # https://www.naturalhigh.co.jp/all/shn-016/
    natural_high = NaturalHigh('SHN-016')
    print(natural_high.get_poster_url())
    print(natural_high.get_backdrop_url())
    print(natural_high.get_trailer_url())

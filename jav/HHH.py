#!/usr/bin/envpython3
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup

from utils import http_util


class HHH(object):
    # 官网
    SITE_URL = 'https://www.hhh-av.com/'
    SEARCH_URL = 'https://www.hhh-av.com/search/list?keyword={video_no}'

    def __init__(self, video_no):
        self.video_no = video_no

        # 搜索列表
        list_url = HHH.SEARCH_URL.format(video_no=video_no.replace('-', ''))
        list_html = http_util.get(list_url)
        self.list_soup = BeautifulSoup(list_html, features="html.parser")

        # 详情页
        detail_url = self.list_soup.find('div', class_='c-card').find('a')['href']
        detail_html = http_util.get(detail_url)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        return self.list_soup.find('div', class_='c-card').find('img')['data-src']

    def get_backdrop_url(self):
        return self.detail_soup.find('div', class_='swiper-wrapper').find('img')['data-src']

    def get_trailer_url(self):
        return self.detail_soup.find('div', class_='video').find('video')['src']


if __name__ == '__main__':
    # https://www.hhh-av.com/search/list?keyword=HUNTA661
    hhh = HHH('HUNTA-661')
    print(hhh.get_poster_url())
    print(hhh.get_backdrop_url())
    print(hhh.get_trailer_url())

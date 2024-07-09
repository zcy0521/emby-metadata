#!/usr/bin/envpython3
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup

from utils import http_util


class Attackers(object):
    # 官网
    SITE_URL = 'https://www.attackers.net/'
    SEARCH_URL = 'https://attackers.net/search/list?keyword={video_no}'

    def __init__(self, video_no):
        self.video_no = video_no

        # 搜索列表
        list_url = Attackers.SEARCH_URL.format(video_no=video_no.lower().replace('-', ''))
        list_html = http_util.get(list_url)
        self.list_soup = BeautifulSoup(list_html, features="html.parser")

        # 详情页
        detail_url = self.list_soup.find('div', class_="swiper-wrapper").find('div', class_="item").find('a')['href']
        detail_html = http_util.get(detail_url)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        return self.list_soup.find('div', class_="swiper-wrapper").find('div', class_="item").find('img')['data-src']

    def get_backdrop_url(self):
        return self.detail_soup.find('div', class_="swiper-slide").find('img')['data-src']

    def get_trailer_url(self):
        return self.detail_soup.find('div', class_="video").find('video')['src']


if __name__ == '__main__':
    # https://www.attackers.net/works/detail/atid318/
    attackers = Attackers('ATID-318')
    print(attackers.get_poster_url())
    print(attackers.get_backdrop_url())
    print(attackers.get_trailer_url())

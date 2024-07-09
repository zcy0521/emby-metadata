#!/usr/bin/envpython3
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup

from utils import http_util


class TameikeGoro(object):
    # 溜池ゴロー 官网
    SITE_URL = 'https://www.tameikegoro.jp/'
    SEARCH_URL = 'https://tameikegoro.jp/search/list?keyword={video_no}'

    def __init__(self, video_no):
        self.video_no = video_no

        # 搜索列表
        list_url = TameikeGoro.SEARCH_URL.format(video_no=video_no.replace('-', ''))
        list_html = http_util.get(list_url)
        self.list_soup = BeautifulSoup(list_html, features="html.parser")

        # 详情页
        detail_url = self.list_soup.find('div', class_='swiper-wrapper').find_all('div', class_='item')[0].find('a')['href']
        detail_html = http_util.get(detail_url)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        return self.list_soup.find('div', class_='swiper-wrapper').find_all('div', class_='item')[0].find('img')['data-src']

    def get_backdrop_url(self):
        fanart_img = self.detail_soup.find_all('div', class_='swiper-slide')[0].find('img')
        if fanart_img.has_attr('src'):
            return fanart_img['src']
        else:
            return fanart_img['data-src']

    def get_trailer_url(self):
        return self.detail_soup.find('div', class_="video").find('video')['src']


if __name__ == '__main__':
    # 详情页一张图片
    # https://tameikegoro.jp/search/list?keyword=MBYD380
    mbyd380 = TameikeGoro('MBYD-380')
    print(mbyd380.get_poster_url())
    print(mbyd380.get_backdrop_url())
    print(mbyd380.get_trailer_url())

    # 详情页多张图片
    # https://tameikegoro.jp/search/list?keyword=PFES047
    pfes047 = TameikeGoro('PFES-047')
    print(pfes047.get_poster_url())
    print(pfes047.get_backdrop_url())
    print(pfes047.get_trailer_url())

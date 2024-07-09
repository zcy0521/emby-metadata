#!/usr/bin/envpython3
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup

from jav.Fanza import Fanza
from utils import http_util


class OPPAI(object):
    # 官网
    SITE_URL = 'https://oppai-av.com/'
    SEARCH_URL = 'https://oppai-av.com/search/list?keyword={video_no}'

    def __init__(self, video_no):
        self.video_no = video_no

        # 搜索列表
        list_url = OPPAI.SEARCH_URL.format(video_no=video_no.replace('-', ''))
        list_html = http_util.get(list_url)
        self.list_soup = BeautifulSoup(list_html, features="html.parser")

        # 详情页
        detail_url = self.list_soup.find('div', class_='swiper-wrapper').find_all('div', class_='item')[0].find('a')['href']
        detail_html = http_util.get(detail_url)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        return self.list_soup.find('div', class_='swiper-wrapper').find_all('div', class_='item')[0].find('img')['data-src']

    def get_backdrop_url(self):
        return self.detail_soup.find('div', class_='swiper-wrapper').find_all('div', class_='swiper-slide')[0].find('img')['data-src']

    def get_trailer_url(self):
        fanza = Fanza(self.video_no)
        return fanza.get_trailer_url()


if __name__ == '__main__':
    # https://oppai-av.com/search/list?keyword=PPPE062
    oppai = OPPAI('PPPE-062')
    print(oppai.get_poster_url())
    print(oppai.get_backdrop_url())
    print(oppai.get_trailer_url())

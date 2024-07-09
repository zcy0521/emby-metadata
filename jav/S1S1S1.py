#!/usr/bin/envpython3
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup

from jav.Fanza import Fanza
from utils import http_util


class S1S1S1(object):
    # 官网
    SITE_URL = 'https://s1s1s1.com/'
    SEARCH_URL = 'https://s1s1s1.com/search/list?keyword={video_no}'

    def __init__(self, video_no):
        self.video_no = video_no

        # 搜索列表
        list_url = S1S1S1.SEARCH_URL.format(video_no=video_no.lower().replace('-', ''))
        list_html = http_util.get(list_url)
        self.list_soup = BeautifulSoup(list_html, features="html.parser")

        # 详情页
        detail_url = self.list_soup.find('div', class_="swiper-wrapper").find('a')['href']
        detail_html = http_util.get(detail_url)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        return self.list_soup.find('div', class_="swiper-wrapper").find('img')['data-src']

    def get_backdrop_url(self):
        return self.detail_soup.find('div', class_="swiper-wrapper").find('img')['data-src']

    def get_trailer_url(self):
        if self.detail_soup.find('div', class_="video"):
            return self.detail_soup.find('div', class_="video").find('video')['src']
        else:
            fanza = Fanza(self.video_no)
            return fanza.get_trailer_url()


if __name__ == '__main__':
    # https://s1s1s1.com/works/detail/ssni939/
    # SSNI-939 web上有video标签
    # SSNI-547 web上没有video标签
    s1s1s1 = S1S1S1('SSNI-547')
    print(s1s1s1.get_poster_url())
    print(s1s1s1.get_backdrop_url())
    print(s1s1s1.get_trailer_url())

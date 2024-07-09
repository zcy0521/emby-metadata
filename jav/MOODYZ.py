#!/usr/bin/envpython3
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup

from utils import http_util


class MOODYZ(object):
    # 官网
    SITE_URL = 'https://moodyz.com/'
    SEARCH_URL = 'https://moodyz.com/search/list?keyword={video_no}'

    def __init__(self, video_no):
        self.video_no = video_no

        # 搜索列表
        list_url = MOODYZ.SEARCH_URL.format(video_no=video_no.replace('-', ''))
        list_html = http_util.get(list_url)
        self.list_soup = BeautifulSoup(list_html, features="html.parser")

        # 详情页
        detail_url = self.list_soup.find('div', class_="swiper-wrapper").find('a')['href']
        detail_html = http_util.get(detail_url)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        return self.list_soup.find('div', class_="swiper-wrapper").find('img')['data-src']

    def get_backdrop_url(self):
        return self.detail_soup.find('div', class_="swiper-slide").find('img')['data-src']

    def get_trailer_url(self):
        return self.detail_soup.find('div', class_="video").find('video')['src']


if __name__ == '__main__':
    # https://moodyz.com/works/detail/MIDE936
    moodyz = MOODYZ('MIDE-936')
    print(moodyz.get_poster_url())
    print(moodyz.get_backdrop_url())
    print(moodyz.get_trailer_url())

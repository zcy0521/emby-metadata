#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from utils import http_util

site_url = 'https://s1s1s1.com/'


class S1S1S1(object):
    def __init__(self, video_no):
        # 番号
        self.video_no = video_no

        # 搜索列表
        list_url = 'https://s1s1s1.com/search/list?keyword={video_no}'.format(
            video_no=video_no.lower().replace('-', ''))
        list_html = http_util.get(list_url)
        list_soup = BeautifulSoup(list_html, features="html.parser")

        # poster
        self.poster_url = list_soup.find('div', class_="swiper-wrapper").find('img')['data-src']
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # 详情页
        self.detail_url = list_soup.find('div', class_="swiper-wrapper").find('a')['href']
        detail_html = http_util.get(self.detail_url)
        detail_soup = BeautifulSoup(detail_html, features="html.parser")

        # fanart
        self.fanart_url = detail_soup.find('div', class_="swiper-wrapper").find('img')['data-src']
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

        # movie
        self.movie_url = detail_soup.find('div', class_="video").find('video')['src']
        self.movie_name = os.path.basename(self.movie_url)
        self.movie_ext = os.path.splitext(self.movie_name)[1]

    def get_video_no(self):
        return self.video_no

    def get_detail_url(self):
        return self.detail_url

    def get_poster_url(self):
        return self.poster_url

    def get_fanart_url(self):
        return self.fanart_url

    def get_movie_url(self):
        return self.movie_url

    def get_poster_ext(self):
        return self.poster_ext

    def get_fanart_ext(self):
        return self.fanart_ext

    def get_movie_ext(self):
        return self.movie_ext

    def download_poster(self):
        return http_util.download(self.poster_url)

    def download_fanart(self):
        return http_util.download(self.fanart_url)

    def download_movie(self):
        return http_util.download(self.movie_url)


if __name__ == '__main__':
    # https://s1s1s1.com/works/detail/ssni939/
    s1s1s1 = S1S1S1('SSNI-939')

    print(s1s1s1.get_poster_url())
    print(s1s1s1.get_fanart_url())
    print(s1s1s1.get_movie_url())

    print(s1s1s1.get_poster_ext())
    print(s1s1s1.get_fanart_ext())
    print(s1s1s1.get_movie_ext())

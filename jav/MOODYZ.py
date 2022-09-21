#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from utils import http


class MOODYZ(object):
    site_url = 'https://moodyz.com/'

    def __init__(self, video_no):
        self.video_no = video_no = video_no.replace('-', '')

        # 搜索列表
        list_url = 'https://moodyz.com/search/list?keyword=' + video_no
        list_html = http.get(list_url)
        list_soup = BeautifulSoup(list_html, features="html.parser")

        # poster
        self.poster_url = list_soup.find('div', class_="swiper-wrapper").find('img')['data-src']
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # 详情页
        url = list_soup.find('div', class_="swiper-wrapper").find('a')['href']
        html = http.get(url)
        soup = BeautifulSoup(html, features="html.parser")

        # fanart
        self.fanart_url = soup.find('div', class_="swiper-slide").find('img')['data-src']
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

        # movie
        self.movie_url = soup.find('div', class_="video").find('video')['src']
        self.movie_name = os.path.basename(self.movie_url)
        self.movie_ext = os.path.splitext(self.movie_name)[1]

    def download_poster(self):
        response = http.get(self.poster_url)
        return response.content

    def download_fanart(self):
        response = http.get(self.fanart_url)
        return response.content

    def download_movie(self):
        response = http.get(self.movie_url)
        return response.content

    def get_poster_ext(self):
        return self.poster_ext

    def get_fanart_ext(self):
        return self.fanart_ext

    def get_movie_ext(self):
        return self.movie_ext


if __name__ == '__main__':
    # https://moodyz.com/works/detail/MIDE936
    moodyz = MOODYZ('MIDE-936')

    print(moodyz.poster_url)
    print(moodyz.fanart_url)
    print(moodyz.movie_url)

    print(moodyz.poster_ext)
    print(moodyz.fanart_ext)
    print(moodyz.movie_ext)

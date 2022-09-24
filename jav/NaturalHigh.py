#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from utils import http

site_url = 'https://www.naturalhigh.co.jp/'


class NaturalHigh(object):
    def __init__(self, video_no):
        self.video_no = video_no = video_no.lower()

        # 视频详情页html
        url = 'https://www.naturalhigh.co.jp/all/' + video_no + '/'
        html = http.get(url)
        soup = BeautifulSoup(html, features="html.parser")

        # poster
        self.poster_url = soup.find('div', class_="single_main_image").find('img')['data-lazy-src']
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # fanart
        self.fanart_url = soup.find('div', class_="single_main_image").find('a')['href']
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

        # movie
        self.movie_url = soup.find('div', class_="sample_movie").find('div', class_='movie_area').find('video')['src']
        self.movie_name = os.path.basename(self.movie_url)
        self.movie_ext = os.path.splitext(self.movie_name)[1]

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
        return http.download(self.poster_url)

    def download_fanart(self):
        return http.download(self.fanart_url)

    def download_movie(self):
        return http.download(self.movie_url)


if __name__ == '__main__':
    # https://www.naturalhigh.co.jp/all/shn-016/
    natural_high = NaturalHigh('SHN-016')

    print(natural_high.get_poster_url())
    print(natural_high.get_fanart_url())
    print(natural_high.get_movie_url())

    print(natural_high.get_poster_ext())
    print(natural_high.get_fanart_ext())
    print(natural_high.get_movie_ext())

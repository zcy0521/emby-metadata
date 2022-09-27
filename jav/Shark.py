#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from utils import http

site_url = 'https://shark2012-av.com/'


class Shark(object):
    def __init__(self, video_no):
        # 番号
        self.video_no = video_no

        # 详情页
        url = 'https://shark2012-av.com/products/index.php?pn={video_no}'.format(video_no=video_no)
        html = http.get(url, charset='cp932')
        soup = BeautifulSoup(html, features="html.parser")

        # poster
        poster_url = soup.find('div', class_="works-detail").find('img')['src']
        self.poster_url = site_url + poster_url.split('../')[1]
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # fanart
        fanart_url = soup.find('div', class_="works-detail").find('a')['href']
        self.fanart_url = site_url + fanart_url.split('../')[1]
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

        # movie
        movie_url = soup.find('div', class_="works-detail").find('video').find('source')['src']
        self.movie_url = site_url + movie_url.split('../')[1]
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
    # https://shark2012-av.com/products/index.php?pn=MACB-006
    shark = Shark('MACB-006')

    print(shark.get_poster_url())
    print(shark.get_fanart_url())
    print(shark.get_movie_url())

    print(shark.get_poster_ext())
    print(shark.get_fanart_ext())
    print(shark.get_movie_ext())

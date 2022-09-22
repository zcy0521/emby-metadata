#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from utils import http

site_url = 'https://www.ideapocket.com/'


class IdeaPocket(object):
    def __init__(self, video_no):
        self.video_no = video_no = video_no.lower().replace('-', '')

        # 搜索列表
        list_url = 'https://ideapocket.com/search/list?keyword=' + video_no
        list_html = http.get(list_url)
        list_soup = BeautifulSoup(list_html, features="html.parser")

        # poster
        self.poster_url = list_soup.find('div', class_="swiper-wrapper").find('div', class_="item").find('img')[
            'data-src']
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # 详情页
        url = list_soup.find('div', class_="swiper-wrapper").find('div', class_="item").find('a')['href']
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
        return http.download(self.poster_url)

    def download_fanart(self):
        return http.download(self.fanart_url)

    def download_movie(self):
        return http.download(self.movie_url)

    def get_poster_ext(self):
        return self.poster_ext

    def get_fanart_ext(self):
        return self.fanart_ext

    def get_movie_ext(self):
        return self.movie_ext


if __name__ == '__main__':
    # https://www.ideapocket.com/works/detail/ipx536/
    idea_pocket = IdeaPocket('IPX-536')

    print(idea_pocket.poster_url)
    print(idea_pocket.fanart_url)
    print(idea_pocket.movie_url)

    print(idea_pocket.poster_ext)
    print(idea_pocket.fanart_ext)
    print(idea_pocket.movie_ext)

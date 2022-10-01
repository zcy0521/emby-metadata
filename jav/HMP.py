#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from utils import http_util

site_url = 'https://smt.hmp.jp/'


class HMP(object):
    def __init__(self, video_no):
        # 番号
        self.video_no = video_no

        # 搜索列表
        list_url = 'https://smt.hmp.jp/list.php'
        list_param = {'key': video_no}
        list_html = http_util.post(list_url, list_param)
        list_soup = BeautifulSoup(list_html, features="html.parser")

        # poster
        self.poster_url = site_url.rstrip('/') + list_soup.find('p', class_="mainImg").find('img')['data-original']
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # 详情页
        url = site_url.rstrip('/') + list_soup.find('p', class_="mainImg").find('a')['href']
        html = http_util.get(url)
        soup = BeautifulSoup(html, features="html.parser")

        # fanart
        self.fanart_url = site_url.rstrip('/') + soup.find('p', class_="mainImg").find('img')['src']
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

        # movie
        sample_url = site_url.rstrip('/') + soup.find('img', src='/images/detail/btn-det-sample.png').parent['href']
        sample_html = http_util.get(sample_url)
        sample_soup = BeautifulSoup(sample_html, features="html.parser")
        self.movie_url = sample_soup.find('video').find('source')['src']
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
        return http_util.download(self.poster_url)

    def download_fanart(self):
        return http_util.download(self.fanart_url)

    def download_movie(self):
        return http_util.download(self.movie_url)


if __name__ == '__main__':
    hmp = HMP('HODV-21402')

    print(hmp.get_poster_url())
    print(hmp.get_fanart_url())
    print(hmp.get_movie_url())

    print(hmp.get_poster_ext())
    print(hmp.get_fanart_ext())
    print(hmp.get_movie_ext())

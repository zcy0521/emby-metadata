#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

import urllib3
from bs4 import BeautifulSoup

from jav import FANZA
from utils import http_util

# 人妻花園劇場
site_url = 'http://www.tsumabana.com/'


class Tsumabana(object):
    def __init__(self, video_no):
        # 番号
        self.video_no = video_no

        # poster
        post_url = 'http://www.tsumabana.com/images/portfolio/{video_no}.jpg'
        self.poster_url = post_url.format(video_no=video_no.lower().replace('-', ''))
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # 详情页
        self.detail_url = 'http://www.tsumabana.com/{video_no}.php'.format(video_no=video_no.lower().replace('-', ''))
        detail_html = http_util.get(self.detail_url)
        detail_soup = BeautifulSoup(detail_html, features="html.parser")

        # fanart
        self.fanart_url = site_url + detail_soup.find('article', class_="post").find('a')['href']
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

        # movie
        self.movie_url = FANZA.get_movie_url(video_no)
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


def get_movie_url(video_no):
    # 详情页
    url = 'http://www.tsumabana.com/{video_no}.php'.format(video_no=video_no.lower().replace('-', ''))
    html = http_util.get(url)
    soup = BeautifulSoup(html, features="html.parser")

    # 获取 dmm 的 redirect url
    dmm_url = soup.find('article', class_="post").find_all('p')[-1].find('a')['href']
    dmm_res = proxy.urlopen('GET', dmm_url, retries=urllib3.Retry(10, redirect=10))
    dmm_url = dmm_res.geturl()

    # 返回 movie url
    return FANZA.get_movie_url(video_no)


if __name__ == '__main__':
    # http://www.tsumabana.com/hzgd116.php
    tsumabana = Tsumabana('HZGD-116')

    print(tsumabana.get_poster_url())
    print(tsumabana.get_fanart_url())
    print(tsumabana.get_movie_url())

    print(tsumabana.get_poster_ext())
    print(tsumabana.get_fanart_ext())
    print(tsumabana.get_movie_ext())

    print(get_movie_url('HZGD-116'))

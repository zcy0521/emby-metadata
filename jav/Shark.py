#!/usr/bin/envpython3
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup

from utils import http_util


class Shark(object):
    # 官网
    SITE_URL = 'https://shark2012-av.com'
    DETAIL_URL = 'https://shark2012-av.com/products/index.php?pn={video_no}'

    def __init__(self, video_no):
        self.video_no = video_no

        # 详情页
        detail_url = Shark.DETAIL_URL.format(video_no=video_no)
        detail_html = http_util.get(detail_url, charset='cp932')
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        poster_url = self.detail_soup.find('div', class_="works-detail").find('img')['src']
        return Shark.SITE_URL + poster_url.lstrip('..')

    def get_backdrop_url(self):
        backdrop_url = self.detail_soup.find('div', class_="works-detail").find('a')['href']
        return Shark.SITE_URL + backdrop_url.lstrip('..')

    def get_trailer_url(self):
        trailer_url = self.detail_soup.find('div', class_="works-detail").find('video').find('source')['src']
        return Shark.SITE_URL + trailer_url.lstrip('..')


if __name__ == '__main__':
    # https://shark2012-av.com/products/index.php?pn=MACB-006
    shark = Shark('MACB-006')
    print(shark.get_poster_url())
    print(shark.get_backdrop_url())
    print(shark.get_trailer_url())

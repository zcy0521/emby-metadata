#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from utils import http


class NaturalHigh(object):
    site_url = 'https://www.naturalhigh.co.jp/'

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

    def download_poster(self):
        response = http.get(self.poster_url)
        return response.content

    def download_fanart(self):
        response = http.get(self.fanart_url)
        return response.content

    def get_poster_ext(self):
        return self.poster_ext

    def get_fanart_ext(self):
        return self.fanart_ext


if __name__ == '__main__':
    # https://www.naturalhigh.co.jp/all/shn-016/
    natural_high = NaturalHigh('SHN-016')

    print(natural_high.poster_url)
    print(natural_high.fanart_url)

    print(natural_high.poster_ext)
    print(natural_high.fanart_ext)

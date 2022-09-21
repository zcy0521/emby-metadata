#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from utils import http


class Madonna(object):
    site_url = 'https://www.madonna-av.com/'

    def __init__(self, video_no):
        self.video_no = video_no = video_no.lower().replace('-', '')

        # 搜索列表
        list_url = 'https://madonna-av.com/search/list?keyword=' + video_no
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
    # https://www.madonna-av.com/works/detail/juy983/
    madonna = Madonna('JUY-983')

    print(madonna.poster_url)
    print(madonna.fanart_url)

    print(madonna.poster_ext)
    print(madonna.fanart_ext)

#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from utils import http


class MOODYZ(object):
    site_url = 'https://moodyz.com/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }

    def __init__(self, video_no):
        self.video_no = video_no = video_no.lower().replace('-', '')

        # 搜索列表
        list_url = 'https://moodyz.com/search/list?keyword=' + video_no
        list_response = http.get(list_url, self.headers)
        list_html = list_response.text
        list_soup = BeautifulSoup(list_html, features="html.parser")

        # poster
        self.poster_url = list_soup.find('div', class_="swiper-wrapper").find('img')['data-src']
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # 详情页
        url = list_soup.find('div', class_="swiper-wrapper").find('a')['href']
        response = http.get(url, self.headers)
        html = response.text
        soup = BeautifulSoup(html, features="html.parser")

        # fanart
        self.fanart_url = soup.find('div', class_="swiper-slide").find('img')['src']
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

    def download_poster(self):
        response = http.get(self.poster_url, self.headers)
        return response.content

    def download_fanart(self):
        response = http.get(self.fanart_url, self.headers)
        return response.content

    def get_poster_ext(self):
        return self.poster_ext

    def get_fanart_ext(self):
        return self.fanart_ext


if __name__ == '__main__':
    # https://moodyz.com/works/detail/mide607/
    moodyz = MOODYZ('MIDE-607')

    print(moodyz.poster_url)
    print(moodyz.fanart_url)

    print(moodyz.poster_ext)
    print(moodyz.fanart_ext)

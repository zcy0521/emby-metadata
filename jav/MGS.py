#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import json
import os

from bs4 import BeautifulSoup

from utils import http

site_url = 'https://www.mgstage.com/'


class MGS(object):
    def __init__(self, video_no):
        self.video_no = video_no

        # 年龄认证Cookie
        headers = {'Cookie': 'adc=1'}

        # 详情页
        url = 'https://www.mgstage.com/product/product_detail/' + video_no + '/'
        html = http.get(url, headers)
        soup = BeautifulSoup(html, features="html.parser")

        # fanart
        self.fanart_url = soup.find('div', class_="detail_data").find('a', class_='link_magnify')['href']
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

        # poster
        self.poster_url = self.fanart_url.replace('pb', 'pf')
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # movie
        sample_token = soup.find('div', class_="detail_data").find('a', class_='button_sample')['href'].split(
            '/sampleplayer/sampleplayer.html/')[1]
        sample_url = 'https://www.mgstage.com/sampleplayer/sampleRespons.php?pid=' + sample_token
        sample_html = http.get(sample_url, headers)
        sample_json = json.loads(sample_html)
        self.movie_url = sample_json['url'].split('.ism')[0] + '.mp4'
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
    # https://www.mgstage.com/product/product_detail/259LUXU-1033/
    # mgs = MGS('SIRO-4989')
    # mgs = MGS('200GANA-2789')
    # mgs = MGS('259LUXU-1033')
    mgs = MGS('ABP-721')

    print(mgs.poster_url)
    print(mgs.fanart_url)
    print(mgs.movie_url)

    print(mgs.poster_ext)
    print(mgs.fanart_ext)
    print(mgs.movie_ext)

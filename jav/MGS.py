#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import json
import os

from bs4 import BeautifulSoup

from utils import http_util

site_url = 'https://www.mgstage.com/'
age_check_headers = {'Cookie': 'adc=1'}


class MGS(object):
    def __init__(self, video_no):
        # 番号
        self.video_no = video_no

        # 详情页
        url = 'https://www.mgstage.com/product/product_detail/{video_no}/'.format(video_no=video_no)
        html = http_util.get(url, age_check_headers)
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
        sample_url = 'https://www.mgstage.com/sampleplayer/sampleRespons.php?pid={token}'.format(token=sample_token)
        sample_html = http_util.get(sample_url, age_check_headers)
        sample_json = json.loads(sample_html)
        self.movie_url = sample_json['url'].split('.ism')[0] + '.mp4'
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
    # https://www.mgstage.com/product/product_detail/259LUXU-1033/
    # mgs = MGS('SIRO-4989')
    # mgs = MGS('200GANA-2789')
    mgs = MGS('259LUXU-1033')

    print(mgs.get_poster_url())
    print(mgs.get_fanart_url())
    print(mgs.get_movie_url())

    print(mgs.get_poster_ext())
    print(mgs.get_fanart_ext())
    print(mgs.get_movie_ext())

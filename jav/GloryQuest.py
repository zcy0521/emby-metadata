#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from bs4 import BeautifulSoup

from jav import FANZA
from utils import http_util

# グローリークエスト
site_url = 'https://www.gloryquest.tv/'


class GloryQuest(object):
    def __init__(self, video_no):
        # 番号
        self.video_no = video_no

        # 搜索列表
        list_url = 'https://www.gloryquest.tv/search.php?KeyWord={video_no}'.format(video_no=video_no)
        list_html = http_util.get(list_url)
        list_soup = BeautifulSoup(list_html, features="html.parser")

        # poster
        poster_url = list_soup.find('ul', id='scene').find('li').find('span', class_='thumb2').find('img')['data-original']
        self.poster_url = site_url + poster_url.lstrip('/')
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # 详情页
        detail_url = 'https://www.gloryquest.tv/item.php?id={video_no}'.format(video_no=video_no)
        detail_html = http_util.get(detail_url)
        detail_soup = BeautifulSoup(detail_html, features="html.parser")

        # fanart
        fanart_url = detail_soup.find('div', class_='package').find('img')['src']
        self.fanart_url = site_url + fanart_url.lstrip('/')
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1].split('?')[0]

        # movie
        self.movie_url = FANZA.get_movie_url(video_no)
        self.movie_name = os.path.basename(self.movie_url)
        self.movie_ext = os.path.splitext(self.movie_name)[1]

    def get_video_no(self):
        return self.video_no

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
    # https://www.gloryquest.tv/item.php?id=GVH-313
    glory_quest = GloryQuest('GVH-313')

    print(glory_quest.get_poster_url())
    print(glory_quest.get_fanart_url())
    print(glory_quest.get_movie_url())

    print(glory_quest.get_poster_ext())
    print(glory_quest.get_fanart_ext())
    print(glory_quest.get_movie_ext())

#!/usr/bin/envpython3
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup

from jav.Fanza import Fanza
from utils import http_util


class GloryQuest(object):
    # グローリークエスト 官网
    SITE_URL = 'https://www.gloryquest.tv'
    SEARCH_URL = 'https://www.gloryquest.tv/search.php?KeyWord={video_no}'
    DETAIL_URL = 'https://www.gloryquest.tv/item.php?id={video_no}'

    def __init__(self, video_no):
        self.video_no = video_no

        # 搜索列表
        list_url = GloryQuest.SEARCH_URL.format(video_no=video_no)
        list_html = http_util.get(list_url)
        self.list_soup = BeautifulSoup(list_html, features="html.parser")

        # 详情页
        detail_url = GloryQuest.DETAIL_URL.format(video_no=video_no)
        detail_html = http_util.get(detail_url)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        poster_url = self.list_soup.find('ul', id='scene').find('li').find('span', class_='thumb2').find('img')['data-original']
        return GloryQuest.SITE_URL + poster_url

    def get_backdrop_url(self):
        fanart_url = self.detail_soup.find('div', class_='package').find('img')['src']
        return GloryQuest.SITE_URL + fanart_url

    def get_trailer_url(self):
        fanza = Fanza(self.video_no)
        return fanza.get_trailer_url()


if __name__ == '__main__':
    # https://www.gloryquest.tv/item.php?id=GVH-313
    glory_quest = GloryQuest('GVH-313')
    print(glory_quest.get_poster_url())
    print(glory_quest.get_backdrop_url())
    print(glory_quest.get_trailer_url())

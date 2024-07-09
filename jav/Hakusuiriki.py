#!/usr/bin/envpython3
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup

from jav.Fanza import Fanza
from utils import http_util


class Hakusuiriki(object):
    # 官网
    SITE_URL = 'https://hakusuiriki.tv'
    DETAIL_URL = 'https://hakusuiriki.tv/dl_detail.php?code={video_no}'

    def __init__(self, video_no):
        self.video_no = video_no

        # 详情页
        detail_url = Hakusuiriki.DETAIL_URL.format(video_no=video_no)
        detail_html = http_util.get(detail_url)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        poster_url = self.detail_soup.find('div', id='newmovies').find('tr').find('th').find('img')['src']
        return Hakusuiriki.SITE_URL + poster_url.lstrip('.')

    def get_backdrop_url(self):
        backdrop_url = self.detail_soup.find('div', id='newmovies').find('tr').find('th').find('a')['href']
        return Hakusuiriki.SITE_URL + backdrop_url.lstrip('.')

    def get_trailer_url(self):
        fanza = Fanza(self.video_no)
        return fanza.get_trailer_url()


if __name__ == '__main__':
    # https://hakusuiriki.tv/dl_detail.php?code=CEAD-465
    hakusuiriki = Hakusuiriki('CEAD-465')
    print(hakusuiriki.get_poster_url())
    print(hakusuiriki.get_backdrop_url())
    print(hakusuiriki.get_trailer_url())

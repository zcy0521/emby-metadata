#!/usr/bin/envpython3
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup

from jav.Fanza import Fanza
from utils import http_util


class AuroraProject(object):
    # 官网
    SITE_URL = 'https://www.aurora-pro.com/'
    DETAIL_URL = 'https://www.aurora-pro.com/shop/-/product/p/goods_id={video_no}/'

    def __init__(self, video_no):
        self.video_no = video_no

        # 详情页
        detail_url = AuroraProject.DETAIL_URL.format(video_no=video_no)
        detail_html = http_util.get(detail_url)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        return self.get_backdrop_url().replace('open_xl', 'close_m')

    def get_backdrop_url(self):
        return  self.detail_soup.find('img', id='main_pkg')['src']

    def get_trailer_url(self):
        fanza = Fanza(self.video_no)
        return fanza.get_trailer_url()


if __name__ == '__main__':
    # https://www.aurora-pro.com/shop/-/product/p/goods_id=APAA-405/
    aurora = AuroraProject('APAA-405')
    print(aurora.get_poster_url())
    print(aurora.get_backdrop_url())
    print(aurora.get_trailer_url())

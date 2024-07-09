#!/usr/bin/envpython3
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup

from utils import http_util


class Faleno(object):
    # 官网
    SITE_URL = 'https://faleno.jp/'
    SEARCH_URL = 'https://faleno.jp/top/?s={video_no}'

    def __init__(self, video_no):
        self.video_no = video_no

        # 搜索列表
        list_url = Faleno.SEARCH_URL.format(video_no=video_no.lower().replace('-', ''))
        list_html = http_util.get(list_url)
        self.list_soup = BeautifulSoup(list_html, features="html.parser")

        # 详情页
        detail_url = self.list_soup.find('ul', class_='clearfix').find_all('li')[0].find('a')['href']
        detail_html = http_util.get(detail_url)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        return self.list_soup.find('ul', class_='clearfix').find_all('li')[0].find('img')['src']

    def get_backdrop_url(self):
        return self.detail_soup.find('a', class_="pop_sample").find('img')['src']

    def get_trailer_url(self):
        return self.detail_soup.find('a', class_="pop_sample")['href']


if __name__ == '__main__':
    # https://faleno.jp/top/?s=fsdss609
    faleno = Faleno('FSDSS-609')
    print(faleno.get_poster_url())
    print(faleno.get_backdrop_url())
    print(faleno.get_trailer_url())

#!/usr/bin/envpython3
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup

from utils import http_util


class HMP(object):
    # 官网
    SITE_URL = 'https://smt.hmp.jp'
    SEARCH_URL = 'https://smt.hmp.jp/list.php'

    def __init__(self, video_no):
        self.video_no = video_no

        # 搜索列表
        list_html = http_util.post(HMP.SEARCH_URL, {'key': video_no})
        self.list_soup = BeautifulSoup(list_html, features="html.parser")

        # 详情页
        detail_url = HMP.SITE_URL + self.list_soup.find('p', class_="mainImg").find('a')['href']
        detail_html = http_util.get(detail_url)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        poster_url = self.list_soup.find('p', class_="mainImg").find('img')['data-original']
        return HMP.SITE_URL + poster_url

    def get_backdrop_url(self):
        backdrop_url = self.detail_soup.find('p', class_="mainImg").find('img')['src']
        return HMP.SITE_URL + backdrop_url

    def get_trailer_url(self):
        sample_url = self.detail_soup.find('img', src='/images/detail/btn-det-sample.png').parent['href']
        sample_url = HMP.SITE_URL + sample_url
        sample_html = http_util.get(sample_url)
        sample_soup = BeautifulSoup(sample_html, features="html.parser")
        trailer_url = sample_soup.find('video').find('source')['src']
        return HMP.SITE_URL + trailer_url


if __name__ == '__main__':
    hmp = HMP('HODV-21758')
    print(hmp.get_poster_url())
    print(hmp.get_backdrop_url())
    print(hmp.get_trailer_url())

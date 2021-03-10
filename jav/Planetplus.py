#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup


class Planetplus(object):
    site_url = 'http://planetplus.jp/'

    def __init__(self, video_no):
        self.session = session = requests.Session()
        self.headers = headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

        # 查询列表页
        list_url= 'http://planetplus.jp/wp01/?s=' + video_no
        list_response = session.get(list_url, headers=headers)
        list_html = list_response.text
        list_soup = BeautifulSoup(list_html, features="html.parser")

        # poster
        self.poster_url = list_soup.find('article').find('img')['src']

        # 详情页
        info_url = list_soup.find('article').find('a')['href']
        info_response = session.get(info_url, headers=headers)
        info_html = info_response.text
        info_soup = BeautifulSoup(info_html, features="html.parser")

        # fanart
        self.fanart_url = info_soup.find('div', class_="execphpwidget").find('a')['href']

    def download_poster(self):
        response = self.session.get(self.poster_url, headers=self.headers)
        return response.content

    def download_fanart(self):
        response = self.session.get(self.fanart_url, headers=self.headers)
        return response.content


if __name__ == '__main__':
    planetplus = Planetplus('NACR-387')

    print(planetplus.poster_url)
    print(planetplus.fanart_url)

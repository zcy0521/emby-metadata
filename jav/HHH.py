#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup


class HHH(object):
    site_url = 'https://www.hhh-av.com/'

    def __init__(self, video_no):
        self.video_no = video_no = video_no.lower().replace('-', '')
        self.session = session = requests.Session()
        self.headers = headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

        # 查询列表页
        list_url= 'https://www.hhh-av.com/search/list/?q=' + video_no
        list_response = session.get(list_url, headers=headers)
        list_html = list_response.text
        list_soup = BeautifulSoup(list_html, features="html.parser")

        # poster
        poster_url = list_soup.find('ul', class_="lst-works").find('img')['src']
        self.poster_url = self.site_url.rstrip('/') + poster_url

        # 详情页
        info_url = list_soup.find('ul', class_="lst-works").find('a')['href']
        info_url = self.site_url.rstrip('/') + info_url
        info_response = session.get(info_url, headers=headers)
        info_html = info_response.text
        info_soup = BeautifulSoup(info_html, features="html.parser")

        # fanart
        fanart_url = info_soup.find('div', class_="area-sample").find('img')['src']
        self.fanart_url = self.site_url.rstrip('/') + fanart_url

    def download_poster(self):
        response = self.session.get(self.poster_url, headers=self.headers)
        return response.content

    def download_fanart(self):
        response = self.session.get(self.fanart_url, headers=self.headers)
        return response.content


if __name__ == '__main__':
    hhh = HHH('HUNTA-926')

    print(hhh.poster_url)
    print(hhh.fanart_url)

#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup


class HMP(object):
    site_url = 'https://smt.hmp.jp/'

    def __init__(self, video_no):
        self.video_no = video_no
        self.session = session = requests.Session()
        self.headers = headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

        # 查询列表页
        list_url= 'https://smt.hmp.jp/list.php'
        list_data = {'key': video_no}
        list_response = session.post(list_url, data=list_data, headers=headers)
        list_html = list_response.text
        list_soup = BeautifulSoup(list_html, features="html.parser")

        # poster
        poster_url = list_soup.find('p', class_="mainImg").find('img')['data-original']
        self.poster_url = self.site_url.rstrip('/') + poster_url

        # 详情页
        info_url = list_soup.find('p', class_="mainImg").find('a')['href']
        info_url = self.site_url.rstrip('/') + info_url
        info_response = session.get(info_url, headers=headers)
        info_html = info_response.text
        info_soup = BeautifulSoup(info_html, features="html.parser")

        # fanart
        fanart_url = info_soup.find('p', class_="mainImg").find('img')['src']
        self.fanart_url = self.site_url.rstrip('/') + fanart_url

    def download_poster(self):
        response = self.session.get(self.poster_url, headers=self.headers)
        return response.content

    def download_fanart(self):
        response = self.session.get(self.fanart_url, headers=self.headers)
        return response.content


if __name__ == '__main__':
    hmp = HMP('HODV-21402')

    print(hmp.poster_url)
    print(hmp.fanart_url)

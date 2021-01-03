#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup


class Prestige(object):
    site_url = 'https://www.prestige-av.com/'

    def __init__(self, video_no):
        self.video_no = video_no = video_no.lower()
        self.url = url = 'https://www.prestige-av.com/goods/goods_detail.php?sku=' + video_no

        self.session = session = requests.Session()
        self.headers = headers = {
            'referer': self.url,
            'cookie': 'coc=1; age_auth=1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

        # 视频详情页html
        response = session.get(url, headers=headers)
        html = response.text

        # BeautifulSoup https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/
        # pip install beautifulsoup4
        soup = BeautifulSoup(html, features="html.parser")

        # poster
        poster_url = soup.find('p', class_="package_layout").find('img', class_='border_image')['src']
        self.poster_url = self.site_url.rstrip('/') + poster_url

        # fanart
        fanart_url = soup.find('p', class_="package_layout").find('a', class_='sample_image')['href']
        self.fanart_url = self.site_url.rstrip('/') + fanart_url

    def download_poster(self):
        response = self.session.get(self.poster_url, headers=self.headers)
        return response.content

    def download_fanart(self):
        response = self.session.get(self.fanart_url, headers=self.headers)
        return response.content


if __name__ == '__main__':
    # https://www.prestige-av.com/goods/goods_detail.php?sku=abp-721
    prestige = Prestige('ABP-721')

    print(prestige.poster_url)
    print(prestige.fanart_url)

#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup


class Shark(object):
    site_url = 'https://shark2012-av.com/'

    def __init__(self, video_no):
        self.url = url = 'https://shark2012-av.com/products/index.php?pn=' + video_no

        self.session = session = requests.Session()
        self.headers = headers = {
            'Referer': url,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

        # 视频详情页html
        response = session.get(url, headers=headers)
        html = response.text

        # BeautifulSoup https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/
        # pip install beautifulsoup4
        soup = BeautifulSoup(html, features="html.parser")

        # poster
        poster_url = soup.find('div', class_="works-detail").find('img')['src']
        self.poster_url = self.site_url + poster_url

        # fanart
        fanart_url = soup.find('div', class_="works-detail").find('a')['href']
        self.fanart_url = self.site_url + fanart_url

    def download_poster(self):
        response = self.session.get(self.poster_url, headers=self.headers)
        return response.content

    def download_fanart(self):
        response = self.session.get(self.fanart_url, headers=self.headers)
        return response.content


if __name__ == '__main__':
    # https://shark2012-av.com/products/index.php?pn=JBJB-019
    shark = Shark('MACB-006')

    print(shark.poster_url)
    print(shark.fanart_url)

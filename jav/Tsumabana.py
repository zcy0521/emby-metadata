#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup


class Tsumabana(object):
    # 人妻花園劇場
    site_url = 'http://www.tsumabana.com/'
    post_url = 'http://www.tsumabana.com/images/portfolio/{video_no}.jpg'

    def __init__(self, video_no):
        self.video_no = video_no = video_no.lower().replace('-', '')
        self.url = url = 'http://www.tsumabana.com/' + video_no + '.php'

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
        self.poster_url = self.post_url.format(video_no=video_no)

        # fanart
        fanart_url = soup.find('article', class_="post").find('a')['href']
        self.fanart_url = self.site_url + fanart_url

    def download_poster(self):
        response = self.session.get(self.poster_url, headers=self.headers)
        return response.content

    def download_fanart(self):
        response = self.session.get(self.fanart_url, headers=self.headers)
        return response.content


if __name__ == '__main__':
    # http://www.tsumabana.com/hzgd116.php
    tsumabana = Tsumabana('HZGD-116')

    print(tsumabana.poster_url)
    print(tsumabana.fanart_url)

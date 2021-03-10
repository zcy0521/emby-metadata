#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup


class KMP(object):
    # K.M.Produce
    site_url = 'https://www.km-produce.com/'
    post_url = 'https://www.km-produce.com/img/title0/{video_no}.jpg'

    # 宇宙企画
    uchu_site_url = 'http://uchu.co.jp/'

    def __init__(self, video_no):
        self.video_no = video_no = video_no.lower()
        self.url = url = 'https://www.km-produce.com/works/' + video_no

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
        fanart_url = soup.find('div', class_="details").find('a')['href']
        self.fanart_url = self.site_url + fanart_url

    def download_poster(self):
        response = self.session.get(self.poster_url, headers=self.headers)
        return response.content

    def download_fanart(self):
        response = self.session.get(self.fanart_url, headers=self.headers)
        return response.content


if __name__ == '__main__':
    # https://www.km-produce.com/works/mdtm-515
    kmp = KMP('MDTM-515')

    print(kmp.poster_url)
    print(kmp.fanart_url)

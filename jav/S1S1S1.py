#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup


class S1S1S1(object):
    site_url = 'https://www.s1s1s1.com/'

    def __init__(self, video_no):
        self.video_no = video_no = video_no.lower().replace('-', '')
        self.url = url = 'https://www.s1s1s1.com/works/detail/' + video_no + '/'

        self.session = session = requests.Session()
        self.headers = headers = {
            'Referer': self.url,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

        # 视频详情页html
        response = session.get(url, headers=headers)
        html = response.text

        # BeautifulSoup https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/
        # pip install beautifulsoup4
        soup = BeautifulSoup(html, features="html.parser")

        # poster
        self.poster_url = soup.find(attrs={"property": "og:image"})['content']

        # fanart
        fanart_url = soup.find('li', class_="item").find('img')['src']
        self.fanart_url = self.site_url.rstrip('/') + fanart_url

    def download_poster(self):
        response = self.session.get(self.poster_url, headers=self.headers)
        return response.content

    def download_fanart(self):
        response = self.session.get(self.fanart_url, headers=self.headers)
        return response.content


if __name__ == '__main__':
    # https://www.s1s1s1.com/works/detail/ssni647/
    s1s1s1 = S1S1S1('SSNI-647')

    print(s1s1s1.poster_url)
    print(s1s1s1.fanart_url)

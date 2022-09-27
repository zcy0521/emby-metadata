#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import base64
import io
import os

from bs4 import BeautifulSoup
from urllib3.contrib.socks import SOCKSProxyManager

from utils import http

site_url = 'https://ec.sod.co.jp/'


class SOD(object):
    def __init__(self, video_no):
        # 番号
        self.video_no = video_no

        # 详情页url
        url = 'https://ec.sod.co.jp/prime/videos/?id={video_no}'.format(video_no=video_no)

        # 年龄检查
        check_url = 'https://ec.sod.co.jp/prime/_ontime.php'
        check_header = {'Referer': url}
        proxy = SOCKSProxyManager('socks5h://localhost:1080/')
        check_r = proxy.urlopen('GET', check_url, headers=check_header, redirect=False)

        # 详情页
        headers = {'Cookie': check_r.headers['Set-Cookie'], 'Referer': url}
        r = proxy.request('GET', url, headers=headers)
        html = r.data.decode('utf-8')
        soup = BeautifulSoup(html, features="html.parser")

        # poster
        self.poster_url = soup.find('div', class_="videos_samimg").find('img')['src']
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # fanart
        self.fanart_url = soup.find('div', class_="videos_samimg").find('a')['href']
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

        # 视频页
        movie_url = 'https://ec.sod.co.jp/prime/videos/sample.php?id=' + video_no
        movie_headers = {'Cookie': check_r.headers['Set-Cookie'], 'Referer': movie_url}
        movie_r = proxy.request('GET', movie_url, headers=movie_headers)
        movie_html = movie_r.data.decode('utf-8')
        movie_soup = BeautifulSoup(movie_html, features="html.parser")

        # movie
        self.movie_url = movie_soup.find('video').find('source')['src']
        self.movie_name = os.path.basename(self.movie_url)
        self.movie_ext = os.path.splitext(self.movie_name)[1]

    def get_poster_url(self):
        poster_bytes = self.download_poster()
        encoded_bytes = base64.b64encode(poster_bytes)
        encoded_str = encoded_bytes.decode('utf-8')
        return 'data:image/' + self.poster_ext.replace('.', '') + ';base64,' + encoded_str

    def get_fanart_url(self):
        fanart_bytes = self.download_fanart()
        encoded_bytes = base64.b64encode(fanart_bytes)
        encoded_str = encoded_bytes.decode('utf-8')
        return 'data:image/' + self.fanart_ext.replace('.', '') + ';base64,' + encoded_str

    def get_movie_url(self):
        movie_bytes = self.download_movie()
        encoded_bytes = base64.b64encode(movie_bytes)
        encoded_str = encoded_bytes.decode('utf-8')
        return 'data:video/' + self.movie_ext.replace('.', '') + ';base64,' + encoded_str

    def get_poster_ext(self):
        return self.poster_ext

    def get_fanart_ext(self):
        return self.fanart_ext

    def get_movie_ext(self):
        return self.movie_ext

    def download_poster(self):
        # 添加referer 绕过 Amazon CloudFront 图片防盗链
        headers = {'referer': 'https://ec.sod.co.jp/'}
        return http.download(self.poster_url, headers)

    def download_fanart(self):
        headers = {'referer': 'https://ec.sod.co.jp/'}
        return http.download(self.fanart_url, headers)

    def download_movie(self):
        headers = {'referer': 'https://ec.sod.co.jp/'}
        return http.download(self.movie_url, headers)


if __name__ == '__main__':
    # https://ec.sod.co.jp/prime/videos/?id=STARS-212
    sod = SOD('STARS-212')

    print(sod.get_poster_url())
    print(sod.get_fanart_url())
    print(sod.get_movie_url())

    print(sod.get_poster_ext())
    print(sod.get_fanart_ext())
    print(sod.get_movie_ext())

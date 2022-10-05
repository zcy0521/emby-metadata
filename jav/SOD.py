#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import base64
import os

from bs4 import BeautifulSoup
from urllib3.contrib.socks import SOCKSProxyManager

proxy = SOCKSProxyManager('socks5h://192.168.50.254:1080/')

site_url = 'https://ec.sod.co.jp/'

# 添加referer 绕过 Amazon CloudFront 图片防盗链
cloud_front_header = {'referer': 'https://ec.sod.co.jp/'}


class SOD(object):
    def __init__(self, video_no):
        # 番号
        self.video_no = video_no

        # 详情页url
        self.detail_url = 'https://ec.sod.co.jp/prime/videos/?id={video_no}'.format(video_no=video_no)

        # 年龄检查
        check_r = age_check(self.detail_url)

        # 详情页
        headers = {'Cookie': check_r.headers['Set-Cookie'], 'Referer': self.detail_url}
        r = proxy.request('GET', self.detail_url, headers=headers)
        detail_soup = BeautifulSoup(r.data, features="html.parser")

        # poster
        self.poster_url = detail_soup.find('div', class_="videos_samimg").find('img')['src']
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # fanart
        self.fanart_url = detail_soup.find('div', class_="videos_samimg").find('a')['href']
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

        # movie
        self.movie_url = get_movie_url(video_no, check_r)
        self.movie_name = os.path.basename(self.movie_url)
        self.movie_ext = os.path.splitext(self.movie_name)[1]

    def get_video_no(self):
        return self.video_no

    def get_detail_url(self):
        return self.detail_url

    def get_poster_url(self):
        return base64_image(self.poster_url)

    def get_fanart_url(self):
        return base64_image(self.fanart_url)

    def get_movie_url(self):
        return base64_video(self.movie_url)

    def get_poster_ext(self):
        return self.poster_ext

    def get_fanart_ext(self):
        return self.fanart_ext

    def get_movie_ext(self):
        return self.movie_ext

    def download_poster(self):
        r = proxy.request('GET', self.poster_url, headers=cloud_front_header)
        return r.data

    def download_fanart(self):
        r = proxy.request('GET', self.fanart_url, headers=cloud_front_header)
        return r.data

    def download_movie(self):
        r = proxy.request('GET', self.movie_url, headers=cloud_front_header)
        return r.data


def age_check(refer_url):
    age_check_url = 'https://ec.sod.co.jp/prime/_ontime.php'
    headers = {'Referer': refer_url}

    check_r = proxy.urlopen('GET', age_check_url, headers=headers, redirect=False)
    return check_r


def get_movie_url(video_no, check_r):
    movie_url = 'https://ec.sod.co.jp/prime/videos/sample.php?id=' + video_no
    headers = {'Cookie': check_r.headers['Set-Cookie'], 'Referer': movie_url}

    # 视频页
    movie_r = proxy.request('GET', movie_url, headers=headers)
    movie_soup = BeautifulSoup(movie_r.data, features="html.parser")
    return movie_soup.find('video').find('source')['src']


def base64_image(image_url):
    image_name = os.path.basename(image_url)
    image_ext = os.path.splitext(image_name)[1]

    poster_r = proxy.request('GET', image_url, headers=cloud_front_header)
    encoded_bytes = base64.b64encode(poster_r.data)
    encoded_str = encoded_bytes.decode('utf-8')
    return 'data:image/' + image_ext.lstrip('.') + ';base64,' + encoded_str


def base64_video(video_url):
    video_name = os.path.basename(video_url)
    video_ext = os.path.splitext(video_name)[1]

    poster_r = proxy.request('GET', video_url, headers=cloud_front_header)
    encoded_bytes = base64.b64encode(poster_r.data)
    encoded_str = encoded_bytes.decode('utf-8')
    return 'data:video/' + video_ext.lstrip('.') + ';base64,' + encoded_str


def search_actress(video_no):
    detail_url = 'https://ec.sod.co.jp/prime/videos/?id={video_no}'.format(video_no=video_no)

    # 年龄检查
    check_r = age_check(detail_url)
    headers = {'Cookie': check_r.headers['Set-Cookie'], 'Referer': detail_url}

    # 详情页
    detail_r = proxy.request('GET', detail_url, headers=headers)
    detail_soup = BeautifulSoup(detail_r.data, features="html.parser")

    # actress
    actress_td = detail_soup.find('table', id='v_introduction').find_all('tr')[4].find_all('td')[1].find('a')
    if actress_td is None:
        videos = []
        return videos

    actress_url = detail_soup.find('table', id='v_introduction').find_all('tr')[4].find_all('td')[1].find('a')['href']
    return search_videos(actress_url, check_r)


def search_series(video_no):
    detail_url = 'https://ec.sod.co.jp/prime/videos/?id={video_no}'.format(video_no=video_no)

    # 年龄检查
    check_r = age_check(detail_url)
    headers = {'Cookie': check_r.headers['Set-Cookie'], 'Referer': detail_url}

    # 详情页
    detail_r = proxy.request('GET', detail_url, headers=headers)
    detail_soup = BeautifulSoup(detail_r.data, features="html.parser")

    # series
    series_td = detail_soup.find('table', id='v_introduction').find_all('tr')[2].find_all('td')[1].find('a')
    if series_td is None:
        videos = []
        return videos

    series_url = detail_soup.find('table', id='v_introduction').find_all('tr')[2].find_all('td')[1].find('a')['href']
    return search_videos(series_url, check_r)


def search_videos(search_url, check_r):
    search_url = site_url + 'prime' + search_url.lstrip('..') + '&sort=2'
    search_r = proxy.request('GET', search_url, headers={'Cookie': check_r.headers['Set-Cookie']})
    search_soup = BeautifulSoup(search_r.data, 'html.parser')

    item_div = search_soup.find('div', id='videos_search_main').find_all('div', id='videos_s_mainbox')
    print('video数量: ' + str(len(item_div)))

    # 查询video列表
    videos = []
    for item in reversed(item_div):
        # detail
        detail_url = site_url + 'prime/videos' + item.find('a')['href'].lstrip('..')
        detail_headers = {'Cookie': check_r.headers['Set-Cookie'], 'Referer': search_url}
        detail_r = proxy.request('GET', detail_url, headers=detail_headers)
        detail_soup = BeautifulSoup(detail_r.data, 'html.parser')

        # video_no
        video_no = detail_url.split('?id=')[1]
        print('(' + video_no + ')[' + detail_url + ']')

        # poster
        poster_url = detail_soup.find('div', class_="videos_samimg").find('img')['src']
        print(poster_url)

        # fanart
        fanart_url = detail_soup.find('div', class_="videos_samimg").find('a')['href']
        print(fanart_url)

        # movie
        movie_url = get_movie_url(video_no, check_r)
        print(movie_url)

        video = {'number': video_no, 'url': detail_url,
                 'poster_url': base64_image(poster_url), 'fanart_url': base64_image(fanart_url),
                 'movie_url': base64_video(movie_url)}
        videos.append(video)

    return videos


if __name__ == '__main__':
    # https://ec.sod.co.jp/prime/videos/?id=STARS-212
    sod = SOD('STARS-212')

    print(sod.get_poster_url())
    print(sod.get_fanart_url())
    print(sod.get_movie_url())

    print(sod.get_poster_ext())
    print(sod.get_fanart_ext())
    print(sod.get_movie_ext())

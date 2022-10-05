#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import json
import os

from bs4 import BeautifulSoup

from utils import http_util

site_url = 'https://www.mgstage.com/'

# 年龄检查cookie
age_check_headers = {'Cookie': 'adc=1'}


class MGS(object):
    def __init__(self, video_no):
        # 番号
        self.video_no = video_no

        # 详情页
        self.detail_url = 'https://www.mgstage.com/product/product_detail/{video_no}/'.format(video_no=video_no)
        detail_html = http_util.get(self.detail_url, age_check_headers)
        detail_soup = BeautifulSoup(detail_html, features="html.parser")

        # fanart
        self.fanart_url = detail_soup.find('div', class_="detail_data").find('a', class_='link_magnify')['href']
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

        # poster
        self.poster_url = self.fanart_url.replace('pb', 'pf')
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # movie
        self.movie_url = get_movie_url(detail_soup)
        self.movie_name = os.path.basename(self.movie_url)
        self.movie_ext = os.path.splitext(self.movie_name)[1]

    def get_video_no(self):
        return self.video_no

    def get_detail_url(self):
        return self.detail_url

    def get_poster_url(self):
        return self.poster_url

    def get_fanart_url(self):
        return self.fanart_url

    def get_movie_url(self):
        return self.movie_url

    def get_poster_ext(self):
        return self.poster_ext

    def get_fanart_ext(self):
        return self.fanart_ext

    def get_movie_ext(self):
        return self.movie_ext

    def download_poster(self):
        return http_util.download(self.poster_url)

    def download_fanart(self):
        return http_util.download(self.fanart_url)

    def download_movie(self):
        return http_util.download(self.movie_url)


def get_movie_url(detail_soup):
    sample_token = detail_soup.find('div', class_="detail_data").find('a', class_='button_sample')['href'].split(
        '/sampleplayer/sampleplayer.html/')[1]

    sample_url = 'https://www.mgstage.com/sampleplayer/sampleRespons.php?pid={token}'.format(token=sample_token)
    sample_html = http_util.get(sample_url, age_check_headers)
    sample_json = json.loads(sample_html)
    return sample_json['url'].split('.ism')[0] + '.mp4'


def search_actress(video_no):
    detail_url = 'https://www.mgstage.com/product/product_detail/{video_no}/'.format(video_no=video_no)
    detail_html = http_util.get(detail_url, age_check_headers)
    detail_soup = BeautifulSoup(detail_html, features="html.parser")

    # actress
    actress_td = detail_soup.body.find(text='出演：').parent.find_next_sibling('td')
    if actress_td is None:
        videos = []
        return videos

    actress_url = actress_td.find('a')['href']
    return search_videos(actress_url)


def search_series(video_no):
    detail_url = 'https://www.prestige-av.com/goods/goods_detail.php?sku={video_no}'.format(video_no=video_no)
    detail_html = http_util.get(detail_url, age_check_headers)
    detail_soup = BeautifulSoup(detail_html, features="html.parser")

    # series_p
    series_a = detail_soup.body.find(text='メーカー：').parent.find_next_sibling('td')
    if series_a is None:
        videos = []
        return videos

    series_url = series_a['href']
    return search_videos(series_url)


def search_videos(search_url):
    search_url = site_url.rstrip('/') + search_url + '&sort=new&list_cnt=120'
    search_html = http_util.get(search_url, headers=age_check_headers)
    search_soup = BeautifulSoup(search_html, 'html.parser')

    li_list = search_soup.find('div', class_='search_list').find('ul').find_all('li')
    print('video数量: ' + str(len(li_list)))

    # 查询video列表
    videos = []
    for li in reversed(li_list):
        # detail
        detail_url = site_url.rstrip('/') + li.find('a')['href']
        print(detail_url)
        detail_html = http_util.get(detail_url, age_check_headers)
        detail_soup = BeautifulSoup(detail_html, features="html.parser")

        # video_no
        video_no = detail_url.split('product_detail/')[1].lstrip('/')
        print('(' + video_no + ')[' + detail_url + ']')

        # fanart
        fanart_url = detail_soup.find('div', class_="detail_data").find('a', class_='link_magnify')['href']
        print(fanart_url)

        # poster
        poster_url = fanart_url.replace('pb', 'pf')
        print(poster_url)

        # movie
        movie_url = get_movie_url(detail_soup)
        print(movie_url)

        video = {'number': video_no, 'url': detail_url,
                 'poster_url': poster_url, 'fanart_url': fanart_url, 'movie_url': movie_url}
        videos.append(video)

    return videos


if __name__ == '__main__':
    # https://www.mgstage.com/product/product_detail/259LUXU-1033/
    # mgs = MGS('SIRO-4989')
    # mgs = MGS('200GANA-2789')
    mgs = MGS('259LUXU-1033')

    print(mgs.get_poster_url())
    print(mgs.get_fanart_url())
    print(mgs.get_movie_url())

    print(mgs.get_poster_ext())
    print(mgs.get_fanart_ext())
    print(mgs.get_movie_ext())

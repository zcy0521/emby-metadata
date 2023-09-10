#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import json
import os

from bs4 import BeautifulSoup

from utils import http_util

site_url = 'https://www.prestige-av.com/'

# 年龄检查cookie
age_check_headers = {'cookie': '__age_auth__=true'}


class Prestige(object):
    def __init__(self, video_no):
        # 番号
        self.video_no = video_no

        # 详情页
        self.detail_url = 'https://www.prestige-av.com/goods/goods_detail.php?sku={video_no}'.format(video_no=video_no)
        detail_html = http_util.get(self.detail_url, age_check_headers)
        detail_soup = BeautifulSoup(detail_html, features="html.parser")

        print(detail_soup)

        # poster
        poster_url = detail_soup.find('div', class_="c-ratio-image").find('img')['src']
        self.poster_url = poster_url.split('?')[0]
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # fanart
        self.fanart_url = self.poster_url.replace('pf_', 'pb_')
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

        # movie
        movie_url = 'https://www.prestige-av.com/api/media/movie/{number}.mp4'
        self.movie_url = movie_url.format(number=video_no)
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


def search_actress(video_no):
    # 详情页
    detail_url = 'https://www.prestige-av.com/goods/goods_detail.php?sku={video_no}'.format(video_no=video_no)
    detail_html = http_util.get(detail_url, age_check_headers)
    detail_soup = BeautifulSoup(detail_html, features="html.parser")

    # actress
    actress_p = detail_soup.body.find(text='出演者').parent.find_next_sibling('p')
    if actress_p is None:
        videos = []
        return videos

    actress_url = actress_p.find('a')['href']
    actress = actress_url.split('actress=')[1]
    return search_videos('actress', actress)


def search_series(video_no):
    # 详情页
    detail_url = 'https://www.prestige-av.com/goods/goods_detail.php?sku={video_no}'.format(video_no=video_no)
    detail_html = http_util.get(detail_url, age_check_headers)
    detail_soup = BeautifulSoup(detail_html, features="html.parser")

    # series_p
    series_a = detail_soup.body.find(text='シリーズ').parent.find_next_sibling('a')
    if series_a is None:
        videos = []
        return videos

    series_url = series_a['href']
    series = series_url.split('series=')[1]
    return search_videos('series', series)


def search_videos(search_type, search_key):
    search_url = 'https://www.prestige-av.com/api/search?isEnabledQuery=true&isEnableAggregation=false&{search_type}[]={search_key}&release=false&reservation=false&soldOut=false&order=new&aggregationTermsSize=0&from={index}&size={size}'.format(
        search_type=search_type, search_key=search_key, index=0, size=20)
    search_html = http_util.get(search_url, age_check_headers)
    search_json = json.loads(search_html)

    hits = search_json['hits']['hits']
    print('video数量: ' + str(len(hits)))

    # 查询video列表
    videos = []
    for hit in hits:
        uuid = hit['_source']['productUuid']
        item_id = hit['_source']['deliveryItemId']

        # detail
        detail_url = 'https://www.prestige-av.com/goods/{uuid}?skuId={item_id}'.format(uuid=uuid, item_id=item_id)
        print(detail_url)
        detail_html = http_util.get(detail_url, age_check_headers)
        detail_soup = BeautifulSoup(detail_html, features="html.parser")

        # video_no
        video_no = item_id
        print('(' + video_no + ')[' + detail_url + ']')

        # poster
        poster_url = detail_soup.find('div', class_="c-ratio-image").find('img')['src']
        poster_url = poster_url.split('?')[0]
        print(poster_url)

        # fanart
        fanart_url = poster_url.replace('pf_', 'pb_')
        print(fanart_url)

        # movie
        movie_url = 'https://www.prestige-av.com/api/media/movie/{number}.mp4'
        movie_url = movie_url.format(number=item_id)
        print(movie_url)

        video = {'number': item_id, 'url': detail_url,
                 'poster_url': poster_url, 'fanart_url': fanart_url, 'movie_url': movie_url}
        videos.append(video)

    return videos


if __name__ == '__main__':
    # https://www.prestige-av.com/goods/goods_detail.php?sku=ABP-721
    # https://www.prestige-av.com/goods/goods_detail.php?sku=AOI-005
    # https://www.prestige-av.com/goods/goods_detail.php?sku=DOM-045
    # https://www.prestige-av.com/goods/goods_detail.php?sku=EDD-202
    # https://www.prestige-av.com/goods/goods_detail.php?sku=INU-050
    # https://www.prestige-av.com/goods/goods_detail.php?sku=JBS-028
    # https://www.prestige-av.com/goods/goods_detail.php?sku=JOB-033
    # https://www.prestige-av.com/goods/goods_detail.php?sku=PPT-046
    # https://www.prestige-av.com/goods/goods_detail.php?sku=SGA-092
    # https://www.prestige-av.com/goods/goods_detail.php?sku=WAT-001
    prestige = Prestige('ABP-721')

    print(prestige.get_poster_url())
    print(prestige.get_fanart_url())
    print(prestige.get_movie_url())

    print(prestige.get_poster_ext())
    print(prestige.get_fanart_ext())
    print(prestige.get_movie_ext())

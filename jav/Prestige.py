#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import json

from bs4 import BeautifulSoup

from utils import http_util


class Prestige(object):
    # 官网
    SITE_URL = 'https://www.prestige-av.com/'
    DETAIL_URL = 'https://www.prestige-av.com/goods/goods_detail.php?sku={video_no}'
    VIDEO_URL = 'https://www.prestige-av.com/api/media/movie/{number}.mp4'

    AGE_CHECK_HEADERS = {'cookie': '__age_auth__=true'}

    def __init__(self, video_no):
        # 番号
        self.video_no = video_no

        # 详情页
        self.detail_url = Prestige.DETAIL_URL.format(video_no=video_no)
        detail_html = http_util.get(self.detail_url, Prestige.AGE_CHECK_HEADERS)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        poster_url = self.detail_soup.find('div', class_="c-ratio-image").find('img')['src']
        return poster_url.split('?')[0]

    def get_backdrop_url(self):
        return self.get_poster_url().replace('pf_', 'pb_')

    def get_trailer_url(self):
        return Prestige.VIDEO_URL.format(number=self.video_no)

    @classmethod
    def search_actress(cls, video_no):
        # 详情页
        detail_url = cls.DETAIL_URL.format(video_no=video_no.upper())
        detail_html = http_util.get(detail_url, cls.AGE_CHECK_HEADERS)
        detail_soup = BeautifulSoup(detail_html, features="html.parser")

        # actress
        actress_p = detail_soup.body.find(text='出演者').parent.find_next_sibling('p')
        if actress_p is None:
            items = []
            return items

        actress_url = actress_p.find('a')['href']
        actress = actress_url.split('actress=')[1]
        return cls.search_items('actress', actress)

    @classmethod
    def search_series(cls, video_no):
        # 详情页
        detail_url = cls.DETAIL_URL.format(video_no=video_no.upper())
        detail_html = http_util.get(detail_url, cls.AGE_CHECK_HEADERS)
        detail_soup = BeautifulSoup(detail_html, features="html.parser")

        # series_p
        series_a = detail_soup.body.find(text='シリーズ').parent.find_next_sibling('a')
        if series_a is None:
            items = []
            return items

        series_url = series_a['href']
        series = series_url.split('series=')[1]
        return cls.search_items('series', series)

    @classmethod
    def search_items(cls, search_type, search_key):
        search_url = 'https://www.prestige-av.com/api/search?isEnabledQuery=true&isEnableAggregation=false&{search_type}[]={search_key}&release=false&reservation=false&soldOut=false&order=new&aggregationTermsSize=0&from={index}&size={size}'.format(search_type=search_type, search_key=search_key, index=0, size=20)
        search_html = http_util.get(search_url, cls.AGE_CHECK_HEADERS)
        search_json = json.loads(search_html)

        hits = search_json['hits']['hits']
        print('video数量: ' + str(len(hits)))

        # 查询video列表
        items = []
        for hit in hits:
            uuid = hit['_source']['productUuid']
            item_id = hit['_source']['deliveryItemId']

            # 页面详情页
            goods_url = 'https://www.prestige-av.com/goods/{uuid}?skuId={item_id}'.format(uuid=uuid, item_id=item_id)
            goods_html = http_util.get(goods_url, cls.AGE_CHECK_HEADERS)
            goods_soup = BeautifulSoup(goods_html, features="html.parser")

            # 封面
            poster_url = goods_soup.find('div', class_="c-ratio-image").find('img')['src']
            poster_url = poster_url.split('?')[0]

            # 背景图
            backdrop_url = poster_url.replace('pf_', 'pb_')

            # 预告片
            trailer_url = cls.VIDEO_URL.format(number=item_id)

            item = {'video_no': item_id, 'detail_url': goods_url, 'poster_url': poster_url, 'backdrop_url': backdrop_url, 'trailer_url': trailer_url}
            items.append(item)

        return items


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
    print(prestige.get_backdrop_url())
    print(prestige.get_trailer_url())

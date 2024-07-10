#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import json
import sys

from bs4 import BeautifulSoup

from utils import http_util


class Fanza(object):
    # 官网
    SITE_URL = 'https://www.dmm.co.jp'
    SEARCH_URL = 'https://www.dmm.co.jp/digital/-/list/search/=/?searchstr={search_key}'

    AGE_CHECK_HEADERS = {'cookie': 'age_check_done=1'}

    def __init__(self, video_no):
        self.video_no = video_no

        # 查询列表页
        list_url = Fanza.SEARCH_URL.format(search_key=video_no.lower().replace('-', '00'))
        list_html = http_util.get(list_url, Fanza.AGE_CHECK_HEADERS)
        self.list_soup = BeautifulSoup(list_html, features="html.parser")

        # 详情页
        self.detail_url = self.list_soup.find('ul', id='list').find_all('li')[0].find('a')['href']
        detail_html = http_util.get(self.detail_url, Fanza.AGE_CHECK_HEADERS)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        return self.detail_soup.find('div', id='sample-video').find('a').find('img')['src']

    def get_backdrop_url(self):
        return self.detail_soup.find('div', id='sample-video').find('a')['href']

    def get_trailer_url(self):
        return Fanza.get_video_url(self.detail_soup)

    @classmethod
    def get_video_url(cls, detail_soup):
        ajax_div = detail_soup.find('div', id='detail-sample-movie')
        if ajax_div is None:
            return None

        ajax_url = ajax_div.find('a', class_='d-btn')['onclick']
        ajax_url = cls.SITE_URL + ajax_url.split('\'')[1]
        ajax_html = http_util.get(ajax_url, headers=cls.AGE_CHECK_HEADERS)
        ajax_soup = BeautifulSoup(ajax_html, 'html.parser')

        # trailer iframe
        iframe_url = ajax_soup.find('iframe', id='DMMSample_player_now')['src']
        iframe_html = http_util.get(iframe_url, headers=cls.AGE_CHECK_HEADERS)
        iframe_soup = BeautifulSoup(iframe_html, 'html.parser')

        # trailer
        iframe_script = iframe_soup.find_all('script')[-4].text
        iframe_args = iframe_script.split('const args = ')[1].rstrip().rstrip(';')
        args_json = json.loads(iframe_args)
        return 'https:' + args_json['src']

    @classmethod
    def search_actress(cls, search_key):
        # search
        search_url = cls.SEARCH_URL.format(search_key=search_key)
        search_html = http_util.get(search_url, headers=cls.AGE_CHECK_HEADERS)
        search_soup = BeautifulSoup(search_html, 'html.parser')

        # item
        item_url = search_soup.find('ul', id='list').find_all('li')[0].find('a')['href']
        item_html = http_util.get(item_url, headers=cls.AGE_CHECK_HEADERS)
        item_soup = BeautifulSoup(item_html, 'html.parser')

        # actress
        actress_url = item_soup.find('span', id='performer').find('a')['href']
        return cls.search_items(actress_url)


    @classmethod
    def search_series(cls, search_key):
        # search
        search_url = cls.SEARCH_URL.format(search_key=search_key)
        search_html = http_util.get(search_url, headers=cls.AGE_CHECK_HEADERS)
        search_soup = BeautifulSoup(search_html, 'html.parser')

        # item
        item_url = search_soup.find('ul', id='list').find_all('li')[0].find('a')['href']
        item_html = http_util.get(item_url, headers=cls.AGE_CHECK_HEADERS)
        item_soup = BeautifulSoup(item_html, 'html.parser')

        # series
        series_url = item_soup.find('div', class_='page-detail').find('table').find('table').find_all('tr')[7].find_all('td')[1].find('a')['href']
        return cls.search_items(series_url)

    @classmethod
    def search_items(cls, search_url):
        search_url = cls.SITE_URL + search_url + '&sort=date'
        search_html = http_util.get(search_url, headers=cls.AGE_CHECK_HEADERS)
        search_soup = BeautifulSoup(search_html, 'html.parser')

        li_list = search_soup.find('ul', id='list').find_all('li')
        print('video数量: ' + str(len(li_list)))

        # 查询列表
        items = []
        for li in reversed(li_list):
            # detail
            detail_url = li.find('a')['href']
            detail_html = http_util.get(detail_url, headers=Fanza.AGE_CHECK_HEADERS)
            detail_soup = BeautifulSoup(detail_html, 'html.parser')

            # video_no
            video_no = detail_url.split('cid=')[1].rstrip('/')

            # poster
            poster_url = detail_soup.find('div', id='sample-video').find('img')['src']

            # backdrop
            backdrop_url = detail_soup.find('div', id='sample-video').find('a')['href']

            # trailer
            trailer_url = cls.get_video_url(detail_soup)
            if trailer_url:
                item = {'video_no': video_no, 'detail_url': detail_url, 'poster_url': poster_url, 'backdrop_url': backdrop_url, 'trailer_url': trailer_url}
            else:
                item = {'video_no': video_no, 'detail_url': detail_url, 'poster_url': poster_url, 'backdrop_url': backdrop_url}
            items.append(item)

        return items


if __name__ == '__main__':
    # https://www.dmm.co.jp/digital/videoa/-/detail/=/cid=alb00219/
    fanza = Fanza('ALB-219')
    print(fanza.get_poster_url())
    print(fanza.get_backdrop_url())
    print(fanza.get_trailer_url())

    # https://www.dmm.co.jp/digital/videoa/-/detail/=/cid=stars00212/
    sod = Fanza('STARS-212')
    print(sod.get_poster_url())
    print(sod.get_backdrop_url())
    print(sod.get_trailer_url())

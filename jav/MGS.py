#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import json

from bs4 import BeautifulSoup

from utils import http_util


class MGS(object):
    # 官网
    SITE_URL = 'https://www.mgstage.com'
    DETAIL_URL = 'https://www.mgstage.com/product/product_detail/{video_no}/'
    VIDEO_URL = 'https://www.mgstage.com/sampleplayer/sampleRespons.php?pid={token}'

    # 年龄检查cookie
    AGE_CHECK_HEADERS = {'Cookie': 'adc=1'}

    def __init__(self, video_no):
        self.video_no = video_no

        # 详情页
        detail_url = MGS.DETAIL_URL.format(video_no=video_no)
        detail_html = http_util.get(detail_url, MGS.AGE_CHECK_HEADERS)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        return self.get_backdrop_url().replace('pb', 'pf')

    def get_backdrop_url(self):
        return self.detail_soup.find('div', class_="detail_data").find('a', class_='link_magnify')['href']

    def get_trailer_url(self):
        return MGS.get_video_url(self.detail_soup)

    @classmethod
    def get_video_url(cls, detail_soup):
        token = detail_soup.find('div', class_="detail_data").find('a', class_='button_sample')['href'].split('/sampleplayer/sampleplayer.html/')[1]
        video_url = cls.VIDEO_URL.format(token=token)
        video_html = http_util.get(video_url, cls.AGE_CHECK_HEADERS)
        video_json = json.loads(video_html)
        return video_json['url'].split('.ism')[0] + '.mp4'

    @classmethod
    def search_actress(cls, video_no):
        detail_url = cls.DETAIL_URL.format(video_no=video_no)
        detail_html = http_util.get(detail_url, cls.AGE_CHECK_HEADERS)
        detail_soup = BeautifulSoup(detail_html, features="html.parser")

        # actress
        actress_td = detail_soup.body.find(text='出演：').parent.find_next_sibling('td')
        if actress_td is None:
            videos = []
            return videos

        actress_url = actress_td.find('a')['href']
        return cls.search_items(actress_url)

    @classmethod
    def search_series(cls, video_no):
        detail_url = cls.DETAIL_URL.format(video_no=video_no)
        detail_html = http_util.get(detail_url, cls.AGE_CHECK_HEADERS)
        detail_soup = BeautifulSoup(detail_html, features="html.parser")

        # series_p
        series_a = detail_soup.body.find(text='メーカー：').parent.find_next_sibling('td')
        if series_a is None:
            videos = []
            return videos

        series_url = series_a['href']
        return cls.search_items(series_url)

    @classmethod
    def search_items(cls, search_url):
        search_url = cls.SITE_URL + search_url + '&sort=new&list_cnt=120'
        search_html = http_util.get(search_url, headers=cls.AGE_CHECK_HEADERS)
        search_soup = BeautifulSoup(search_html, 'html.parser')

        li_list = search_soup.find('div', class_='search_list').find('ul').find_all('li')
        print('video数量: ' + str(len(li_list)))

        # 查询video列表
        videos = []
        for li in reversed(li_list):
            # detail
            detail_url = cls.SITE_URL + li.find('a')['href']
            print(detail_url)
            detail_html = http_util.get(detail_url, cls.AGE_CHECK_HEADERS)
            detail_soup = BeautifulSoup(detail_html, features="html.parser")

            # video_no
            video_no = detail_url.split('product_detail/')[1].lstrip('/')
            print('(' + video_no + ')[' + detail_url + ']')

            # backdrop
            backdrop_url = detail_soup.find('div', class_="detail_data").find('a', class_='link_magnify')['href']
            print(backdrop_url)

            # poster
            poster_url = backdrop_url.replace('pb', 'pf')
            print(poster_url)

            # trailer
            trailer_url = cls.get_video_url(detail_soup)
            print(trailer_url)

            video = {'number': video_no, 'url': detail_url, 'poster_url': poster_url, 'backdrop_url': backdrop_url, 'trailer_url': trailer_url}
            videos.append(video)

        return videos


if __name__ == '__main__':
    # https://www.mgstage.com/product/product_detail/259LUXU-1033/
    # mgs = MGS('SIRO-4989')
    # mgs = MGS('200GANA-2789')
    mgs = MGS('413INST-168')
    print(mgs.get_poster_url())
    print(mgs.get_backdrop_url())
    print(mgs.get_trailer_url())

    # https://www.mgstage.com/product/product_detail/107STARS-212
    sod = MGS('107STARS-212')
    print(sod.get_poster_url())
    print(sod.get_backdrop_url())
    print(sod.get_trailer_url())

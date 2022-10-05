import json
import os

from bs4 import BeautifulSoup

from utils import http_util

site_url = 'https://www.dmm.co.jp'
age_check_headers = {'cookie': 'age_check_done=1'}


class FANZA(object):
    def __init__(self, video_no):
        # 番号
        self.video_no = video_no

        # 查询页
        list_url = 'https://www.dmm.co.jp/digital/-/list/search/=/?searchstr={video_no}'.format(
            video_no=video_no.lower().replace('-', '00'))
        list_html = http_util.get(list_url, age_check_headers)
        list_soup = BeautifulSoup(list_html, features="html.parser")

        # 请求dmm 年龄认证Cookie
        self.detail_url = list_soup.find('ul', id='list').find_all('li')[0].find('a')['href']
        detail_html = http_util.get(self.detail_url, age_check_headers)
        detail_soup = BeautifulSoup(detail_html, features="html.parser")

        # poster
        self.poster_url = detail_soup.find('div', id='sample-video').find('a').find('img')['src']
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # fanart
        self.fanart_url = detail_soup.find('div', id='sample-video').find('a')['href']
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

        # ajax_url
        ajax_url = detail_soup.find('div', id='detail-sample-movie').find('a')['onclick']
        ajax_url = site_url + ajax_url.split('\'')[1]
        ajax_html = http_util.get(ajax_url, age_check_headers)
        ajax_soup = BeautifulSoup(ajax_html, features="html.parser")

        # iframe_url
        iframe_url = ajax_soup.find('iframe', id='DMMSample_player_now')['src']
        iframe_html = http_util.get(iframe_url, age_check_headers)
        iframe_soup = BeautifulSoup(iframe_html, features="html.parser")

        # iframe_script str.rstrip()删除最右侧空格
        iframe_script = iframe_soup.find_all('script')[-4].text
        iframe_args = iframe_script.split('const args = ')[1].rstrip().rstrip(';')
        args_json = json.loads(iframe_args)

        # movie
        self.movie_url = 'https:' + args_json['src']
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


def get_movie_url(video_no):
    # 查询页
    list_url = 'https://www.dmm.co.jp/digital/-/list/search/=/?searchstr={video_no}'.format(
        video_no=video_no.lower().replace('-', '00'))
    list_html = http_util.get(list_url, age_check_headers)
    list_soup = BeautifulSoup(list_html, features="html.parser")

    # 请求dmm 年龄认证Cookie
    detail_url = list_soup.find('ul', id='list').find_all('li')[0].find('a')['href']
    detail_html = http_util.get(detail_url, age_check_headers)
    detail_soup = BeautifulSoup(detail_html, features="html.parser")

    # ajax_url
    ajax_url = detail_soup.find('div', id='detail-sample-movie').find('a')['onclick']
    ajax_url = site_url + ajax_url.split('\'')[1]
    ajax_html = http_util.get(ajax_url, age_check_headers)
    ajax_soup = BeautifulSoup(ajax_html, features="html.parser")

    # iframe_url
    iframe_url = ajax_soup.find('iframe', id='DMMSample_player_now')['src']
    iframe_html = http_util.get(iframe_url, age_check_headers)
    iframe_soup = BeautifulSoup(iframe_html, features="html.parser")

    # iframe_script
    iframe_script = iframe_soup.find_all('script')[-4].text
    iframe_args = iframe_script.split('const args = ')[1].rstrip().rstrip(';')
    args_json = json.loads(iframe_args)
    return 'https:' + args_json['src']


def search_actress(search_key):
    # search
    search_url = 'https://www.dmm.co.jp/digital/-/list/search/=/?searchstr={search_key}'.format(search_key=search_key)
    search_html = http_util.get(search_url, headers=age_check_headers)
    search_soup = BeautifulSoup(search_html, 'html.parser')

    # item
    item_url = search_soup.find('ul', id='list').find('li').find('a')['href']
    item_html = http_util.get(item_url, headers=age_check_headers)
    item_soup = BeautifulSoup(item_html, 'html.parser')

    # actress
    actress_url = item_soup.find('span', id='performer').find('a')['href']
    return search_videos(actress_url)


def search_series(search_key):
    # search
    search_url = 'https://www.dmm.co.jp/digital/-/list/search/=/?searchstr={search_key}'.format(search_key=search_key)
    search_html = http_util.get(search_url, headers=age_check_headers)
    search_soup = BeautifulSoup(search_html, 'html.parser')

    # item
    item_url = search_soup.find('ul', id='list').find('li').find('a')['href']
    item_html = http_util.get(item_url, headers=age_check_headers)
    item_soup = BeautifulSoup(item_html, 'html.parser')

    # series
    series_url = item_soup.find('div', class_='page-detail').find('table').find('table').find_all('tr')[7].find_all('td')[1].find('a')['href']
    return search_videos(series_url)


def search_videos(search_url):
    search_url = site_url + search_url + 'sort=date/'
    search_html = http_util.get(search_url, headers=age_check_headers)
    search_soup = BeautifulSoup(search_html, 'html.parser')

    li_list = search_soup.find('ul', id='list').find_all('li')
    print('video数量: ' + str(len(li_list)))

    # 查询video列表
    videos = []
    for li in reversed(li_list):
        # detail
        detail_url = li.find('a')['href']
        detail_html = http_util.get(detail_url, headers=age_check_headers)
        detail_soup = BeautifulSoup(detail_html, 'html.parser')

        # video_no
        print(detail_url.split('cid=')[1])
        video_no = detail_url.split('cid=')[1].rstrip('/')
        print('(' + video_no + ')[' + detail_url + ']')

        # poster
        poster_url = detail_soup.find('div', id='sample-video').find('img')['src']
        print(poster_url)

        # fanart
        fanart_url = detail_soup.find('div', id='sample-video').find('a')['href']
        print(fanart_url)

        # movie ajax
        ajax_div = detail_soup.find('div', id='detail-sample-movie')
        if ajax_div is None:
            video = {'number': video_no, 'url': detail_url,
                     'poster_url': poster_url, 'fanart_url': fanart_url}
            videos.append(video)
            continue

        ajax_url = detail_soup.find('div', id='detail-sample-movie').find('a', class_='d-btn')['onclick']
        ajax_url = 'https://www.dmm.co.jp' + ajax_url.split('\'')[1]
        ajax_html = http_util.get(ajax_url, headers=age_check_headers)
        ajax_soup = BeautifulSoup(ajax_html, 'html.parser')

        # movie iframe
        iframe_url = ajax_soup.find('iframe', id='DMMSample_player_now')['src']
        iframe_html = http_util.get(iframe_url, headers=age_check_headers)
        # euc-jp
        iframe_soup = BeautifulSoup(iframe_html, 'html.parser')
        # print(iframe_soup)

        # movie
        iframe_script = iframe_soup.find_all('script')[-4].text
        iframe_args = iframe_script.split('const args = ')[1].rstrip().rstrip(';')
        args_json = json.loads(iframe_args)
        movie_url = 'https:' + args_json['src']
        print(movie_url)

        video = {'number': video_no, 'url': detail_url,
                 'poster_url': poster_url, 'fanart_url': fanart_url, 'movie_url': movie_url}
        videos.append(video)

    return videos


if __name__ == '__main__':
    # https://www.dmm.co.jp/digital/videoa/-/detail/=/cid=alb00219/
    fanza = FANZA('ALB-219')

    print(fanza.get_poster_url())
    print(fanza.get_fanart_url())
    print(fanza.get_movie_url())

    print(fanza.get_poster_ext())
    print(fanza.get_fanart_ext())
    print(fanza.get_movie_ext())

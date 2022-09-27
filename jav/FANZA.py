import json
import os

from bs4 import BeautifulSoup

from utils import http

site_url = 'https://www.dmm.co.jp'
age_check_headers = {'cookie': 'age_check_done=1'}


class FANZA(object):
    def __init__(self, video_no):
        # 番号
        self.video_no = video_no

        # 详情页
        url = 'https://www.dmm.co.jp/digital/videoa/-/detail/=/cid={video_no}/'.format(
            video_no=video_no.lower().replace('-', '00'))
        html = http.get(url, age_check_headers)
        soup = BeautifulSoup(html, features="html.parser")

        # poster
        self.poster_url = soup.find('div', id='sample-video').find('a').find('img')['src']
        self.poster_name = os.path.basename(self.poster_url)
        self.poster_ext = os.path.splitext(self.poster_name)[1]

        # fanart
        self.fanart_url = soup.find('div', id='sample-video').find('a')['href']
        self.fanart_name = os.path.basename(self.fanart_url)
        self.fanart_ext = os.path.splitext(self.fanart_name)[1]

        # movie
        self.movie_url = get_movie_by_detail_url(url)
        self.movie_name = os.path.basename(self.movie_url)
        self.movie_ext = os.path.splitext(self.movie_name)[1]

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
        return http.download(self.poster_url)

    def download_fanart(self):
        return http.download(self.fanart_url)

    def download_movie(self):
        return http.download(self.movie_url)


def get_movie_by_detail_url(detail_url):
    # 请求dmm 年龄认证Cookie
    detail_html = http.get(detail_url, age_check_headers)
    detail_soup = BeautifulSoup(detail_html, features="html.parser")

    # ajax_url
    ajax_url = detail_soup.find('div', id='detail-sample-movie').find('a')['onclick']
    ajax_url = site_url + ajax_url.split('\'')[1]
    ajax_html = http.get(ajax_url, age_check_headers)
    ajax_soup = BeautifulSoup(ajax_html, features="html.parser")

    # iframe_url
    iframe_url = ajax_soup.find('iframe', id='DMMSample_player_now')['src']
    iframe_html = http.get(iframe_url, age_check_headers)
    iframe_soup = BeautifulSoup(iframe_html, features="html.parser")

    # iframe_script
    iframe_script = iframe_soup.find_all('script')[-4].text
    iframe_args = iframe_script.split('const args = ')[1].replace(';', '')
    args_json = json.loads(iframe_args)
    return 'https:' + args_json['src']


def get_movie_by_video_no(video_no):
    # 查询与
    list_url = 'https://www.dmm.co.jp/digital/-/list/search/=/?searchstr={video_no}'.format(
        video_no=video_no.lower().replace('-', '00'))
    list_html = http.get(list_url, age_check_headers)
    list_soup = BeautifulSoup(list_html, features="html.parser")

    # 请求dmm 年龄认证Cookie
    detail_url = list_soup.find('ul', id='list').find_all('li')[0].find('a')['href']
    detail_html = http.get(detail_url, age_check_headers)
    detail_soup = BeautifulSoup(detail_html, features="html.parser")

    # ajax_url
    ajax_url = detail_soup.find('div', id='detail-sample-movie').find('a')['onclick']
    ajax_url = site_url + ajax_url.split('\'')[1]
    ajax_html = http.get(ajax_url, age_check_headers)
    ajax_soup = BeautifulSoup(ajax_html, features="html.parser")

    # iframe_url
    iframe_url = ajax_soup.find('iframe', id='DMMSample_player_now')['src']
    iframe_html = http.get(iframe_url, age_check_headers)
    iframe_soup = BeautifulSoup(iframe_html, features="html.parser")

    # iframe_script
    iframe_script = iframe_soup.find_all('script')[-4].text
    iframe_args = iframe_script.split('const args = ')[1].replace(';', '')
    args_json = json.loads(iframe_args)
    return 'https:' + args_json['src']


if __name__ == '__main__':
    # https://www.dmm.co.jp/digital/videoa/-/detail/=/cid=alb00219/
    fanza = FANZA('ALB-219')

    print(fanza.get_poster_url())
    print(fanza.get_fanart_url())
    print(fanza.get_movie_url())

    print(fanza.get_poster_ext())
    print(fanza.get_fanart_ext())
    print(fanza.get_movie_ext())

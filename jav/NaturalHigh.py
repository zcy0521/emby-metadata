#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup


class NaturalHigh(object):
    site_url = 'https://www.naturalhigh.co.jp/'

    def __init__(self, video_no):
        self.video_no = video_no = video_no.lower()
        self.url = url = 'https://www.naturalhigh.co.jp/all/' + video_no + '/'
        print(url)

        self.session = session = requests.Session()

        # 年龄检查
        data = {
            'age_gate': '1',
            'age_gate[age]': 'TVRnPQ==',
            'action': 'age_gate_submit',
            'age_gate[nonce]': '7d70b59573',
            '_wp_http_referer': '/all/shn-016/',
            'confirm_action': '0'
        }
        age_check_headers = {
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Accept-Language': 'en-US,en;q=0.9',
            # 'Cache-Control': 'max-age=0',
            # 'Connection': 'keep-alive',
            # 'Content-Length': '162',
            # 'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': '_ga=GA1.3.488997533.1609657427; _gid=GA1.3.1979187914.1609657427; _gat=1',
            'Host': 'www.naturalhigh.co.jp',
            'Origin': 'https://www.naturalhigh.co.jp',
            'Referer': 'https://www.naturalhigh.co.jp/all/shn-016/',
            # 'Sec-Fetch-Dest': 'document',
            # 'Sec-Fetch-Mode': 'navigate',
            # 'Sec-Fetch-Site': 'same-origin',
            # 'Sec-Fetch-User': '?1',
            # 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        session.post('https://www.naturalhigh.co.jp/wp-admin/admin-post.php', data=data, headers=age_check_headers)

        # 视频详情页html
        headers = {
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Accept-Language': 'en-US,en;q=0.9',
            # 'Cache-Control': 'max-age=0',
            # 'Connection': 'keep-alive',
            'Cookie': '_ga=GA1.3.488997533.1609657427; _gid=GA1.3.1979187914.1609657427; _gat=1; age_gate=18',
            'Host': 'www.naturalhigh.co.jp',
            'Referer': 'https://www.naturalhigh.co.jp/all/shn-016/',
            # 'Sec-Fetch-Dest': 'document',
            # 'Sec-Fetch-Mode': 'navigate',
            # 'Sec-Fetch-Site': 'same-origin',
            # 'Sec-Fetch-User': '?1',
            # 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        response = session.get(url, headers=headers)
        html = response.text
        print(html)

        # BeautifulSoup https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/
        # pip install beautifulsoup4
        soup = BeautifulSoup(html, features="html.parser")

        # poster
        # self.poster_url = soup.find('img', class_="sam160")['src']

        # fanart
        # self.fanart_url = soup.find('a', class_="popup-image")['href']

    def download_poster(self):
        response = self.session.get(self.poster_url, headers=self.headers)
        return response.content

    def download_fanart(self):
        response = self.session.get(self.fanart_url, headers=self.headers)
        return response.content


if __name__ == '__main__':
    # https://www.naturalhigh.co.jp/all/shn-016/
    natural_high = NaturalHigh('SHN-016')

    # print(natural_high.poster_url)
    # print(natural_high.fanart_url)

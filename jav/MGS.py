#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup


class MGS(object):
    site_url = 'https://www.mgstage.com/'
    siro_poster_url = 'https://image.mgstage.com/images/shirouto/siro/{number}/pf_t1_siro-{number}.jpg'
    siro_fanart_url = 'https://image.mgstage.com/images/shirouto/siro/{number}/pb_e_siro-{number}.jpg'
    gana_poster_url = 'https://image.mgstage.com/images/nanpatv/200gana/{number}/pf_t1_200gana-{number}.jpg'
    gana_fanart_url = 'https://image.mgstage.com/images/nanpatv/200gana/{number}/pb_e_200gana-{number}.jpg'

    def __init__(self, video_no):
        self.video_no = video_no
        self.url = url = 'https://www.mgstage.com/product/product_detail/' + video_no + '/'

        self.session = session = requests.Session()
        self.headers = headers = {
            'Referer': url,
            'Cookie': 'coc=1; adc=1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

        # 视频详情页html
        response = session.get(url, headers=headers)
        html = response.text

        # BeautifulSoup https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/
        # pip install beautifulsoup4
        soup = BeautifulSoup(html, features="html.parser")

        if video_no.startswith("SIRO"):
            number = video_no.split('-')[1]
            self.poster_url = self.siro_poster_url.format(number=number)
            self.fanart_url = self.siro_fanart_url.format(number=number)
        elif video_no.startswith("200GANA"):
            number = video_no.split('-')[1]
            self.poster_url = self.gana_poster_url.format(number=number)
            self.fanart_url = self.gana_fanart_url.format(number=number)
        else:
            self.poster_url = soup.find('div', class_="detail_photo").find('img', class_='enlarge_image')['src']
            self.fanart_url = soup.find('div', class_="detail_photo").find('a', class_='link_magnify')['href']

    def download_poster(self):
        response = self.session.get(self.poster_url, headers=self.headers)
        return response.content

    def download_fanart(self):
        response = self.session.get(self.fanart_url, headers=self.headers)
        return response.content


if __name__ == '__main__':
    # https://www.mgstage.com/product/product_detail/259LUXU-1033/
    mgs = MGS('SIRO-3577')

    print(mgs.poster_url)
    print(mgs.fanart_url)

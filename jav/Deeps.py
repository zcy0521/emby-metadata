#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

from bs4 import BeautifulSoup

from jav.Fanza import Fanza
from utils import http_util


class Deeps(object):
    # 官网
    SITE_URL = 'https://deeps.net/'
    DETAIL_URL = 'https://deeps.net/product/{video_no}/'

    def __init__(self, video_no):
        self.video_no = video_no

        # 详情页
        detail_url = Deeps.DETAIL_URL.format(video_no=video_no.lower())
        detail_html = http_util.get(detail_url)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        return self.detail_soup.find('div', id='item').find('figure').find_all('img', class_='sp')[0]['src']

    def get_backdrop_url(self):
        return self.detail_soup.find('div', id='item').find('figure').find('img', class_='pc')['src']

    def get_trailer_url(self):
        fanza = Fanza(self.video_no)
        return fanza.get_trailer_url()

    def create_nfo(self, filepath):
        # 创建 XML 结构
        movie = ET.Element("movie")

        # 详情页
        movie_details = self.detail_soup
        print(movie_details)

        # 标题
        title = movie_details.find('h2', class_="p-workPage__title").get_text().strip()
        ET.SubElement(movie, "title").text = title

        # 情节
        plot = movie_details.find('p', class_="p-workPage__text").get_text().strip()
        ET.SubElement(movie, "plot").text = plot

        # thumb 封面图
        poster = ET.SubElement(movie, "thumb")
        poster.set("aspect", "poster")
        poster.text = self.get_poster_url()

        # fanart 背景图
        fanart = ET.SubElement(movie, "fanart")
        thumbs_imgs = movie_details.find('div', class_="swiper-wrapper").find_all('img')
        for thumbs_img in thumbs_imgs:
            ET.SubElement(fanart, "thumb").text = thumbs_img.get('data-src')

        # trailer 预告片
        ET.SubElement(movie, "trailer").text = self.get_trailer_url()

        info_items = movie_details.find('div', class_="p-workPage__table").find_all('div', recursive=False)
        # print(info_items)

        # 女優
        actor_name = info_items[0].find('a').get_text().strip()
        actor_elem = ET.SubElement(movie, "actor")
        ET.SubElement(actor_elem, "name").text = actor_name

        # 発売日
        premiered = info_items[1].find('a').get_text().strip()
        ET.SubElement(movie, "premiered").text = premiered

        # シリーズ 所属系列
        collection_tag = info_items[2].find('a')
        if collection_tag:
            movie_set = ET.SubElement(movie, "set")
            ET.SubElement(movie_set, "name").text = collection_tag.get_text().strip()

        # レーベル 工作室
        studio = info_items[3].find('a').get_text().strip()
        ET.SubElement(movie, "studio").text = studio

        # ジャンル 标签
        tags = info_items[4].find_all('a')
        for tag in tags:
            ET.SubElement(movie, "tag").text = tag.get_text().strip()

        # 品番
        p_tag = info_items[6].find('p')
        p_text = p_tag.get_text()
        span_texts = [span.get_text() for span in p_tag.find_all('span')]
        for span_text in span_texts:
            p_text = p_text.replace(span_text, '')
        ET.SubElement(movie, "code").text = p_text

        # 生成粗略XML字符串
        rough_string = ET.tostring(movie, 'utf-8')

        # 使用minidom进行格式化
        reparsed = minidom.parseString(rough_string)
        pretty_xml_as_string = reparsed.toprettyxml(indent="    ")

        # 写入文件并包括XML声明
        filename = self.video_no + '.nfo'
        nfo_path = os.path.join(filepath, filename)
        with open(nfo_path, "w", encoding="utf-8") as file:
            file.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
            file.write(pretty_xml_as_string.split("?>", 1)[1].strip())


if __name__ == '__main__':
    # https://deeps.net/product/dvrt-024/
    deeps = Deeps('DVRT-024')
    # print(deeps.get_poster_url())
    # print(deeps.get_backdrop_url())
    # print(deeps.get_trailer_url())

    deeps.create_nfo('D:\\JetBrains\\PycharmProjects\\emby-metadata\\nfo')

#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

from bs4 import BeautifulSoup

from jav.Fanza import Fanza
from utils import http_util


class Casanova(object):
    # 官网
    SITE_URL = 'http://casanova-vr.com/'
    DETAIL_URL = 'http://casanova-vr.com/items/detail/{video_no}'

    def __init__(self, video_no):
        self.video_no = video_no

        # 详情页
        detail_url = Casanova.DETAIL_URL.format(video_no=video_no)
        detail_html = http_util.get(detail_url)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        poster_url = self.detail_soup.find('div', class_="img").find('img')['src']
        return poster_url.lstrip('.')

    def get_backdrop_url(self):
        backdrop_url = self.detail_soup.find('div', class_="img").find('img')['src']
        return backdrop_url.lstrip('.')

    def get_trailer_url(self):
        fanza = Fanza(self.video_no)
        return fanza.get_trailer_url()

    def create_nfo(self, filepath):
        # 创建 XML 结构
        movie = ET.Element("movie")

        # 详情页
        movie_details = self.detail_soup
        # print(movie_details)

        # 标题
        title = movie_details.find('div', class_="title-area").find('h2').get_text().strip()
        ET.SubElement(movie, "title").text = title

        # 情节
        plot = movie_details.find('p', class_="explain").get_text().strip()
        ET.SubElement(movie, "plot").text = plot

        # thumb 封面图
        poster = ET.SubElement(movie, "thumb")
        poster.set("aspect", "poster")
        poster.text = self.get_poster_url()

        # fanart 背景图
        fanart = ET.SubElement(movie, "fanart")
        ET.SubElement(fanart, "thumb").text = movie_details.find('div', class_="vr_wrapper clearfix").find('img')['src']
        thumbs_imgs = movie_details.find('div', class_="vr_images clearfix").find_all('img')
        for thumbs_img in thumbs_imgs:
            ET.SubElement(fanart, "thumb").text = thumbs_img.get('src')

        # trailer 预告片
        ET.SubElement(movie, "trailer").text = self.get_trailer_url()

        info_items = movie_details.find('div', class_="info clearfix").find('table').find_all('tr', recursive=False)
        # print(info_items)

        # 出演者
        actor_name = info_items[6].find('a').get_text().strip()
        actor_elem = ET.SubElement(movie, "actor")
        ET.SubElement(actor_elem, "name").text = actor_name

        # 発売日
        premiered = info_items[2].find('td').get_text().strip()
        ET.SubElement(movie, "premiered").text = premiered

        # シリーズ 所属系列
        collection_tag = info_items[4].find('a')
        if collection_tag:
            movie_set = ET.SubElement(movie, "set")
            ET.SubElement(movie_set, "name").text = collection_tag.get_text().strip()

        # ジャンル 标签
        tags = info_items[5].find_all('a')
        for tag in tags:
            ET.SubElement(movie, "tag").text = tag.get_text().strip()

        # 品番
        code = info_items[0].find('td').get_text().strip()
        ET.SubElement(movie, "code").text = code

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
    # http://casanova-vr.com/items/detail/CAFR-001
    casanova = Casanova('CAFR-001')
    # print(casanova.get_poster_url())
    # print(casanova.get_backdrop_url())
    # print(casanova.get_trailer_url())

    casanova.create_nfo('D:\\JetBrains\\PycharmProjects\\emby-metadata\\nfo')

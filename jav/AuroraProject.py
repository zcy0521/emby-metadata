#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

from bs4 import BeautifulSoup

from jav.Fanza import Fanza
from utils import http_util


class AuroraProject(object):
    # 官网
    SITE_URL = 'https://www.aurora-pro.com/'
    DETAIL_URL = 'https://www.aurora-pro.com/shop/-/product/p/goods_id={video_no}/'

    def __init__(self, video_no):
        self.video_no = video_no

        # 详情页
        detail_url = AuroraProject.DETAIL_URL.format(video_no=video_no)
        detail_html = http_util.get(detail_url)
        self.detail_soup = BeautifulSoup(detail_html, features="html.parser")

    def get_poster_url(self):
        return self.get_backdrop_url().replace('open_xl', 'close_m')

    def get_backdrop_url(self):
        return  self.detail_soup.find('img', id='main_pkg')['src']

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
        title = movie_details.find('h1', class_="pro_title").get_text().strip()
        ET.SubElement(movie, "title").text = title

        # 情节
        plot = movie_details.find('div', id="product_exp").find('p').get_text().strip()
        ET.SubElement(movie, "plot").text = plot

        # thumb 封面图
        poster = ET.SubElement(movie, "thumb")
        poster.set("aspect", "poster")
        poster.text = self.get_poster_url()

        # fanart 背景图
        fanart = ET.SubElement(movie, "fanart")
        ET.SubElement(fanart, "thumb").text = movie_details.find('img', id="main_pkg")['src']
        thumbs_imgs = movie_details.find('div', class_="product_scene").find('ul').find_all('img')
        for thumbs_img in thumbs_imgs:
            ET.SubElement(fanart, "thumb").text = thumbs_img.get('src')

        # trailer 预告片
        ET.SubElement(movie, "trailer").text = self.get_trailer_url()

        info_items = movie_details.find('div', id="product_info").find('dl').find_all('dd', recursive=False)
        # print(info_items)

        # 出演女優
        actor_name = info_items[0].find('a').get_text().strip()
        actor_elem = ET.SubElement(movie, "actor")
        ET.SubElement(actor_elem, "name").text = actor_name

        # 発売日
        premiered = info_items[4].get_text().strip()
        ET.SubElement(movie, "premiered").text = premiered

        # 作品番号
        code = info_items[1].find('li').get_text().strip()
        ET.SubElement(movie, "code").text = code

        # ジャンル 标签
        tags = info_items[5].find_all('a')
        for tag in tags:
            ET.SubElement(movie, "tag").text = tag.get_text().strip()

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
    # https://www.aurora-pro.com/shop/-/product/p/goods_id=APAA-405/
    aurora = AuroraProject('APAA-405')
    # print(aurora.get_poster_url())
    # print(aurora.get_backdrop_url())
    # print(aurora.get_trailer_url())

    aurora.create_nfo('D:\\JetBrains\\PycharmProjects\\emby-metadata\\nfo')

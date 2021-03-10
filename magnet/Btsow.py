#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup


class Btsow(object):
    site_url = "https://btsow.cam/"

    def __init__(self, video_no):
        url = "https://btsow.cam/search/{video_no}".format(video_no=video_no)
        html = requests.get(url)
        print(html)

        # bs4解析html
        soup = BeautifulSoup(html.content, "html.parser")

        # 列表页
        results = soup.find("div", class_="data-list").findChildren("div", class_="row")
        results = results[1:]
        for result in results:
            # 列表页信息
            result_url = result.find("a")["href"]
            name = result.find("a")["title"]
            size = result.find("div", class_="col-sm-2 col-lg-1 hidden-xs text-right size").text.strip()
            print(result_url, "|", size, "|", name)

            # 详情页信息
            result_html = requests.get(result_url)
            result_soup = BeautifulSoup(result_html.content, "html.parser")

            # magnet
            magnet = result_soup.find("textarea", id="magnetLink").text.strip()
            print(magnet)

            # 文件列表
            files = result_soup.find_all("div", class_="detail data-list")[1].findChildren("div", class_="row")
            files = files[1:]
            for file in files:
                file_name = file.find("div", class_="col-xs-8 col-sm-10 col-lg-11 file").text.strip()
                file_size = file.find("div", class_="col-xs-4 col-sm-2 col-lg-1 text-right size").text.strip()
                print(file_name, " ", file_size)


if __name__ == "__main__":
    # https://btsow.cam/search/MIDE-607
    btsow = Btsow("326SCP-006")

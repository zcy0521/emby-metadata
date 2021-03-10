#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup


class Zhongziso(object):
    site_url = "https://zhongziso13.xyz/"

    def __init__(self, video_no):
        url = "https://zhongziso13.xyz/list/{video_no}/1".format(video_no=video_no)
        print(url)
        html = requests.get(url)
        print(html)

        # bs4解析html
        soup = BeautifulSoup(html.content, "html.parser")

        # 列表页
        results = soup.find("div", class_="panel-body table-responsive table-condensed").findChildren("table")
        for result in results:
            # 列表页信息
            result_url = result.find("a")["href"]
            result_url = self.site_url + result_url.lstrip("/")
            size = result.find(lambda tag:tag.name=="td" and "大小：" in tag.text).find("strong").text.strip()
            print(result_url, "|", size, end="")

            # 详情页信息
            result_html = requests.get(result_url)
            result_soup = BeautifulSoup(result_html.content, "html.parser")

            # 名称
            name = result_soup.find("div", class_="panel panel-primary").find("div", class_="panel-heading").find("div", class_="text-left").text.strip()
            print("|", name)

            # magnet
            magnet = result_soup.find("div", class_="panel panel-primary").find("div", class_="panel-body").find("textarea", id="copytext").text.strip()
            print(magnet)

            # 文件列表
            files = result_soup.find("select", class_="form-control").find_all("option")
            for file in files:
                print(file.text.strip())


if __name__ == "__main__":
    # https://zhongziso13.xyz/list/MIDE-607/1
    zhongziso = Zhongziso("IPIT-010")

#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup


class IDope(object):
    SITE_URL = "https://idope.se"
    SEARCH_URL = "https://idope.se/torrent-list/{video_no}/"

    def __init__(self, video_no):
        list_url = IDope.SEARCH_URL.format(video_no=video_no)
        print(list_url)


if __name__ == "__main__":
    idope = IDope("326SCP-006")
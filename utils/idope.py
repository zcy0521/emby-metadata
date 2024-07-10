#!/usr/bin/envpython3
# -*-coding:utf-8-*-


class Idope(object):
    SITE_URL = "https://idope.se"
    SEARCH_URL = "https://idope.se/torrent-list/{video_no}/"

    def __init__(self, video_no):
        list_url = Idope.SEARCH_URL.format(video_no=video_no)
        print(list_url)


if __name__ == "__main__":
    idope = Idope("326SCP-006")
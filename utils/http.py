#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import requests


def get(url):
    session = requests.Session()
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }

    return session.get(url, headers=headers)

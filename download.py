#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import requests


def download(url, proxy_ip):
    if url is None:
        return None

    session = requests.Session()
    session.proxies = {
        "http": 'socks5://{proxy}'.format(proxy=proxy_ip),
        "https": 'socks5://{proxy}'.format(proxy=proxy_ip)
    }

    response = session.get(url)
    if response is None:
        print('Download %s response is None'.format(url))
        return None

    return response.content

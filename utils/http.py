#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import requests


def get(url):
    session = requests.Session()
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }

    proxies = {
        "http": "socks5://127.0.0.1:1080",
        "https": "socks5://127.0.0.1:1080",
    }

    return session.get(url, headers=headers, proxies=proxies)


def proxy_get(session, url, headers):
    proxies = {
        "http": "socks5://127.0.0.1:1080",
        "https": "socks5://127.0.0.1:1080",
    }

    return session.get(url, headers=headers, proxies=proxies)


def proxy_post(session, url, data, headers):
    proxies = {
        "http": "socks5://127.0.0.1:1080",
        "https": "socks5://127.0.0.1:1080",
    }

    return session.post(url, data=data, headers=headers, proxies=proxies)

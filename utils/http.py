#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import requests


def get(url, headers):
    session = requests.Session()

    proxies = {
        "http": "socks5://192.168.50.254:1080",
        "https": "socks5://192.168.50.254:1080",
    }

    return session.get(url, headers=headers, proxies=proxies)


def post(url, data, headers):
    session = requests.Session()

    proxies = {
        "http": "socks5://127.0.0.1:1080",
        "https": "socks5://127.0.0.1:1080",
    }

    return session.post(url, data=data, headers=headers, proxies=proxies)

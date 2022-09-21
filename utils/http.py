#!/usr/bin/envpython3
# -*-coding:utf-8-*-
from urllib3.contrib.socks import SOCKSProxyManager


def get(url):
    # https://urllib3.readthedocs.io/en/stable/advanced-usage.html#socks-proxies
    proxy = SOCKSProxyManager('socks5h://localhost:1080/')

    r = proxy.request('GET', url)

    # https://urllib3.readthedocs.io/en/stable/user-guide.html#response-content
    return r.data.decode('utf-8')


def post(url, fields):
    # https://urllib3.readthedocs.io/en/stable/advanced-usage.html#socks-proxies
    proxy = SOCKSProxyManager('socks5h://localhost:1080/')

    r = proxy.request('POST', url, fields=fields)

    # https://urllib3.readthedocs.io/en/stable/user-guide.html#response-content
    return r.data.decode('utf-8')

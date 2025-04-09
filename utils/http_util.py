#!/usr/bin/envpython3
# -*-coding:utf-8-*-
from urllib3.contrib.socks import SOCKSProxyManager

# https://urllib3.readthedocs.io/en/stable/advanced-usage.html#socks-proxies
proxy = SOCKSProxyManager('socks5h://127.0.0.1:1080/')


def get(url, headers=None, redirect=True, *, charset='utf8'):
    # https://urllib3.readthedocs.io/en/stable/user-guide.html#response-content
    response = proxy.request('GET', url, headers=headers, redirect=redirect)
    return response.data.decode(charset, 'ignore')


def post(url, fields, headers=None, redirect=True, *, charset='utf8'):
    response = proxy.request('POST', url, fields=fields, headers=headers, redirect=redirect)
    return response.data.decode(charset, 'ignore')


def download(url, headers=None):
    response = proxy.request('GET', url, headers=headers)
    return response.data

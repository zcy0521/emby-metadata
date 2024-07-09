#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import urllib3
from urllib3.contrib.socks import SOCKSProxyManager

# https://urllib3.readthedocs.io/en/stable/advanced-usage.html#socks-proxies
proxy = SOCKSProxyManager('socks5h://127.0.0.1:10800/')


def get(url, headers=None, redirect=True, *, charset='utf8'):
    r = proxy.request('GET', url, headers=headers, redirect=redirect)

    # https://urllib3.readthedocs.io/en/stable/user-guide.html#response-content
    return r.data.decode(charset, 'ignore')


def post(url, fields, headers=None, redirect=True, *, charset='utf8'):
    r = proxy.request('POST', url, fields=fields, headers=headers, redirect=redirect)

    # https://urllib3.readthedocs.io/en/stable/user-guide.html#response-content
    return r.data.decode(charset, 'ignore')


def download(url, headers=None):
    r = proxy.request('GET', url, headers=headers)

    # https://urllib3.readthedocs.io/en/stable/user-guide.html#response-content
    return r.data

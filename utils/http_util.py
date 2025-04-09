#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import urllib3
from urllib3.contrib.socks import SOCKSProxyManager


def get(url, headers=None, redirect=True, *, charset='utf8'):
    # 非代理方式 https://urllib3.readthedocs.io/en/stable/user-guide.html#response-content
    response = urllib3.request('GET', url, headers=headers, redirect=redirect)

    # socks理方式 https://urllib3.readthedocs.io/en/stable/advanced-usage.html#socks-proxies
    # proxy = SOCKSProxyManager('socks5h://127.0.0.1:10800/')
    # response = proxy.request('GET', url, headers=headers, redirect=redirect)

    return response.data.decode(charset, 'ignore')


def post(url, fields, headers=None, redirect=True, *, charset='utf8'):
    response = urllib3.request('POST', url, fields=fields, headers=headers, redirect=redirect)

    # proxy = SOCKSProxyManager('socks5h://127.0.0.1:10800/')
    # response = proxy.request('GET', url, headers=headers, redirect=redirect)

    return response.data.decode(charset, 'ignore')


def download(url, headers=None):
    response = urllib3.request('GET', url, headers=headers)

    # proxy = SOCKSProxyManager('socks5h://127.0.0.1:10800/')
    # response = proxy.request('GET', url, headers=headers, redirect=redirect)

    return response.data

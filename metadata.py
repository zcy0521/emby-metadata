#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os
import sys

from fanart import download_fanart
from poster import download_poster
from folder import format_folder, series_not_in, get_video_number

if __name__ == '__main__':
    # 输入待整理文件夹与下载代理
    folder_path = "T:\\Downloads"
    proxy_ip = None

    # 整理视频文件夹
    format_folder(folder_path)

    # 查找不在的系列
    series = series_not_in(folder_path)
    if series:
        print(series) and sys.exit()

    # metadata
    for (dirpath, dirnames, filenames) in os.walk(folder_path):
        for filename in filenames:
            # 已有封面
            poster_path = os.path.join(dirpath, 'poster.jpg')
            if os.path.exists(poster_path):
                continue

            # 已有背景图
            fanart_path = os.path.join(dirpath, 'fanart.jpg')
            if os.path.exists(fanart_path):
                continue

            # 文件
            file = os.path.join(dirpath, filename)

            # 预告视频所在文件夹
            dirname = os.path.basename(os.path.dirname(file))
            if dirname == 'trailers':
                continue

            # 获取视频文件编号
            video_number = get_video_number(file)
            if video_number is None:
                continue

            # 下载封面
            poster_bytes = download_poster(video_number, proxy_ip)
            if poster_bytes is not None:
                with open(poster_path, 'wb') as f:
                    f.write(poster_bytes)

            # 下载背景图
            fanart_bytes = download_fanart(video_number, proxy_ip)
            if fanart_bytes is not None:
                with open(fanart_path, 'wb') as f:
                    f.write(fanart_bytes)

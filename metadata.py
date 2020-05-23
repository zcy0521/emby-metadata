#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os
import sys

from background import download_background
from cover import download_cover
from folder import format_folder, series_not_in, get_video_number

if __name__ == '__main__':
    # 输入待整理文件夹与下载代理
    folder_path = "D:\Downloads\YRH-063"
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
            cover_path = os.path.join(dirpath, 'cover.jpg')
            if os.path.exists(cover_path):
                continue

            # 已有背景图
            background_path = os.path.join(dirpath, 'background.jpg')
            if os.path.exists(background_path):
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
            cover_bytes = download_cover(video_number, proxy_ip)
            if cover_bytes is not None:
                with open(cover_path, 'wb') as f:
                    f.write(cover_bytes)

            # 下载背景图
            background_bytes = download_background(video_number, proxy_ip)
            if background_bytes is not None:
                with open(background_path, 'wb') as f:
                    f.write(background_bytes)

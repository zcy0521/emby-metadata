#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os
import sys

from utils import folder, backdrop, poster

if __name__ == '__main__':
    # 输入待整理文件夹与下载代理
    folder_path = "D:\\Test"

    # 整理视频文件夹
    folder.format_folder(folder_path)

    # 按文件夹整理
    for (dir_path, dirnames, filenames) in os.walk(folder_path):
        for dirname in dirnames:
            # 已有封面
            poster_path = os.path.join(dir_path, dirname, 'poster.jpg')
            if os.path.exists(poster_path):
                continue

            # 已有背景图
            backdrop_path = os.path.join(dir_path, dirname, 'backdrop.jpg')
            if os.path.exists(backdrop_path):
                continue

            # 文件夹名即视频番号
            video_no = dirname

            # 如果存在未包含的系列编号，则打印编号并退出
            series = video_no.split('-', 1)[0]
            if series not in poster.posters:
                print(f"番号前缀 {series} 封面url不存在！")
                sys.exit()
            if series not in backdrop.backdrops:
                print(f"番号前缀 {series} 背景图url不存在！")
                sys.exit()

            # 下载封面
            poster_bytes = poster.download_poster(video_no)
            if poster_bytes is not None:
                with open(poster_path, 'wb') as f:
                    f.write(poster_bytes)

            # 下载背景图
            backdrop_bytes = backdrop.download_backdrop(video_no)
            if backdrop_bytes is not None:
                with open(backdrop_path, 'wb') as f:
                    f.write(backdrop_bytes)

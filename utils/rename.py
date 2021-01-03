#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

if __name__ == '__main__':
    # 输入待整理文件夹与下载代理
    folder_path = "D:\Happy"

    for (dirpath, dirnames, filenames) in os.walk(folder_path):
        for filename in filenames:

            if filename == 'cover.jpg':
                file_old = os.path.join(dirpath, filename)
                file_new = os.path.join(dirpath, 'poster.jpg')
                os.renames(file_old, file_new)

            if filename == 'background.jpg':
                file_old = os.path.join(dirpath, filename)
                file_new = os.path.join(dirpath, 'fanart.jpg')
                os.renames(file_old, file_new)

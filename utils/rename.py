#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

if __name__ == '__main__':
    folder_path = '/mnt/downloads/明里つむぎ'

    for (dirpath, dirnames, filenames) in os.walk(folder_path):
        for filename in filenames:

            if filename == 'poster.jpg':
                file_old = os.path.join(dirpath, filename)
                file_new = os.path.join(dirpath, 'poster.jpg')
                os.renames(file_old, file_new)

            if filename == 'fanart.jpg':
                file_old = os.path.join(dirpath, filename)
                file_new = os.path.join(dirpath, 'backdrop.jpg')
                os.renames(file_old, file_new)

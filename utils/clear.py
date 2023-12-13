#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os
import shutil


def clear_qnap(folder_path):
    for (dirpath, dirnames, filenames) in os.walk(folder_path):
        # 删除@eaDir目录
        for dirname in dirnames:
            eaDir_folder = os.path.join(dirpath, dirname, '@eaDir')
            if os.path.exists(eaDir_folder):
                shutil.rmtree(eaDir_folder)

        # 删除Thumbs.db文件
        for filename in filenames:
            if filename == 'Thumbs.db':
                file = os.path.join(dirpath, filename)
                os.remove(file)


def clear_synology(folder_path):
    for (dirpath, dirnames, filenames) in os.walk(folder_path):
        # 删除thumb_folder目录
        for dirname in dirnames:
            thumb_folder = os.path.join(dirpath, dirname, '.@__thumb')
            if os.path.exists(thumb_folder):
                shutil.rmtree(thumb_folder)


if __name__ == '__main__':
    # 清理 @eaDir Thumbs.db
    clear_qnap('J:\\')
    clear_qnap('K:\\')
    clear_qnap('L:\\')
    clear_qnap('M:\\')
    clear_qnap('N:\\')

    # 清理
    clear_synology('O:\\')

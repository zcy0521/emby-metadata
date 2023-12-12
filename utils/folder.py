#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import mimetypes
import os
import shutil
from distutils.file_util import move_file
from pathlib import Path


def format_folder(folder_path):
    for (dirpath, dirnames, filenames) in os.walk(folder_path):
        for filename in filenames:
            # 文件
            file = os.path.join(dirpath, filename)

            # 非视频文件
            if not is_video(file):
                continue

            # 文件夹名
            dirname = os.path.basename(os.path.dirname(file))

            # 预告视频所在文件夹
            if dirname == 'trailers':
                continue

            # 文件名
            filename = Path(file).stem
            if ' - ' in filename:
                filename = filename.split(' - ')[0]

            # 文件与所在文件夹名称不同
            if filename != dirname:
                target_dir = os.path.join(dirpath, filename)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                move_file(file, target_dir)


def is_video(file):
    mimetypes.init()
    file_type = mimetypes.guess_type(file)[0]
    if file_type is not None:
        file_type = file_type.split('/')[0]
        if file_type == 'video':
            return True
    return False


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
    # 整理 STARS-094 - Chinese.mp4
    clear_qnap('J:\\')
    clear_qnap('K:\\')
    clear_qnap('L:\\')
    clear_qnap('M:\\')
    clear_qnap('N:\\')

    clear_synology('O:\\')

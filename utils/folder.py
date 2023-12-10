#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import mimetypes
import os
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


if __name__ == '__main__':
    # 整理 STARS-094 - Chinese.mp4
    format_folder('Z:\\')

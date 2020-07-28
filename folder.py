#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import mimetypes
import os
from distutils.file_util import move_file
from pathlib import Path

from fanart import fanarts
from poster import posters


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


def series_not_in(folder_path):
    series_set = set()
    for (dirpath, dirnames, filenames) in os.walk(folder_path):
        for filename in filenames:
            # 文件
            file = os.path.join(dirpath, filename)

            # 获取视频文件编号
            video_number = get_video_number(file)
            if video_number is None:
                continue

            # 不在 posters fanarts
            series = video_number.split('-', 1)[0]
            if series not in posters:
                series_set.add(filename)
            if series not in fanarts:
                series_set.add(filename)
    return series_set


def get_video_number(file):
    if is_video(file):
        video_number = Path(file).stem
        if ' - ' in video_number:
            video_number = video_number.split(' - ')[0]
        if video_number.endswith('-Split'):
            video_number = video_number[:-6]
        return video_number
    return None


def is_video(file):
    mimetypes.init()
    file_type = mimetypes.guess_type(file)[0]
    if file_type is not None:
        file_type = file_type.split('/')[0]
        if file_type == 'video':
            return True
    return False


if __name__ == '__main__':
    # 整理
    # format_folder('\\\\192.168.100.5\happy\Digital')
    format_folder('D:\Downloads\来まえび')

    # # 查找不存在的系列
    # result = series_not_in('C:\Downloads')
    # if result:
    #     print(result)
    # else:
    #     print("match all")

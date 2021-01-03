#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os

from tqdm import tqdm

class_dict = {
    'FANZA': {},
    'MOODYZ': {'MIDD', 'MIDE'},
    'IdeaPocket': {'IPZ', 'IPX', 'IDBD', 'SUPD'},
    'S1S1S1': {'SNIS', 'SSNI', 'OFJE', 'SIVR'},
    'PREMIUM': {'PRED'},
    'Madonna': {'JUY'},
    'TameikeGoro': {'MEYD'},
    'Attackers': {'ADN', 'ATID', 'RBD', 'SHKD', 'SSPD', 'ATKD'},
    'Das': {'DASD'},
    'SOD': {'STAR', 'STARS', 'SDDE', 'SDEN', 'SDMF', 'SDMU', 'SSHN', 'HYPN', '3DSVR'},
    'NaturalHigh': {'NHDTB', 'SHN'},
    'MGS': {'ABS', 'ABP', 'DOM', 'EDD', 'INU', 'JOB', 'PPT', 'SGA', 'WAT', 'YRH', 'SIRO', '001HMNF', '200GANA', '230ORE', '259LUXU', '276KITAIKE', '277DCV', '300MAAN', '300MIUM', '300NTK', '345SIMM', '390JAC', '390JNT', '402MNTJ', '435MFC', '459TEN', '483SGK'},
    'Prestige': {},
    'AliceJapan': {},
    'Dogma': {},
    'HHH': {'HUNTA', 'AP'},
    'HMP': {'HODV'},
    'MaxA': {},
    'Momotaro': {},
    'Mousouzoku': {}
}

if __name__ == '__main__':
    folder_path = '/mnt/downloads/明里つむぎ'

    # 删除文件夹中现有图片
    for (dirpath, dirnames, filenames) in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith('.jpg'):
                file = os.path.join(dirpath, filename)
                os.remove(file)

    # 按文件夹整理
    for (dirpath, dirnames, filenames) in os.walk(folder_path):
        for dirname in tqdm(dirnames):
            # 文件夹名 系列-番号
            (series, item) = dirname.split('-', 1)

            # 查找系列不在字典中
            if series not in str(class_dict.values()):
                if series.startswith('230ORE'):
                    series = '230ORE'
                else:
                    print('无法下载封面:' + dirname)
                    continue

            # 查找系列所在类
            class_name = next(filter(lambda x: series in class_dict[x] and x, class_dict))
            print('下载封面:' + dirname)

            # 根据类名实例化
            # class_name.py
            jav_package = __import__(class_name)
            # class class_name(){...}
            jav_class = getattr(jav_package, class_name)
            # instance dirname是番号
            jav = jav_class(dirname)

            # 保存poster
            poster_bytes = jav.download_poster()
            if poster_bytes is not None:
                poster_path = os.path.join(dirpath, dirname, 'poster.jpg')
                with open(poster_path, 'wb') as f:
                    f.write(poster_bytes)

            # 保存fanart
            fanart_bytes = jav.download_fanart()
            if fanart_bytes is not None:
                fanart_path = os.path.join(dirpath, dirname, 'fanart.jpg')
                with open(fanart_path, 'wb') as f:
                    f.write(fanart_bytes)

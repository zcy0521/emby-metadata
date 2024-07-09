#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os
import shutil

from tqdm import tqdm

from utils import http_util

class_dict = {
    'AliceJapan': {},
    'Attackers': {'ADN', 'ATID', 'ATKD', 'RBD', 'RBK', 'SHKD', 'SSPD', 'YUJ'},
    'AuroraProject': {'APAA', 'APAK', 'APGH', 'APNS'},
    'Beckaku': {'BKKG'},
    'BeFree': {'BF'},
    'Casanova': {'CAFR', 'CAMI'},
    'CrystalEizou': {},
    'DasDas': {'DASD', 'DASS'},
    'Deeps': {'DVRT'},
    'Dogma': {},
    'EBody': {'EYAN'},
    'Faleno': {'FSDSS'},
    'Fanza': {'AP', 'GAID', 'FMDL', 'JUKF', 'KSJK', 'MADV', 'REXD', 'SQTE', 'OYC'},
    'GloryQuest': {'GVH'},
    'Hakusuiriki': {'CEAD', 'CEMD'},
    'HHH': {'HUNTA'},
    'HMP': {'HODV'},
    'IdeaPocket': {'IPX', 'IPZ', 'IPZZ', 'IDBD', 'IPIT', 'IPTD', 'SUPD'},
    'Kawaii': {'CAWD'},
    'KiraKira': {'BLK'},
    'KMP': {'MDTM', 'REAL'},
    'Madonna': {'JUL', 'JUQ', 'JUY'},
    'MaxA': {},
    'MGS': {'SIRO', '001HMNF', '020GVG', '039NEO', '169MDTM', '179BAZX', '200GANA', '230ORE', '249OKS', '259LUXU', '263NACR', '276KITAIKE', '277DCV', '290JBJB', '300MAAN', '300MIUM', '300NTK', '302GERK', '315ETQR', '345SIMM', '348NTR', '390JAC', '390JNT', '402MNTJ', '413INST', '435MFC', '459TEN', '483SGK'},
    'MkoLabo': {'MISM'},
    'Momotaro': {},
    'MOODYZ': {'MIAA', 'MIDD', 'MIDE', 'MIDV', 'MIMK'},
    'Mousouzoku': {'BIJN', 'GMEM', 'USBA'},
    'Muku': {'MUDR', 'MUKC'},
    'Mvg': {'MVSD'},
    'NaturalHigh': {'NHDTB', 'SHN'},
    'OPPAI': {'PPPE'},
    'Planetplus': {'NACR'},
    'PREMIUM': {'PRED'},
    'Prestige': {'ABS', 'ABP', 'ABW', 'AOI', 'DOM', 'EDD', 'INU', 'JBS', 'JOB', 'PPT', 'SGA', 'WAT', 'YRH'},
    'S1S1S1': {'SNIS', 'SSNI', 'SSIS', 'OFJE', 'SIVR'},
    'Shark': {'JBJB', 'MACB'},
    # SOD Prime 无法访问，通过FANZA、MGS查询
    # 'SOD': {'AVOP', 'HBAD', 'HYPN', 'IESP', 'KMHRS', 'OKS', 'SDDE', 'SDEN', 'SDMF', 'SDMU', 'SDNM', 'SDNT', 'SDSI', 'SSHN', 'STAR', 'STARS', '3DSVR'},
    'TAKARA': {'CEMN'},
    'TameikeGoro': {'MBYD', 'MEYD', 'PFES'},
    'TMA': {'25ID', 'AOZ'},
    'Tsumabana': {'HZGD'},
    'WANZ': {'WANZ', 'WAAA'},
}


def get_jav(dirname):
    if '-' not in dirname:
        return None

    # 文件夹名 系列-番号
    (series, item) = dirname.split('-', 1)

    # 查找系列不在字典中
    if series not in str(class_dict.values()):
        if series.startswith('230ORE'):
            series = '230ORE'
        else:
            print('无法下载封面:' + dirname)
            return None

    # 查找系列所在类
    class_name = next(filter(lambda x: series in class_dict[x] and x, class_dict))

    # 根据类名实例化
    # class_name.py
    jav_package = __import__('jav.' + class_name)
    # class class_name(){...}
    jav_class = getattr(jav_package, class_name)
    jav_class = getattr(jav_class, class_name)
    # instance dirname是番号
    return jav_class(dirname)


if __name__ == '__main__':
    folder_path = 'Z:\\4K'

    # 删除文件夹中现有图片
    for (dirpath, dirnames, filenames) in os.walk(folder_path):
        # 删除图片
        for filename in filenames:
            if filename.endswith(('.jpg', ',jpeg', 'png')):
                file = os.path.join(dirpath, filename)
                os.remove(file)

        # 删除预告片目录
        for dirname in tqdm(dirnames):
            trailers_folder = os.path.join(dirpath, dirname, 'trailers')
            if os.path.exists(trailers_folder):
                shutil.rmtree(trailers_folder)

    # 按文件夹整理
    for (dirpath, dirnames, filenames) in os.walk(folder_path):
        for dirname in tqdm(dirnames):
            jav = get_jav(dirname)
            if jav is None:
                continue

            # 保存封面
            poster_url = jav.get_poster_url()
            poster_bytes = http_util.download(poster_url)
            if poster_bytes is not None:
                poster_name = os.path.basename(poster_url)
                poster_ext = os.path.splitext(poster_name)[1]
                poster_path = os.path.join(dirpath, dirname, 'poster' + poster_ext)
                with open(poster_path, 'wb') as f:
                    f.write(poster_bytes)

            # 保存背景图 支持多张
            backdrop_url = jav.get_backdrop_url()
            backdrop_bytes = http_util.download(backdrop_url)
            if backdrop_bytes is not None:
                backdrop_name = os.path.basename(backdrop_url)
                backdrop_ext = os.path.splitext(backdrop_name)[1]
                backdrop_path = os.path.join(dirpath, dirname, 'backdrop' + backdrop_ext)
                with open(backdrop_path, 'wb') as f:
                    f.write(backdrop_bytes)

            # 保存预告片
            trailer_url = jav.get_trailer_url()
            trailer_bytes = http_util.download(trailer_url)
            if trailer_bytes is not None:
                # 创建预告片目录
                trailer_folder = os.path.join(dirpath, dirname,'trailers')
                if not os.path.exists(trailer_folder):
                    os.makedirs(trailer_folder)
                # 保存预告片
                trailer_name = os.path.basename(trailer_url)
                trailer_ext = os.path.splitext(trailer_name)[1]
                trailer_path = os.path.join(dirpath, dirname, 'trailers', 'trailer' + trailer_ext)
                with open(trailer_path, 'wb') as f:
                    f.write(trailer_bytes)

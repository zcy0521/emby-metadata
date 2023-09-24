#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os
import shutil

from tqdm import tqdm

class_dict = {
    'FANZA': {'GAID', 'FMDL', 'JUKF', 'MADV', 'REXD', 'SQTE', 'KSJK'},
    'MOODYZ': {'MIDD', 'MIDE', 'MIDV', 'MIMK', 'MIAA'},
    'IdeaPocket': {'IPZ', 'IPZZ', 'IPX', 'IPIT', 'IPTD', 'IDBD', 'SUPD'},
    'S1S1S1': {'SNIS', 'SSNI', 'SSIS', 'OFJE', 'SIVR'},
    'PREMIUM': {'PRED'},
    'Madonna': {'JUY', 'JUQ', 'JUL'},
    'TameikeGoro': {'MBYD', 'MEYD', 'PFES'},
    'Attackers': {'ADN', 'ATID', 'ATKD', 'RBD', 'RBK', 'SHKD', 'SSPD', 'YUJ'},
    'Das': {'DASD', 'DASS'},
    'SOD': {'AVOP', 'HBAD', 'HYPN', 'IESP', 'OKS', 'SDDE', 'SDEN', 'SDMF', 'SDMU', 'SDNM', 'SDNT', 'SDSI', 'SSHN', 'STAR', 'STARS', '3DSVR', 'KMHRS'},
    'NaturalHigh': {'NHDTB', 'SHN'},
    'MGS': {'SIRO', '001HMNF', '020GVG', '039NEO', '169MDTM', '179BAZX', '200GANA', '230ORE', '249OKS', '259LUXU', '263NACR', '276KITAIKE', '277DCV', '290JBJB', '300MAAN', '300MIUM', '300NTK', '302GERK', '315ETQR', '345SIMM', '348NTR', '390JAC', '390JNT', '402MNTJ', '435MFC', '459TEN', '483SGK'},
    'Prestige': {'ABS', 'ABP', 'ABW', 'AOI', 'DOM', 'EDD', 'INU', 'JBS', 'JOB', 'PPT', 'SGA', 'WAT', 'YRH'},
    'AliceJapan': {},
    'Dogma': {},
    'HHH': {'AP', 'HUNTA', 'OYC'},
    'HMP': {'HODV'},
    'MaxA': {},
    'Momotaro': {},
    'Mousouzoku': {'BIJN', 'GMEM', 'USBA'},
    'KMP': {'MDTM', 'REAL'},
    'TMA': {'25ID', 'AOZ'},
    'Tsumabana': {'HZGD'},
    'Shark': {'JBJB', 'MACB'},
    'Planetplus': {'NACR'},
    'WANZ': {'WANZ', 'WAAA'},
    'TAKARA': {'CEMN'},
    'BECKAKU': {'BKKG'},
    'CASANOVA': {'CAFR', 'CAMI'},
    'FALENO': {'FSDSS'},
    'Kawaii': {'CAWD'},
    'OPPAI': {'PPPE'},
    'BeFree': {'BF'},
    'KiraKira': {'BLK'},
    'AURORA': {'APAA', 'APAK', 'APGH', 'APNS'},
    'Hakusuiriki': {'CEAD', 'CEMD'},
    'Deeps': {'DVRT'},
    'EBODY': {'EYAN'},
    'GloryQuest': {'GVH'},
    'MkoLabo': {'MISM'},
    'Muku': {'MUDR', 'MUKC'},
    'Mvg': {'MVSD'},
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
    folder_path = 'E:\\Media\\NSFW\\花狩まい'

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

            # 保存poster
            poster_bytes = jav.download_poster()
            poster_ext = jav.get_poster_ext()
            if poster_bytes is not None:
                poster_path = os.path.join(dirpath, dirname, 'poster' + poster_ext)
                with open(poster_path, 'wb') as f:
                    f.write(poster_bytes)

            # 保存fanart
            fanart_bytes = jav.download_fanart()
            fanart_ext = jav.get_fanart_ext()
            if fanart_bytes is not None:
                fanart_path = os.path.join(dirpath, dirname, 'fanart' + fanart_ext)
                with open(fanart_path, 'wb') as f:
                    f.write(fanart_bytes)

            # 保存movie
            movie_bytes = jav.download_movie()
            movie_ext = jav.get_movie_ext()
            if movie_bytes is not None:
                # 创建预告片目录
                movie_folder = os.path.join(dirpath, dirname,'trailers')
                if not os.path.exists(movie_folder):
                    os.makedirs(movie_folder)
                # 保存预告片
                movie_path = os.path.join(movie_folder, dirname + movie_ext)
                with open(movie_path, 'wb') as f:
                    f.write(movie_bytes)

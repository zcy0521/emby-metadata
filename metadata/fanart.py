#!/usr/bin/envpython3
# -*-coding:utf-8-*-
import os
from io import BytesIO

from PIL import Image

from utils.http_util import get

fanarts = {
    # ATTACKERS https://www.attackers.net
    'ADN': 'https://www.attackers.net/contents/works/adn{item}/adn{item}-pl.jpg',
    'ATID': 'https://www.attackers.net/contents/works/atid{item}/atid{item}-pl.jpg',
    'JBD': 'https://www.attackers.net/contents/works/jbd{item}/jbd{item}-pl.jpg',
    'RBD': 'https://www.attackers.net/contents/works/rbd{item}/rbd{item}-pl.jpg',
    'SHKD': 'https://www.attackers.net/contents/works/shkd{item}/shkd{item}-pl.jpg',
    'SSPD': 'https://www.attackers.net/contents/works/sspd{item}/sspd{item}-pl.jpg',
    # AURORA PROJECT https://www.aurora-pro.com
    'APKH': 'https://rsc.aurora-pro.com/rsc/imgs/pkg/apkh-{item}/apkh-{item}_open_xl.jpg',
    # Be Free https://www.befreebe.com
    'BF': 'https://www.befreebe.com/contents/works/bf{item}/bf{item}-pl.jpg',
    # DREAM TICKET http://www.dt01.co.jp
    'CMD': 'http://www.dt01.co.jp/hskhsk/itsub/CMD{item}.jpg',
    # DANDY & COSMOS http://www.choi-waru.com
    'DANDY': 'http://www.choi-waru.com/images/product/back/dandy-{item}_back.jpg',
    'HAWA': 'http://www.choi-waru.com/images/product/back/hawa-{item}_back.jpg',
    # E-BODY https://www.av-e-body.com
    'EBOD': 'https://www.av-e-body.com/contents/works/ebod{item}/ebod{item}-pl.jpg',
    # FANZA https://www.dmm.co.jp
    'ALB': 'https://pics.dmm.co.jp/digital/video/alb00{item}/alb00{item}pl.jpg',
    'CADV': 'https://pics.dmm.co.jp/digital/video/49cadv00{item}/49cadv00{item}pl.jpg',
    'DVAJ': 'https://pics.dmm.co.jp/digital/video/dvaj00{item}/dvaj00{item}pl.jpg',
    'ETQR': 'https://pics.dmm.co.jp/digital/video/h_1186etqr00{item}/h_1186etqr00{item}pl.jpg',
    'GENM': 'https://pics.dmm.co.jp/digital/video/genm00{item}/genm00{item}pl.jpg',
    'HBAD': 'https://pics.dmm.co.jp/digital/video/1hbad00{item}/1hbad00{item}pl.jpg',
    'IESM': 'https://pics.dmm.co.jp/digital/video/1iesm00{item}/1iesm00{item}pl.jpg',
    'IESP': 'https://pics.dmm.co.jp/digital/video/1iesp00{item}/1iesp00{item}pl.jpg',
    'JUTN': 'https://pics.dmm.co.jp/digital/video/h_227jutn00{item}/h_227jutn00{item}pl.jpg',
    'KSBJ': 'https://pics.dmm.co.jp/digital/video/ksbj00{item}/ksbj00{item}pl.jpg',
    'MADM': 'https://pics.dmm.co.jp/digital/video/49madm00{item}/49madm00{item}pl.jpg',
    'MAKT': 'https://pics.dmm.co.jp/digital/video/h_1133makt00{item}/h_1133makt00{item}pl.jpg',
    'MILK': 'https://pics.dmm.co.jp/digital/video/h_1240milk00{item}/h_1240milk00{item}pl.jpg',
    'MIST': 'https://pics.dmm.co.jp/digital/video/1mist00{item}/1mist00{item}pl.jpg',
    'MMKZ': 'https://pics.dmm.co.jp/digital/video/mmkz00{item}/mmkz00{item}pl.jpg',
    'NGOD': 'https://pics.dmm.co.jp/digital/video/ngod00{item}/ngod00{item}pl.jpg',
    'NKD': 'https://pics.dmm.co.jp/digital/video/nkd00{item}/nkd00{item}pl.jpg',
    'SDNM': 'https://pics.dmm.co.jp/digital/video/1sdnm00{item}/1sdnm00{item}pl.jpg',
    'SHM': 'https://pics.dmm.co.jp/digital/video/h_687shm00{item}/h_687shm00{item}pl.jpg',
    'T28': 'https://pics.dmm.co.jp/digital/video/55t2800{item}/55t2800{item}pl.jpg',
    'ZEX': 'https://pics.dmm.co.jp/digital/video/h_720zex00{item}/h_720zex00{item}pl.jpg',
    'HOI': 'https://pics.dmm.co.jp/digital/amateur/hoi{item}/hoi{item}jp.jpg',
    'ORE': 'https://pics.dmm.co.jp/digital/amateur/ore{item}/ore{item}jp.jpg',
    'OREC': 'https://pics.dmm.co.jp/digital/amateur/orec{item}/orec{item}jp.jpg',
    'ORETD': 'https://pics.dmm.co.jp/digital/amateur/oretd{item}/oretd{item}jp.jpg',
    'OREX': 'https://pics.dmm.co.jp/digital/amateur/orex{item}/orex{item}jp.jpg',
    # Fitch https://www.fitch-av.com
    'JUFD': 'https://www.fitch-av.com/contents/works/jufd{item}/jufd{item}-pl.jpg',
    'JUFE': 'https://www.fitch-av.com/contents/works/jufe{item}/jufe{item}-pl.jpg',
    # GOGOS.TV（ゴーゴーズ） https://www.gogos.tv
    'C': 'https://www.gogos.tv/wp-content/uploads/gogos/pac_n/{item}.jpg',
    # HHH（トリプルエイチ） https://www.hhh-av.com
    'AP': 'https://www.hhh-av.com/contents/works/ap{item}/ap{item}pl.jpg',
    'HUNTA': 'https://www.hhh-av.com/contents/works/hunta{item}/hunta{item}pl.jpg',
    # HMJM http://www.hamajim.com
    'HMNF': 'https://pics.dmm.co.jp/digital/video/h_172hmnf00{item}/h_172hmnf00{item}pl.jpg',
    # IDEAPOCKET https://www.ideapocket.com
    'IDBD': 'https://www.ideapocket.com/contents/works/idbd{item}/idbd{item}-pl.jpg',
    'IPX': 'https://www.ideapocket.com/contents/works/ipx{item}/ipx{item}-pl.jpg',
    'IPZ': 'https://www.ideapocket.com/contents/works/ipz{item}/ipz{item}-pl.jpg',
    'SUPD': 'https://www.ideapocket.com/contents/works/supd{item}/supd{item}-pl.jpg',
    # kawaii* https://www.kawaiikawaii.jp
    'CAWD': 'https://www.kawaiikawaii.jp/contents/works/cawd{item}/cawd{item}-pl.jpg',
    # kira☆kira https://www.kirakira-av.com
    'BLK': 'https://www.kirakira-av.com/contents/works/blk{item}/blk{item}-pl.jpg',
    # K.M.Produce https://www.km-produce.com
    'MDTM': 'https://www.km-produce.com/img/title1/mdtm-{item}.jpg',
    'SABA': 'https://www.km-produce.com/img/title1/saba-{item}.jpg',
    'SUPA': 'https://www.km-produce.com/img/title1/supa-{item}.jpg',
    'XRW': 'https://www.km-produce.com/img/title1/xrw-{item}.jpg',
    # Madonna https://www.madonna-av.com
    'JUL': 'https://www.madonna-av.com/contents/works/jul{item}/jul{item}-pl.jpg',
    'JUY': 'https://www.madonna-av.com/contents/works/juy{item}/juy{item}-pl.jpg',
    'URE': 'https://www.madonna-av.com/contents/works/ure{item}/ure{item}-pl.jpg',
    # MARRION http://marrion-av.com/
    'MMUS': 'http://marrion-av.com/img/products/mcp/mmus_{item}/package_l.jpg',
    # MGS https://www.mgstage.com
    '013ONEZ': 'https://image.mgstage.com/images/onemore/013onez/{item}/pb_e_013onez-{item}.jpg',
    '200GANA': 'https://image.mgstage.com/images/nanpatv/200gana/{item}/pb_e_200gana-{item}.jpg',
    '230OREX': 'https://image.mgstage.com/images/orenoshirouto/230orex/{item}/pb_e_230orex-{item}.jpg',
    '259LUXU': 'https://image.mgstage.com/images/luxutv/259luxu/{item}/pb_e_259luxu-{item}.jpg',
    '261ARA': 'https://image.mgstage.com/images/ara/261ara/{item}/pb_e_261ara-{item}.jpg',
    '277DCV': 'https://image.mgstage.com/images/documentv/277dcv/{item}/pb_e_277dcv-{item}.jpg',
    '300MAAN': 'https://image.mgstage.com/images/prestigepremium/300maan/{item}/pb_e_300maan-{item}.jpg',
    '300MIUM': 'https://image.mgstage.com/images/prestigepremium/300mium/{item}/pb_e_300mium-{item}.jpg',
    '300NTK': 'https://image.mgstage.com/images/prestigepremium/300ntk/{item}/pb_e_300ntk-{item}.jpg',
    '326EVA': 'https://image.mgstage.com/images/kurofune/326eva/{item}/pb_e_326eva-{item}.jpg',
    '326KURO': 'https://image.mgstage.com/images/kurofune/326kuro/{item}/pb_e_326kuro-{item}.jpg',
    '326MAG': 'https://image.mgstage.com/images/kurofune/326mag/{item}/pb_e_326mag-{item}.jpg',
    '326SPOR': 'https://image.mgstage.com/images/kurofune/326spor/{item}/pb_e_326spor-{item}.jpg',
    '326URF': 'https://image.mgstage.com/images/kurofune/326urf/{item}/pb_e_326urf-{item}.jpg',
    '328HMDN': 'https://image.mgstage.com/images/hamedori2nd/328hmdn/{item}/pb_e_328hmdn-{item}.jpg',
    '332NAMA': 'https://image.mgstage.com/images/namanamanet/332nama/{item}/pb_e_332nama-{item}.jpg',
    '336DTT': 'https://image.mgstage.com/images/kanbi/336dtt/{item}/pb_e_336dtt-{item}.jpg',
    '336KBI': 'https://image.mgstage.com/images/kanbi/336kbi/{item}/pb_e_336kbi-{item}.jpg',
    '345SIMM': 'https://image.mgstage.com/images/shiroutomanman/345simm/{item}/pb_e_345simm-{item}.jpg',
    '348NTR': 'https://image.mgstage.com/images/ntrnet/348ntr/{item}/pb_e_348ntr-{item}.jpg',
    '390JAC': 'https://image.mgstage.com/images/jackson/390jac/{item}/pb_e_390jac-{item}.jpg',
    '390JNT': 'https://image.mgstage.com/images/jackson/390jnt/{item}/pb_e_390jnt-{item}.jpg',
    '402MNTJ': 'https://image.mgstage.com/images/minatokujoshi/402mntj/{item}/pb_e_402mntj-{item}.jpg',
    '420HOI': 'https://image.mgstage.com/images/hoihoiz/420hoi/{item}/pb_e_420hoi-{item}.jpg',
    '427MMH': 'https://image.mgstage.com/images/mimiiki/427mmh/{item}/pb_e_427mmh-{item}.jpg',
    '428SUKE': 'https://image.mgstage.com/images/sukekiyo/428suke/{item}/pb_e_428suke-{item}.jpg',
    '435MFC': 'https://image.mgstage.com/images/moonforce/435mfc/{item}/pb_e_435mfc-{item}.jpg',
    'SIRO': 'https://image.mgstage.com/images/shirouto/siro/{item}/pb_e_siro-{item}.jpg',
    'ABP': 'https://image.mgstage.com/images/prestige/abp/{item}/pb_e_abp-{item}.jpg',
    'BLO': 'https://image.mgstage.com/images/prestige/blo/{item}/pb_e_blo-{item}.jpg',
    'CHN': 'https://image.mgstage.com/images/prestige/chn/{item}/pb_e_chn-{item}.jpg',
    'EVO': 'https://image.mgstage.com/images/prestige/evo/{item}/pb_e_evo-{item}.jpg',
    'JBS': 'https://image.mgstage.com/images/prestige/jbs/{item}/pb_e_jbs-{item}.jpg',
    'JOB': 'https://image.mgstage.com/images/prestige/job/{item}/pb_e_job-{item}.jpg',
    'MEK': 'https://image.mgstage.com/images/prestige/mek/{item}/pb_e_mek-{item}.jpg',
    'PPT': 'https://image.mgstage.com/images/prestige/ppt/{item}/pb_e_ppt-{item}.jpg',
    'SGA': 'https://image.mgstage.com/images/prestige/sga/{item}/pb_e_sga-{item}.jpg',
    'TRE': 'https://image.mgstage.com/images/prestige/tre/{item}/pb_e_tre-{item}.jpg',
    'TUS': 'https://image.mgstage.com/images/prestige/tus/{item}/pb_e_tus-{item}.jpg',
    'YRH': 'https://image.mgstage.com/images/prestige/yrh/{item}/pb_e_yrh-{item}.jpg',
    # MOODYZ https://www.moodyz.com
    'MIAA': 'https://www.moodyz.com/contents/works/miaa{item}/miaa{item}-pl.jpg',
    'MIAE': 'https://www.moodyz.com/contents/works/miae{item}/miae{item}-pl.jpg',
    'MIBD': 'https://www.moodyz.com/contents/works/mibd{item}/mibd{item}-pl.jpg',
    'MIDD': 'https://www.moodyz.com/contents/works/midd{item}/midd{item}-pl.jpg',
    'MIDE': 'https://www.moodyz.com/contents/works/mide{item}/mide{item}-pl.jpg',
    'MIGD': 'https://www.moodyz.com/contents/works/migd{item}/migd{item}-pl.jpg',
    'MIMK': 'https://www.moodyz.com/contents/works/mimk{item}/mimk{item}-pl.jpg',
    # MVG https://www.mvg.jp
    'MVSD': 'https://www.mvg.jp/contents/works/mvsd{item}/mvsd{item}-pl.jpg',
    # NATURAL HIGH https://www.naturalhigh.co.jp/
    'NHDTB': 'https://www.naturalhigh.co.jp/wp-content/uploads/NHDTB-{item}_ol.jpg',
    'SHN': 'https://www.naturalhigh.co.jp/wp-content/uploads/SHN-{item}_H4.jpg',
    # OPPAI https://www.oppai-av.com
    'PPPD': 'https://www.oppai-av.com/contents/works/pppd{item}/pppd{item}-pl.jpg',
    # PREMIUM https://www.premium-beauty.com
    'PRED': 'https://www.premium-beauty.com/contents/works/pred{item}/pred{item}-pl.jpg',
    # PRESTIGE https://www.prestige-av.com
    'DAC': 'https://www.prestige-av.com/images/corner/goods/doc/dac/{item}/pb_e_dac-{item}.jpg',
    'GAH': 'https://www.prestige-av.com/images/corner/goods/gallop/gah/{item}/pb_e_gah-{item}.jpg',
    'MGT': 'https://www.prestige-av.com/images/corner/goods/prestige/mgt/{item}/pb_e_mgt-{item}.jpg',
    # ROOKIE https://www.rookie-av.jp
    'RBB': 'https://www.rookie-av.jp/contents/works/rbb{item}/rbb{item}-pl.jpg',
    # S1 NO.1 STYLE https://www.s1s1s1.com
    'OFJE': 'https://www.s1s1s1.com/contents/works/ofje{item}/ofje{item}-pl.jpg',
    'SSNI': 'https://www.s1s1s1.com/contents/works/ssni{item}/ssni{item}-pl.jpg',
    # SOD https://www.sod.co.jp
    # WAAP GROUP http://www.waap.co.jp
    'CWM': 'http://www.waap.co.jp/hskhsk/itsub/CWM{item}.jpg',
    'DFDM': 'http://www.waap.co.jp/hskhsk/itsub/DFDM{item}.jpg',
    'DFE': 'http://www.waap.co.jp/hskhsk/itsub/DFE{item}.jpg',
    # WANZ https://www.wanz-factory.com
    'WANZ': 'https://www.wanz-factory.com/contents/works/wanz{item}/wanz{item}-pl.jpg',
    # 痴女ヘブン https://www.bi-av.com
    'CJOD': 'https://www.bi-av.com/contents/works/cjod{item}/cjod{item}-pl.jpg',
    # ダスッ！ https://www.dasdas.jp
    'DASD': 'https://www.dasdas.jp/contents/works/dasd{item}/dasd{item}-pl.jpg',
    # ひよこ https://www.hiyoko-av.com
    'PIYO': 'https://pics.dmm.co.jp/digital/video/1piyo00{item}/1piyo00{item}pl.jpg',
    # 本中 https://www.honnaka.jp
    'HND': 'https://www.honnaka.jp/contents/works/hnd{item}/hnd{item}-pl.jpg',
    # 桃太郎 https://www.indies-av.co.jp
    'YMDD': 'https://www.indies-av.co.jp/wp-content/uploads/Package/2000/YMDD-{item}_960.jpg',
    # 妄想族 https://www.mousouzoku-av.com
    'TIKB': 'https://www.mousouzoku-av.com/contents/works/tikb/tikb{item}/tikb{item}pl.jpg',
    # 舞ワイフ
    'Mywife': 'https://p02.mywife.cc/girl/{item}/thumb.jpg',
    # プラネットプラス http://planetplus.jp
    'NACR': 'http://planetplus.jp/wp01/wp-content/uploads/NACR-{item}.jpg',
    # サディスティックヴィレッジ http://www.sadistic-v.com
    'SVDVD': 'https://pics.dmm.co.jp/digital/video/1svdvd00{item}/1svdvd00{item}pl.jpg',
    # 溜池ゴロー https://www.tameikegoro.jp
    'MEYD': 'https://www.tameikegoro.jp/contents/works/meyd{item}/meyd{item}-pl.jpg',
    # AV ENTERTAINMENTS https://www.aventertainments.com
    'CWP': 'https://imgs.aventertainments.com/new/bigcover/dvd1cwp-{item}.jpg',
    'CWPBD': 'https://imgs.aventertainments.com/new/bigcover/dvd1cwpbd-{item}.jpg',
    'LAF': 'https://imgs.aventertainments.com/new/bigcover/dvd1laf-{item}.jpg',
    'LAFBD': 'https://imgs.aventertainments.com/new/bigcover/dvd1lafbd-{item}.jpg',
    'SMD': 'https://imgs.aventertainments.com/new/bigcover/dvd1smd-{item}.jpg',
    'SMBD': 'https://imgs.aventertainments.com/new/bigcover/dvd1smbd-{item}.jpg',
    'SKY': 'https://imgs.aventertainments.com/archive/bigcover/dvd1sky-{item}.jpg',
    'SKYHD': 'https://imgs.aventertainments.com/archive/bigcover/dvd1skyhd-{item}.jpg',
}


def download_fanart(video_number):
    (series, item) = video_number.split('-', 1)
    if series not in fanarts:
        return None

    fanart_url = fanarts[series].format(item=item)
    if fanart_url is None:
        print('Video %s fanart_url is None'.format(video_number))
        return None

    response = get(fanart_url)
    return response.content


if __name__ == '__main__':
    fanart_bytes = download_fanart('SKYHD-120')
    if fanart_bytes is not None:
        image = Image.open(BytesIO(fanart_bytes))
        image.show()

        download_folder = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')
        fanart_path = os.path.join(download_folder, 'fanart.jpg')
        with open(fanart_path, 'wb') as f:
            f.write(fanart_bytes)

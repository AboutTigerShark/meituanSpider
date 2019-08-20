# coding:utf-8
import json
import pickle
import re

import requests
from lxml import etree


def crawl_id():
    headers = {
        'Host': 'meishi.meituan.com',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        "Referer": "https://i.meituan.com/guangzhou/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Mobile Safari/537.36",
        "cookie": "__mta=219060518.1558835798686.1558835798686.1558836220233.2; uuid=cd2de2a9210148199638.1558835728.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=16af1d98b3259-0cd7a15037f40c-e353165-144000-16af1d98b35c8; IJSESSIONID=1c5nn3v8hz5xo6u06viol76kd; iuuid=8E14ECDCC3918400D21FE63B62DBCE2FE13527D5A6385060410137D542551935; __utmc=74597006; rvct=1; _lxsdk=8E14ECDCC3918400D21FE63B62DBCE2FE13527D5A6385060410137D542551935; webp=1; ci3=1; ci=20; cityname=%E5%B9%BF%E5%B7%9E; client-id=4bb0ad9a-04bc-49fc-9093-00031ba2aaf1; _hc.v=a961be8d-f4b9-40b2-3038-b7ba99924960.1558835798; logan_custom_report=; logan_session_token=t30jhwsrxngq0yf3o60u; latlng=; __utma=74597006.115702913.1558835739.1558835739.1558838113.2; __utmz=74597006.1558838113.2.2.utmcsr=meishi.meituan.com|utmccn=(referral)|utmcmd=referral|utmcct=/i/; __utmb=74597006.2.9.1558838114106; i_extend=C_b1Gimthomepagecategory11H__a; _lxsdk_s=16af1fdef10-a1c-70e-680%7C%7C4"
    }
    url = "https://meishi.meituan.com/i/?ci=20&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1"
    res = requests.get(url, headers=headers)
    html = etree.HTML(res.content.decode("utf-8"))
    datas = html.xpath('body/script[@crossorigin="anonymous"]')
    for data in datas:
        try:
            text = data.text
            if "window._appState" in text:
                s = text[19:-1]
                a = json.loads(s)
                # print(a)
                area_info = a["navBarData"]["areaObj"]
                pickle.dump(area_info, open("D:/py3code/ArticleSpider/areaid.json", "wb"))
        except:
            pass



crawl_id()
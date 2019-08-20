# coding:utf-8
import csv
import json
import pickle
import time

import requests


def crawl_id(areaid):
    url = "https://meishi.meituan.com/i/api/channel/deal/list"
    proxy_url = {"https": "https://180.97.250.136:6940"}

    headers = {
        'Host': 'meishi.meituan.com',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        "Referer": "https://meishi.meituan.com/i/?ci=20&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Mobile Safari/537.36",
        "Cookie": "__mta=219060518.1558835798686.1559115452678.1559115880819.34; _lxsdk_cuid=16af1d98b3259-0cd7a15037f40c-e353165-144000-16af1d98b35c8; iuuid=8E14ECDCC3918400D21FE63B62DBCE2FE13527D5A6385060410137D542551935; rvct=1; _lxsdk=8E14ECDCC3918400D21FE63B62DBCE2FE13527D5A6385060410137D542551935; webp=1; _hc.v=a961be8d-f4b9-40b2-3038-b7ba99924960.1558835798; __utmz=74597006.1558886434.4.3.utmcsr=meishi.meituan.com|utmccn=(referral)|utmcmd=referral|utmcct=/i/; client-id=f862ddc2-9dc4-40fe-a2f8-2238f5c5f884; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; cityname=%E5%B9%BF%E5%B7%9E; ci=20; IJSESSIONID=171vmqwy7g1w51nf21nf2tsxtn; __utmc=74597006; ci3=1; uuid=570078a3-bb88-432f-bb41-71ceb71f9970; logan_custom_report=; __utma=74597006.115702913.1558835739.1559112621.1559115029.10; logan_session_token=smjp35kgyomywl42wg3n; latlng=23.280772,113.723712,1559116158212; __utmb=74597006.8.9.1559116170517; i_extend=C_b1Gimthomepagecategory11H__a; _lxsdk_s=16b025a99a5-da4-ced-3ae%7C%7C34"
    }
    data = {"app": "", "areaId": areaid, "cateId": "1", "deal_attr_23": "", "deal_attr_24": "", "deal_attr_25": "", "limit": "15", "lineId": "0", "offset": "0", "optimusCode": "10", "originUrl": "http://meishi.meituan.com/i/?ci=20&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1", "partner": "126", "platform": "3", "poi_attr_20033": "", "poi_attr_20043": "", "riskLevel": "1", "sort": "default", "stationId": "0", "uuid": "570078a3-bb88-432f-bb41-71ceb71f9970", "version": "8.3.3"}

    res = requests.post(url, headers=headers, data=data, proxies=proxy_url)
    print(res.text)
    json_text = json.loads(res.text)
    totalcount = json_text["data"]["poiList"]["totalCount"]
    datas = json_text["data"]["poiList"]["poiInfos"]
    parameter_list = []
    for data in datas:
        data_list = ['', '', '', '']
        data_list[0] = data['name']
        data_list[1] = data['cateName']
        data_list[2] = data['poiid']
        data_list[3] = data['ctPoi']
        parameter_list.append(data_list)
    print("1")
    with open("url_parameter.csv", "w", newline='', encoding="gb18030") as f:
        write = csv.writer(f)
        for p in parameter_list:
            write.writerow(p)

    offset = 0
    for i in range(int(totalcount/15)):
        offset += 15
        print(offset/15+1)
        data2 = {"app": "", "areaId": areaid, "cateId": "1", "deal_attr_23": "", "deal_attr_24": "", "deal_attr_25": "", "limit": "15", "lineId": "0", "offset": offset, "optimusCode": "10", "originUrl": "http://meishi.meituan.com/i/?ci=20&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1", "partner": "126", "platform": "3", "poi_attr_20033": "", "poi_attr_20043": "", "riskLevel": "1", "sort": "default", "stationId": "0", "uuid": "570078a3-bb88-432f-bb41-71ceb71f9970", "version": "8.3.3"}
        try:
            time.sleep(5)
            res2 = requests.post(url, headers=headers, data=data2, proxies=proxy_url)
            if res2.status_code >= 300:
                print("被拦截")
            json_text2 = json.loads(res2.text)
            datas2 = json_text2["data"]["poiList"]["poiInfos"]
            for data in datas2:
                data_list2 = ['', '', '', '']
                data_list2[0] = data['name']
                data_list2[1] = data['cateName']
                data_list2[2] = data['poiid']
                data_list2[3] = data['ctPoi']
                parameter_list.append(data_list2)
            with open("url_parameter.csv", "a", newline='', encoding="gb18030") as f:
                write = csv.writer(f)
                for p in parameter_list:
                    write.writerow(p)
        except Exception as e:
            print(e)



if __name__ == "__main__":
    area_infos = pickle.load(open('D:/py3code/ArticleSpider/areaid.json', "rb"))
    area_list = []
    # .values()返回dict中的value,
    for area_info in area_infos.values():
        for list in area_info[1:]:
            area_list.append(list)
    count = 0
    for i in area_list:
        count += 1
        print("抓取第%d个区域: " % count, i["regionName"], '店铺总数：', i['count'])
        try:
            crawl_id(i["id"])
        except Exception as e:
            print(e)




# coding:utf-8


# 1.使用selenium获取cookie,这里为了方便直接复制cookie
# 2.构造详情页的url,传入ct_poi和店铺id
import csv
import json
import threading
import time

import requests
from lxml import etree


def  stwich_ip():
    ip_list = [{"https": "https://21515:81561"}, {"https": "https://21515:81561"}, {"https": "https://21515:81561"}]
    ip = ip_list.pop(0)
    return ip

# t=线程号, u=url_list
def thread_logic(t, u):
    proxy_ip = stwich_ip()
    lock = threading.Lock()
    count = 0
    while True:
        if len(u) > 0:
            u_list = u.pop(0)
            mark, info_list = parse(t, u_list, proxy_ip)
            if mark == 1:  # 拒绝连接错误,应更换IP
                stwich_ip()
                mark, info_list = parse(t, u_list, proxy_ip)
                if mark != 0:
                    count += 1
            if mark == 2:  # 其他错误
                mark, info_list = parse(t, u_list, proxy_ip)
                if mark != 0:
                    count += 1
            if mark == 0:  # 抓取成功则存储到meituan_info.csv
                count = 0
                lock.acquire()
                with open("meituan_info.csv", "w", newline="") as f:
                    write = csv.writer(f)
                    write.writerow(info_list)
                lock.release()
            if count > 2:
                count = 0
                proxy_ip = stwich_ip()
        else:
            print("结束")
            break




def parse(thread ,u, proxy_ip):
    mark = 0
    list_info = []
    headers = {
        'Host': 'meishi.meituan.com',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        "Referer": "https://meishi.meituan.com/i/?ci=20&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Mobile Safari/537.36",
        "Cookie": "__mta=219060518.1558835798686.1559115452678.1559115880819.34; _lxsdk_cuid=16af1d98b3259-0cd7a15037f40c-e353165-144000-16af1d98b35c8; iuuid=8E14ECDCC3918400D21FE63B62DBCE2FE13527D5A6385060410137D542551935; rvct=1; _lxsdk=8E14ECDCC3918400D21FE63B62DBCE2FE13527D5A6385060410137D542551935; webp=1; _hc.v=a961be8d-f4b9-40b2-3038-b7ba99924960.1558835798; __utmz=74597006.1558886434.4.3.utmcsr=meishi.meituan.com|utmccn=(referral)|utmcmd=referral|utmcct=/i/; client-id=f862ddc2-9dc4-40fe-a2f8-2238f5c5f884; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; cityname=%E5%B9%BF%E5%B7%9E; ci=20; IJSESSIONID=171vmqwy7g1w51nf21nf2tsxtn; __utmc=74597006; ci3=1; uuid=570078a3-bb88-432f-bb41-71ceb71f9970; logan_custom_report=; __utma=74597006.115702913.1558835739.1559112621.1559115029.10; logan_session_token=smjp35kgyomywl42wg3n; latlng=23.280772,113.723712,1559116158212; __utmb=74597006.8.9.1559116170517; i_extend=C_b1Gimthomepagecategory11H__a; _lxsdk_s=16b025a99a5-da4-ced-3ae%7C%7C34"
    }
    try:
        res = requests.get(u[0], headers=headers)
        time.sleep(10)
        print("抓取店铺:%s" % u[1])
        html = etree.HTML(res.text)
        html_text = html.xpath("body/script[@crossorigin='anonymous']")
        for data in html_text:
            text1 = data.text
            try:
                if "window._appState" in text1:
                    s = text1[19:-1]
                    json_text = json.loads(s)
                    name = json_text["poiInfo"]["name"]
                    tag = u[2]
                    address = json_text["poiInfo"]["addr"]
                    phone = json_text["poiInfo"]["phone"]
                    open_info = json_text["poiInfo"]["openInfo"]
                    avg_price = json_text["poiInfo"]["avgPrice"]
                    avg_score = json_text["poiInfo"]["avgScore"]
                    marknumbers = json_text["poiInfo"]["MarkNumbers"]
                    lng = json_text["poiInfo"]["lng"]
                    lat = json_text["poiInfo"]["lat"]
                    list_info = [name, tag, address, phone, open_info, avg_price, avg_score, marknumbers, lng, lat]
            except:
                pass
    except Exception as e:
        # 这部分是要判断抓取出错的种类,由mark区分(mark=0抓取成功,mark=1一类错,mark=2另一类错)
        print("error thread:", thread)
        print(e)
        s = str(e)[-22:-6]
        if e == "由于目标计算机积极拒绝，无法连接":
            print('由于目标计算机积极拒绝，无法连接', thread)
            mark = 1
        else:
            mark = 2
    return mark, list_info



if __name__ == "__main__":
    url_list = []
    with open("D:/py3code/ArticleSpider/ArticleSpider/other_spider/url_parameter.csv", "r", encoding="gb18030") as f:
        read = csv.reader(f)
        for data in read:
            url1 = ["", "", ""]
            url = 'https://meishi.meituan.com/i/poi/' + str(data[2]) + '?ct_poi=' + str(data[3])
            url1[0] = url
            url1[1] = data[0]
            url1[2] = data[1]
            url_list.append(url1)


    thread_list = []
    for i in range(1, 6):
        thread = threading.Thread(target=thread_logic, args=(i, url_list,))
        thread.start()
        thread_list.append(thread)
        time.sleep(30)

    for t in thread_list:
        t.join()









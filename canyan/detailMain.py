import requests
import re
import json
import random
import pymongo
import pymysql
import time
# import pymysql.cursors
#__init__.py
import sys
from multiprocessing import Pool
# import Requestdef
from bs4 import BeautifulSoup

sys.setrecursionlimit(100000)

hds = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
{'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
{'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
{'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},
{'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},
{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
{'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},
{'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},
{'User-Agent': 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]

sessionId = 'wx_97f186423a0a8d5a1e0e5ac3608d21be'
# 存储在mongodb
# client = pymongo.MongoClient(host='localhost', port=27017)
# db = client['mealplan']

# 存储到mysql
db = pymysql.connect(host = 'localhost', user = 'root', password = '1767421', port = 3306, db = "mealplan")
cursor = db.cursor()


def detail(target_list, dictMerged, param):
    newUrl2 = 'https://fa.kaoputou.com/api/waimai/shop/detail?id=' + target_list['id'] + '&month=9&platform=1'
    res2 = s.get(newUrl2, headers = dictMerged, data=json.dumps(param))
    res2 = json.loads(res2.content)

    print('===start')
    print(newUrl2)
    print(res2)
    print('===end')         
    if res2 and res2.get('record'):
        record = res2['record']
        # print(record)
        nowTime =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = "INSERT INTO new_shops(s_id, min_price, month, month_sales, new_products,   name, address, brand, category, city, delivery_type, discounts, hot_products, phone, platform, price, province, score, shipping_time, year, created_at) values(%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor.execute(sql, (record['id'], record['minPrice'], record['month'], record['monthSales'],json.dumps(record['newProducts']),
                    record['name'], record['address'],json.dumps(record['brand']),record['category'],
                    record['city'],record['deliveryType'],json.dumps(record['discounts']),
                    json.dumps(record['hotProducts']),record['phone'],record['platform'],
                    record['price'],record['province'],record['score'],
                    record['shippingTime'], record['year'], nowTime))
            db.commit()
        except Exception as err:
            print(err)
            db.rollback()
    return res2

def main(url, header, page, slug = '', param = {}, type = '', *args):
       newUrl = url + str(page)
       print(pc)
       print(newUrl)
       headers = hds[random.randint(0, len(hds) - 1)]
       dictMerged = headers.copy()
       dictMerged.update(header)
       requests.adapters.DEFAULT_RETRIES = 10 # 增加重连次数
       s = requests.session()
       s.keep_alive = False # 关闭多余连接
    #    time.sleep(int(random.random() * 4))
    #    time.sleep(100)
       # 开启IP代理池
       # proxy = 
    #    proxies = { "http": "http://"+str('103.129.237.5:2016') }    
        
        # Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
        # Accept-Encoding: gzip, deflate, br
        # Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
        # Cache-Control: max-age=0
        # Connection: keep-alive
        # Cookie: _lxsdk_cuid=1754bd0f2f0d-03c280a2cc3d99-c781f38-e1000-1754bd0f2f1c8; _hc.v=340666ae-4c7f-f7bc-5611-711d159bc456.1604115312; lsu=; uuid=b0f29e9803e14c2eb5d3.1604659901.1.0.0; _lxsdk=1754bd0f2f0d-03c280a2cc3d99-c781f38-e1000-1754bd0f2f1c8; ci=151; rvct=151%2C10%2C324%2C20%2C197; mtcdn=K; client-id=8f0919ef-f440-428a-9837-f125c964d86e; _lxsdk_s=175a8f531e2-edd-dae-877%7C%7C2
        # Host: diqing.meituan.com
        # Sec-Fetch-Dest: document
        # Sec-Fetch-Mode: navigate
        # Sec-Fetch-Site: none
        # Sec-Fetch-User: ?1
        # Upgrade-Insecure-Requests: 1
        # User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36
        # Referrer Policy: strict-origin-when-cross-origin

        #     dictMerged.update({ 'Cookie': '_lxsdk_cuid=1754bd0f2f0d-03c280a2cc3d99-c781f38-e1000-1754bd0f2f1c8; _hc.v=340666ae-4c7f-f7bc-5611-711d159bc456.1604115312; lsu=; uuid=b0f29e9803e14c2eb5d3.1604659901.1.0.0; _lxsdk=1754bd0f2f0d-03c280a2cc3d99-c781f38-e1000-1754bd0f2f1c8; ci=151; rvct=151%2C10%2C324%2C20%2C197; mtcdn=K; client-id=8f0919ef-f440-428a-9837-f125c964d86e; _lxsdk_s=175a8f531e2-edd-dae-877%7C%7C2' })

        #     print(dictMerged)
        #     proxy = "113.116.50.182:808"
        #     proxies = {
        #         "http":"http://"+proxy,
        #         "https":"https://"+proxy,
        #     }
        #    res = s.get(newUrl, headers = dictMerged, data=json.dumps(param), proxies=proxies)
        p = pc[0]
        cookie=pc[1]
        dictMerged.update({
            'Cookie': cookie
        })
        # dictMerged.update({
        #     'Host': 'fa.kaoputou.com',
        #     'appVersion': '0.1.3',
        #     'channel': 'weapp',
        #     'identity': 0,
        # })
       res = s.get(newUrl, headers = dictMerged, data=json.dumps(param), proxies=p)
       res = json.loads(res.content)
       print(res)

       if type == '':
              if res and res.get('shops') and res.get('shops').get('records'):
                     list = res['shops']['records']
                     for target_list in list:
                            time.sleep(int(random.random() * 4))
                            res2 = detail(target_list, dictMerged, param)
                            if res2.get('error'):
                                time.sleep(int(random.random() * 4))
                                detail(target_list, dictMerged, param)
              if res and res.get('shops') and isinstance(res.get('shops').get('records'), list) and len(res.get('shops').get('records')) == 0:
                sql = "update new_brands set `is_p` = 1 where slug  = " + slug
                cursor.execute(sql)
                db.commit()
              if res and res.get('shops') and res.get('shops').get('records') and page != 0:
                     page = page + 1
                     main(
                            url = url,
                            header = header,
                            page = page,
                            slug = slug,
                     )
       return res

sql = "select `slug` from new_brands where is_p is null"
cursor.execute(sql)
results = cursor.fetchall()
# pool = Pool(processes = 1) 
pc = get_cookie()
for target_list in results:
    # pool.apply_async(main, args = (
    #    'https://fa.kaoputou.com/api/brand/' + target_list[0] +'/waimai-detail?platform=1&province=&city=&page=',
    #    { 'sessionId': sessionId },
    #    1,
    #    target_list[0]
    # ))
    main(
       'https://fa.kaoputou.com/api/brand/' + target_list[0] +'/waimai-detail?platform=1&province=&city=&page=',
       { 'sessionId': sessionId },
       1,
       target_list[0],
       {},
       '',
       pc
    )
    pass
pool.close()
pool.join()

def IPList_61():
  for q in [1,2]:
       url='http://www.66ip.cn/'+str(q)+'.html'
       requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
       s = requests.session()
       s.keep_alive = False # 关闭多余连接
       r = s.get(url=url, headers=hds[random.randint(0, len(hds) - 1)])
       html = r.content
       iplist=BeautifulSoup(html, 'html.parser')
       iplist=iplist.find_all('tr')
       i=2
       for ip in iplist:
             if i<=0:
                 loader=''
              #    print(ip)
                 j=0
                 for ipport in ip.find_all('td',limit=2):
                     if j==0:
                        loader+=ipport.text.strip()+':'
                     else:
                         loader+=ipport.text.strip()
                         print(loader)
                         return loader
                     j=j+1
              #    Requestdef.inspect_ip(loader)
             i=i-1
#       time.sleep(1)

# IPList_61()
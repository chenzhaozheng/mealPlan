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

sessionId = 'wx_b126bd8dccb4f83d2af8b210b11b9926'
# 存储在mongodb
# client = pymongo.MongoClient(host='localhost', port=27017)
# db = client['mealplan']

# 存储到mysql
db = pymysql.connect(host = 'localhost', user = 'root', password = '1767421', port = 3306, db = "mealplan")
cursor = db.cursor()

def main(url, header, page, slug = '', param = {}, type = '', *args):
       newUrl = url + str(page)
       print(newUrl)
       headers = hds[random.randint(0, len(hds) - 1)]
       dictMerged = headers.copy()
       dictMerged.update(header)
       requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
       s = requests.session()
       s.keep_alive = False # 关闭多余连接
       res = s.get(newUrl, headers = dictMerged, data=json.dumps(param))
       res = json.loads(res.content)
       if type == '':
              if res and res.get('shops') and res.get('shops').get('records'):
                     list = res['shops']['records']
                     for target_list in list:
                            # console.log(key)
                            newUrl2 = 'https://fa.kaoputou.com/api/waimai/shop/detail?id=' + target_list['id'] + '&month=9&platform=1'
                            print(newUrl2)
                            res2 = s.get(newUrl2, headers = dictMerged, data=json.dumps(param))
                            res2 = json.loads(res2.content)
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
                            pass
              else: 
                #   ql = "UPDATE customers SET address = 'Canyon 123' WHERE address = 'Valley 345'"
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
pool = Pool(processes = 1) 
for target_list in results:
    pool.apply_async(main, args = (
       'https://fa.kaoputou.com/api/brand/' + target_list[0] +'/waimai-detail?platform=1&province=&city=&page=',
       { 'sessionId': sessionId },
       1,
       target_list[0]
    ))
    pass
pool.close()
pool.join()

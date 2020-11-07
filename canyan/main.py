import requests
import re
import json
import random
import pymongo
import pymysql
import time
# import pymysql.cursors

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

def main(url, header, page, param = {}, type = '', *args):
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
       # 店铺排名查询
       # sql = "INSERT INTO shops(name,category,s_id,month_sales,price,score,created_at) values(%s,%s,%s,%s,%s,%s,%s)"
       # try:
       #        cursor.execute(sql, (target_list['name'],target_list['category'],target_list['id'],target_list['monthSales'],target_list['price'],target_list['score'], nowTime))
       #        db.commit()
       # except:
       #        db.rollback()
       # 品牌信息查询
       
       if type == 'category':
              if res['records']:
                     list = res['records']
                     # for target_list in list:
                     #        # console.log(key)
                     #        nowTime =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                     #        # id count is_hot name parent slug
                     #        sql = "INSERT INTO categories(count, is_hot, name, parent, slug) values(%s,%s,%s,%s,%s)"
                     #        try:
                     #               cursor.execute(sql, (target_list['count'],target_list['isHot'],target_list['name'],
                     #                      target_list['parent'],target_list['slug']))
                     #               db.commit()
                     #        except:
                     #               db.rollback()
                     #        pass
       if type == 'city':
              # print(res['cityMap'])
              if res['cityMap']:
                     list = res['cityMap']
                     # print(list)
                     for key, target_list in list.items():
                            # print(target_list)
                            # print(key)
                            nowTime =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())   
                            # cityMap
                            # for target_list2 in target_list:
                            #        sql = "INSERT INTO citys(name, province) values(%s,%s)"
                            #        try:
                            #               cursor.execute(sql, (target_list2, key))
                            #               db.commit()
                            #        except:
                            #               db.rollback()
                            #        pass
                            # pass
       if type == '':
              if res and res.get('records'):
                     list = res['records']
                     for target_list in list:
                            # console.log(key)
                            nowTime =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                            sql = "INSERT INTO new_brands(company, categories, close_count, evaluation, good_rate, name, open_count, slug, created_at) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                            try:
                                   cursor.execute(sql, (target_list['company'],target_list['categories'],target_list['closeCount'],
                                          target_list['evaluation'],target_list['goodRate'],target_list['name'],target_list['openCount'],target_list['slug'], nowTime))
                                   db.commit()
                            except:
                                   db.rollback()
                            pass
              if res and res.get('records') and page != 0:
                     page = page + 1
                     main(
                            url = url,
                            header = header,
                            page = page,
                            param = param
                     )
       return res

cityRes = main(
       url = 'https://fa.kaoputou.com/api/brand/city-map',
       header = { 'sessionId': sessionId },
       page = '',
       type = 'city'
)['cityMap']

categoryRes = main(
       url = 'https://fa.kaoputou.com/api/categories',
       header = { 'sessionId': sessionId },
       page = '',
       type = 'category'
)['records']

print(cityRes)
print(categoryRes)

# 多级分类筛选
lock = 'true'
lastKey = '青海省'
cityLock = 'true'
lastCity = ''
for cityKey, citys in cityRes.items():
       if cityKey == lastKey:
           lock = 'false'
       for city in citys:
              if city == lastKey:
                     cityLock = 'false'
                     lastCity = city
       if lock == 'false' or cityLock == 'false':
            if lock == 'false':
              main(
                     url = 'https://fa.kaoputou.com/api/brands/ranking?category=&price=&region=' + cityKey + '&sort_key=shop_count&page=',
                     header = { 'sessionId': sessionId },
                     page = 1,
              )
              for category in categoryRes:
                     main(
                                   url = 'https://fa.kaoputou.com/api/brands/ranking?category=' + category['name'] + '&price=&region=' + cityKey + '&sort_key=shop_count&page=',
                                   header = { 'sessionId': sessionId },
                                   page = 1, 
                     )
              cityLock = 'false'
              lock = 'false'
            for city in citys:
                   if cityLock == 'false' and lastCity == city :
                     main(
                                   url = 'https://fa.kaoputou.com/api/brands/ranking?category=&price=&region=' + city + '&sort_key=shop_count&page=',
                                   header = { 'sessionId': sessionId },
                                   page = 1,
                     )
                     for category in categoryRes:
                                   main(
                                          url = 'https://fa.kaoputou.com/api/brands/ranking?category=' + category['name'] + '&price=&region=' + city + '&sort_key=shop_count&page=',
                                          header = { 'sessionId': sessionId },
                                          page = 1, 
                                   )
                     cityLock = 'false'
                     lock = 'false'
                     lastCity = city
                     pass
            # region=广东省
            # region=广州
       pass

# 全国无筛选查询
# main(
#        # url = 'https://fa.kaoputou.com/api/waimai/ranking?platform=1&province=全国&city=&category=全部&sort_type=1&month=9&page=',
#        url = 'https://fa.kaoputou.com/api/brands/ranking?category=&price=&region=&sort_key=shop_count&page=',
#        header = { 'sessionId': sessionId },
#        page = 1,
# )


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


# 存储在mongodb
# client = pymongo.MongoClient(host='localhost', port=27017)
# db = client['mealplan']

# 存储到mysql
db = pymysql.connect(host = 'localhost', user = 'root', password = '1767421', port = 3306, db = "mealplan")
cursor = db.cursor()

def getCategory(url):
    res = requests.get(url=url, headers=hds[random.randint(0, len(hds) - 1)])
    html = res.content
    bHtml = BeautifulSoup(html, 'html.parser')
    page_items = bHtml.find_all('div', attrs={'class': 'p-list'})
    print(page_items)
def main(url, header, page, param, *args):
       newUrl = url + str(page)
       print(newUrl)
       headers = hds[random.randint(0, len(hds) - 1)]
       dictMerged = headers.copy()
       dictMerged.update(header)
       res = requests.get(url=url, headers=hds[random.randint(0, len(hds) - 1)])
       html = res.content
       bHtml = BeautifulSoup(html, 'html.parser')
       page_items = bHtml.find_all('div', attrs={'class': 'p-list'})
       print(page_items)
       print(res)
       if res['records']:
              list = res['records']
              for target_list in list:
                     nowTime =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                     # print(nowTime)
                     sql = "INSERT INTO shops(name,category,s_id,month_sales,price,score,created_at) values(%s,%s,%s,%s,%s,%s,%s)"
                     try:
                            cursor.execute(sql, (target_list['name'],target_list['category'],target_list['id'],target_list['monthSales'],target_list['price'],target_list['score'], nowTime))
                            db.commit()
                     except:
                            db.rollback()

                     
                     pass
       
       if res['hasNext']:
              page = page + 1
              main(
                     url = url,
                     header = header,
                     page = page,
                     param = param
              )

main(
       url = 'https://www.meituan.com/changecity/',
)


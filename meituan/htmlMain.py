# 9005安控
import requests
import random
from bs4 import BeautifulSoup
import pymysql

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

# 存储到mysql
db = pymysql.connect(host='localhost', user='root',
                     password='1767421', port=3306, db="mealplan")
cursor = db.cursor()

def getCity():
    url = 'https://www.meituan.com/changecity/'
    r = requests.get(url=url, headers=hds[random.randint(0, len(hds) - 1)])
    html = r.content
    lj = BeautifulSoup(html, 'html.parser')
    # print(lj)
    items = lj.find_all('span', attrs={'class': 'cities'})
    # print(items)
    # meituan_cities
    for item in items:
        items2 = item.find_all('a', attrs={'class': 'city'})
        for item2 in items2:
            sql = "INSERT INTO meituan_cities(url, name) values(%s,%s)"
            try:
                cursor.execute(sql, (item2.get('href'), item2.text))
                db.commit()
            except:
                db.rollback()
            pass
        pass

def getShops(name = '', url = '', page = 1):
    # print('执行getShops', name, url, page)
    tempUrl = 'https:' + url + '/meishi/'
    newUrl = tempUrl
    if page > 1:
        newUrl = newUrl + 'pn' + str(page) + '/'
        print(newUrl)
    requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
    s = requests.session()
    s.keep_alive = False # 关闭多余连接
    # print(html)
    try:
        r = s.get(url=newUrl, headers=hds[random.randint(0, len(hds) - 1)])
        html = r.content
        lj = BeautifulSoup(html, 'html.parser')
        items = lj.find_all('li')
        #  attrs={'class': 'list'}).find_all('li'
        print(items)
        for item in items:
            item2 = item.find('a')
            item3 = item.find('p', attrs={'class': 'name'})
            if item2 and item3:
                print(item2.get('href'))
                print(item3)
                sql = "INSERT INTO meituan_shops(name, addr, url, shop_id, city, page) values(%s,%s,%s,%s,%s,%s)"
                try:
                    cursor.execute(sql, (item3.get_text(), '', item2.get('href'), item2.get('href').split('/')[2], name, page))
                    db.commit()
                except:
                    db.rollback()
            pass
        # https://ay.meituan.com/meishi/api/poi/getPoiList?cityName=%E5%AE%89%E9%98%B3&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=4&
        # userId=&uuid=8219470054d74685bf46.1604541483.1.0.0&platform=1&partner=126&originUrl=https%3A%2F%2Fay.meituan.com%2Fmeishi%2Fpn4%2F&riskLevel=1&optimusCode=10&
        # _token=eJxVkE1TgzAURf9LtjIlfISE7oTaFgpiaalYxwUCBVrDV2grcfzvxlEXzryZe3PeWbzJB%2BidDEwVCE0IJXDJezAFygRODCCBgYmNAXWEsKYSFWkSSP8zXcESeO13MzB9VlQCJQXBl28SCvBDsCrITzVMUVVdzLfjCAWUw9CyqSwn44Tm1XBO6knaUFl0VlZyW%2BuyuAMInW6FLvL0m8lvDn9vXxwuXFYVtWi5e33jWyW45XdrK7dxu5y1Nbfx496m6xVdO8cmeApc16ee6WgsXUWHwmpHuzzeh%2BktY909ih88VSP7mETQ7o9vuFmOo7Z%2FJ%2B6Fy4cDN252gR11AeJb2WmiU7ZEGyfNzUu9Dio2tvFDPcddVeYhLA2fbNOsSmLcOgTR81x92vmbxTwmNLQWO4tyw0v4qjvHkaGHddKnWoFgGz%2FqaNM1eRfI3NSR7rmKiW2eNatrodF9fCLXhGev1J9ZaZdn4ivPh2LReLBg4PMLx7GO4Q%3D%3D
        if len(items) != 0:
            page = page + 1
            print(page)
            getShops(name, url, page)
        # if 
        pass
    except:
        pass
   

def getShop(id = ''):
    url = 'https:'
    r = requests.get(url=url, headers=hds[random.randint(0, len(hds) - 1)])
    html = r.content
    lj = BeautifulSoup(html, 'html.parser')
    # print(lj)
    items = lj.find_all('span', attrs={'class': 'cities'})
    # print(items)
    # meituan_cities
    for item in items:
        items2 = item.find_all('a', attrs={'class': 'city'})
        for item2 in items2:
            sql = "INSERT INTO meituan_cities(url, name) values(%s,%s)"
            try:
                cursor.execute(sql, (item2.get('href'), item2.text))
                db.commit()
            except:
                db.rollback()
            pass
        pass

def main():
    # getCity()

    sql = "select `name`,`url` from meituan_cities"
    cursor.execute(sql)
    results = cursor.fetchall()
    for target_list in results:
        print(target_list)
        # target_list.name
        # target_list.url
        getShops(target_list[0], target_list[1])

main()




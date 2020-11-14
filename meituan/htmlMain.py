# 9005安控
import requests
import random
from bs4 import BeautifulSoup
import pymysql
import json

import re
from selenium import webdriver
from pyquery import PyQuery as pq
import zlib
import base64
import time

import urllib.parse

from multiprocessing import Pool


from getCookie import getCookie
from getCookie import getIp


class MakeToken():
    """
    测试2019-4-21日可用
    仅作为学术交流！如有侵权，联系作者删除
    美团【餐馆列表】Token生成
    """

    def __init__(self, areaId, cityName, originUrl, page, uuid):
        self.areaId = areaId
        self.cityName = cityName
        self.originUrl = originUrl
        self.page = page
        # self.uuid = 'c6eada3ffd8e444491e9.1555472928.3.0.0'  # Demo
        self.uuid = uuid

    def join_sign(self):
        # 参数
        # b'"areaId=0&cateId=0&cityName=\xe9\x9e\x8d\xe5\xb1\xb1&dinnerCountAttrId=&optimusCode=10&originUrl=https://as.meituan.com/meishi/&page=1&partner=126&platform=1&riskLevel=1&sort=&userId=&uuid=b0f29e9803e14c2eb5d3.1604659901.1.0.0"'

        sign = 'areaId={areaId}&cateId=0&cityName={cityName}&dinnerCountAttrId=&optimusCode=10&originUrl={originUrl}&page={page}&partner=126&platform=1&riskLevel=1&sort=&userId=&uuid={uuid}'
        _str = sign.format(areaId=self.areaId, cityName=self.cityName, originUrl=self.originUrl, page=self.page,
                           uuid=self.uuid)
        # print(_str)
        sign = base64.b64encode(zlib.compress(
            bytes(json.dumps(_str, ensure_ascii=False), encoding="utf8")))
        sign = str(sign, encoding="utf8")
        return sign

    @property
    def join_token(self):
        str_json = {}
        str_json['rId'] = 100900
        str_json['ver'] = '1.0.6'
        str_json['ts'] = int(time.time() * 1000)
        # str_json['cts'] = time.time() + 110
        str_json['cts'] = int(time.time() * 1000) + 62
        # str_json['brVD'] = [1920, 315]
        # str_json['brR'] = [[1920, 1080], [1920, 1057], 24, 24]
        str_json['brVD'] = [440, 531],
        str_json['brR'] = [[1280, 720], [1280, 690], 24, 24]
        str_json['bI'] = [self.originUrl, ""]
        str_json['mT'] = []
        str_json['kT'] = []
        str_json['aT'] = []
        str_json['tT'] = []
        str_json['aM'] = ''
        str_json['sign'] = self.join_sign()
        # str_json['sign'] = 'eJwljb0NwjAQhXehcOnYCYkIkgtEhYToGMDEB5yI7eh8RmIIVmCHDEXBFlhQvU9P72dhCezOGSUGy/AH5MfBejCf1/M9z8JhCEDbmANvmKlkRJwYfU7b6MBoJSLhBcORRnNlntK6qmySHpCzDXKIviqcrliJyV5KoQhxmTS67sQ0Wj5H8sUmTLc93GEsnCKxETnB7y9ndOakznUP/Uo1oJdDDafWNVJ3atm1fa+01FJJtfgCoT5H1A=='
        # token_decode = zlib.compress(
        #     bytes(json.dumps(str_json, separators=(',', ':'), ensure_ascii=False), encoding="utf8"))
        # token = str(base64.b64encode(token_decode), encoding="utf8")
        # print(str_json)
        token_decode = zlib.compress(
            bytes(json.dumps(str_json), encoding="utf8"))
        token = str(base64.b64encode(token_decode), encoding="utf8")
        return token


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

sym = 0


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


def getShops(name='', url='', page=1, pc=''):
    # print('执行getShops', name, url, page)
    # tempUrl = 'https:' + url + '/meishi/'

    # https://anshun.meituan.com/meishi/api/poi/getPoiList?cityName=%E5%AE%89%E9%A1%BA&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1&userId=&uuid=b0f29e9803e14c2eb5d3.1604659901.1.0.0&platform=1&partner=126&originUrl=https%3A%2F%2Fanshun.meituan.com%2Fmeishi%2F&riskLevel=1&optimusCode=10&_token=eJxVjktvqkAYhv%2FLbEtkRu4mXYCDClUUvKFNFwgjgwhYGERszn8%2F05yeRZMveS%2Ffs3i%2FQO0kYIQgNCAUwJ3UYATQAA5UIADW8I8KZU2GEtI0xIH4d6cbsgBO9Q6D0bs6VARFQh%2FfRcDzOxrqUNCG8EP4Z1WD26HM75txOAIoY7dmJIpR2dC2HBQkY21UDuKqELlvaCbyGYDjxYbjXPMfjX6U%2Fc8LvpuzTZaW3BG3u15O0Osupk9DQuNleRhvfbv395mfuxBPcZYqvaMRqgeFYz8K07IK8zyuT2ba3gxSVuICspTpcgV37XTV47PBIkw24r3Uk%2FnS7KzI8p4y3j6vh96x1dUqChbJ9A3ZLn5clp5VWe3hVkf1G71scgfD9Phg%2BUxCu6WJDllckLWaO%2FExR22hTbxJ9RKc5xM378PZ7kHnbpc1ga10RH8epU3xaSvIMtDai3B59qUZ3bf5ie31MFwn8OrO3SRsxuLLdn10XsGfvzgXjUg%3D
    # originUrl = 'https%3A%2F%2Fanshun.meituan.com%2Fmeishi%2F'
    try:

        originUrl = urllib.parse.quote('https:' + url + '/meishi/', '')
        cityName = urllib.parse.quote(name, '')
        areaId = '0'
        # uuid = 'b0f29e9803e14c2eb5d3.1604659901.1.0.0'
        # uuid = '69f4a10f-a7ab-4337-8666-1edcf8b2ead9'
        uuid = pc[2]
        tempUrl = 'https:' + url + '/meishi/' + 'api/poi/getPoiList?cityName=' + cityName + '&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=' + \
            str(page) + '&userId=&uuid=' + uuid + '&platform=1&partner=126&originUrl=' + \
            originUrl + '&riskLevel=1&optimusCode=10'
        newUrl = tempUrl
        # if page > 1:
        #     # newUrl = newUrl + 'pn' + str(page) + '/'
        #     newUrl = newUrl + '&page=' + str(page)
        # newUrl = newUrl + '&page=' + str(page)

        # 测试数据
        # originUrl = 'http://cq.meituan.com/meishi/b4581/'
        token = MakeToken(areaId, name, 'https:' +
                          url + '/meishi/', page, uuid)
        # print(token.join_token)
        if token.join_token:
            newUrl = newUrl + '&_token=' + urllib.parse.quote(token.join_token, '')

        print(newUrl)
        # print('===')

        requests.adapters.DEFAULT_RETRIES = 15  # 增加重连次数
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接

        # print(html)

        # print(newUrl)

        # browser = webdriver.Chrome()
        # browser.get(newUrl)
        # html = browser.page_source
        # data = str(pq(html))
        # print(data)

        # %E9%9E%8D%E5%B1%B1
        # newUrl = 'https://as.meituan.com/meishi/api/poi/getPoiList?c
        # ityName=%E9%9E%8D%E5%B1%B1&cateId=0&areaId=0&sort=&dinnerCountAttrId=&pa
        # ge=1&userId=&uuid=b0f29e9803e14c2eb5d3.1604659901.1.0.0&platform=1&partner=126
        # &originUrl=https%3A%2F%2Fas.meituan.com%2Fmeishi%2F&riskLevel=1&optimusCode=10&
        # _token=eJxVjltvgjAYhv9Lb0ekRaFgsgs5TChDJ4KHLLtABIvQskmnw2X%2FfV3mLpZ8yXv4nov3E5yCPRgjCC0IF
        # XAuTmAM0AAODKAA0cmPAUdYNzUdYcNSQP6v0zA0FbA7rVwwfh6NoKIP0ctPEcv8jDQTKliDL8qvNSxptZG8HyaQ
        # CKBCvHZjVc26ASsq8Z7xQd4yVfqOVqqcACTKEolKrW%2Ba3VT85UhulmxXHbh0Bbk0xx2cXY6TBd0UNJ%2FzrbOtg%2F
        # ogPLpN2mnkerbeB7igZsyCYMUc3%2FU29kNDF%2BfUesLanjrFdT5dptNenfh6VNrF0SmRGllXk1DHc3dsMjuzsKljctmW
        # Kd4Zkd2S5SO183kc81nDRWi8sX7pvzpXdxMG5%2BotPzUV6Vd62C7oB0uWBu4WcH3UfbNLWfKYW8Op13En%2FPASbu
        # Pe4vt5Vl95%2BqSmLWrJ3nWzcj1bkWEmGCqzO4geCBHlwWkT3UeT%2B3vw9Q0Wy4nM'

        # https://as.meituan.com/meishi/api/poi/getPoiList?city
        # Name=%E9%9E%8D%E5%B1%B1&cateId=0&areaId=0&sort=&dinnerCo
        # untAttrId=&page=1&userId=&uuid=b0f29e9803e14c2eb5d3.1604659901.1.0.0&
        # platform=1&partner=126&originUrl=https%3A%2F%2Fas.meituan.com%2Fmeishi
        # %2F&riskLevel=1&optimusCode=10&_token=eJxNjl1vgjAUhv9Lb0egVcuHyS7kY0IZOhGcZ
        # vECESxCyyadDpf993XZli05yfue5zwX5x2cgj0YIwgtCBVwLk5gDJAKVR0oQHTyosORgc2hDlU4GOk
        # QKyD%2Fx0fGH9%2BdVi4YPyFrAJUhwtsvEkvwTRA04Vb57djYKoORnC8rkBKgQjx3Y03LOpUVlXjNuJq3TJO9o5UmvwFSZYlUZdY%2Fmf2k%2BN0j%2Bb50u%2BrAZSvIpTn
        # u4OxynCzouqD5nG%2BcTR3UB%2BHRTdJOI9ezcR8YBTVjFgQr5viut7bvGro4p9aDMdhT
        # p7jOp8t02msTH0elXRydEmmRdTUJdTx3xyazMwubOiaXTZkaOz2yW7K8p3Y%2Bj2M%2Ba
        # 7gI9RfWL%2F1n5%2Bquw%2BBcveSnpiL9Coftgr6xZKkb3QI%2BHrFvdilL7nNrOPU67oRvXsJto7f4fp7VV5
        # 4%2BaGmLWrJ33ax8nK3IMBMMldkNRHeEiPLgtAn20eT2Fnx8AvqKi9w%3D

        # time.sleep(3)
        # proxy = "183.63.188.250:8808"
        # proxies = {
        #     "http":"http://"+proxy,
        #     "https":"https://"+proxy,
        # }
        headers = hds[random.randint(0, len(hds) - 1)]
        dictMerged = headers.copy()
        dictMerged.update(headers)
        # dictMerged.update({

        # Cookie: _lxsdk_cuid=1754bd0f2f0d-03c280a2cc3d99-c781f38-e1000-1754bd0f2f1c8;
        #  _hc.v=340666ae-4c7f-f7bc-5611-711d159bc456.1604115312;
        #  lsu=; uuid=b0f29e9803e14c2eb5d3.1604659901.1.0.0;
        #  _lxsdk=1754bd0f2f0d-03c280a2cc3d99-c781f38-e1000-1754bd0f2f1c8;
        #   mtcdn=K; ci=1; rvct=1%2C151%2C10%2C324%2C20%2C197;
        #    __mta=212276779.1604859290311.1604859290311.1604859290311.1;
        #     client-id=e0854918-aa85-4a02-8bcd-7d07a703d55f;
        #     _lxsdk_s=175a910d33d-2c9-17f-6f8%7C%7C11

        #   'Cookie': '_lxsdk_cuid=1754bd0f2f0d-03c280a2cc3d99-c781f38-e1000-1754bd0f2f1c8;
        # _hc.v=340666ae-4c7f-f7bc-5611-711d159bc456.1604115312;
        # lsu=;
        # uuid=b0f29e9803e14c2eb5d3.1604659901.1.0.0;
        #  _lxsdk=1754bd0f2f0d-03c280a2cc3d99-c781f38-e1000-1754bd0f2f1c8;
        #   ci=151;
        #   rvct=151%2C10%2C324%2C20%2C197; mtcdn=K
        #   ; client-id=8f0919ef-f440-428a-9837-f125c964d86e;
        #    _lxsdk_s=175a8f531e2-edd-dae-877%7C%7C2'
        # })

        p = pc[0]
        cookie = pc[1]

        dictMerged.update({
            # 'Host': 'diqing.meituan.com',
            # 'Connection': 'keep-alive',
            # 'Cache-Control': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            # 'Postman-Token': '30183d22-bebd-dd59-1814-06e09dc84c23',
            # 'Accept': '*/*',
            # 'Sec-Fetch-Site': 'none',
            # 'Sec-Fetch-Mode': 'cors',
            # 'Sec-Fetch-Dest': 'empty',
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cookie': cookie
        })

        # print(dictMerged)
        # try:
        r = s.get(url=newUrl, headers=dictMerged, proxies=p)
        r = json.loads(r.content)
        # pass
        # except Exception:
        #     newPc = [  getIp(), cookie ]
        #     getShops(name, url, page, newPc)
        #     pass

        print(r)

        if r.get('data') and r['data']['poiInfos']:
            for item in r['data']['poiInfos']:
                print('===')
                print(item)
                sql = "INSERT INTO meituan_shops(name, addr, url, shop_id, city, page) values(%s,%s,%s,%s,%s,%s)"
                try:
                    n = cursor.execute(
                        sql, (item['title'], item['address'], '', item['poiId'], name, page))
                    print('succ')
                    print(n)
                    db.commit()
                except Exception as err:
                    print('except')
                    print(err)
                    db.rollback()
        global sym

        if sym > 3:
            sym = 0
            pc = getCookie()

        if r.get('code') == 406:
            sym = sym + 1
            getShops(name, url, page, pc)
        if r.get('data') and len(r['data']['poiInfos']) != 0:
            page = page + 1
            print(page)
            getShops(name, url, page, pc)

        # proxies = { "http": "http://"+str('103.129.237.5:2016') }

        # print(r)
        # print()
        # html = r.content
        # lj = BeautifulSoup(html, 'html.parser')
        # items = lj.find_all('li')
        # #  attrs={'class': 'list'}).find_all('li'
        # print(items)
        # for item in items:
        #     item2 = item.find('a')
        #     item3 = item.find('p', attrs={'class': 'name'})
        #     if item2 and item3:
        #         print(item2.get('href'))
        #         print(item3)
        #         sql = "INSERT INTO meituan_shops(name, addr, url, shop_id, city, page) values(%s,%s,%s,%s,%s,%s)"
        #         try:
        #             cursor.execute(sql, (item3.get_text(), '', item2.get('href'), item2.get('href').split('/')[2], name, page))
        #             db.commit()
        #         except:
        #             db.rollback()
        #     pass

        # https://ay.meituan.com/meishi/api/poi/getPoiList?cityName=%E5%AE%89%E9%98%B3&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=4&
        # userId=&uuid=8219470054d74685bf46.1604541483.1.0.0&platform=1&partner=126&originUrl=https%3A%2F%2Fay.meituan.com%2Fmeishi%2Fpn4%2F&riskLevel=1&optimusCode=10&
        # _token=eJxVkE1TgzAURf9LtjIlfISE7oTaFgpiaalYxwUCBVrDV2grcfzvxlEXzryZe3PeWbzJB%2BidDEwVCE0IJXDJezAFygRODCCBgYmNAXWEsKYSFWkSSP8zXcESeO13MzB9VlQCJQXBl28SCvBDsCrITzVMUVVdzLfjCAWUw9CyqSwn44Tm1XBO6knaUFl0VlZyW%2BuyuAMInW6FLvL0m8lvDn9vXxwuXFYVtWi5e33jWyW45XdrK7dxu5y1Nbfx496m6xVdO8cmeApc16ee6WgsXUWHwmpHuzzeh%2BktY909ih88VSP7mETQ7o9vuFmOo7Z%2FJ%2B6Fy4cDN252gR11AeJb2WmiU7ZEGyfNzUu9Dio2tvFDPcddVeYhLA2fbNOsSmLcOgTR81x92vmbxTwmNLQWO4tyw0v4qjvHkaGHddKnWoFgGz%2FqaNM1eRfI3NSR7rmKiW2eNatrodF9fCLXhGev1J9ZaZdn4ivPh2LReLBg4PMLx7GO4Q%3D%3D
        # if len(items) != 0:
        #     page = page + 1
        #     print(page)
        #     getShops(name, url, page)
        # # if
        # pass
        pass
    except Exception as err:
        print(err)
        # cookie = pc[1]
        # newPc = [getIp(), cookie]
        newPc = getCookie()
        getShops(name, url, page, newPc)
        pass


def getShop(id=''):
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
    pc = getCookie()
    # getCity()
    # pool = Pool(processes = 2)
    sql = "select `name`,`url` from meituan_cities where status = 0"
    cursor.execute(sql)
    results = cursor.fetchall()
    for target_list in results:
        print(target_list)
        # target_list.name
        # target_list.url
        getShops(target_list[0], target_list[1], 1, pc)

    #     pool.apply_async(getShops, args = (
    #         target_list[0],
    #         target_list[1]
    #     ))
    # pool.close()
    # pool.join()
main()

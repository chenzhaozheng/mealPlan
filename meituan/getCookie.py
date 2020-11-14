import requests
import json
from selenium import webdriver
import time

def getIp():
    try:
        p_url = 'https://api.xiaoxiangdaili.com/ip/get?appKey=644014467256307712&appSecret=CqKP7oR1&cnt=&wt=json'
        r = requests.get(p_url)
        print(r.content)
        html = json.loads(r.text)
        a = html['data'][0]['ip']
        b = html['data'][0]['port']
        # val = '--proxy-server=http://' + str(a) + ':' + str(b)
        val2 = 'https://' + str(a) + ':' + str(b)
        p = {'https': val2}
        print('获取IP：',p)
        return p
    except Exception:
        time.sleep(4)
        getIp()
        pass
    

def getCookie():
    mark=0
    print('fuck')
    try:
        while mark==0:
            #购买的ip获取地址
            p_url = 'https://api.xiaoxiangdaili.com/ip/get?appKey=644014467256307712&appSecret=CqKP7oR1&cnt=&wt=json'
            r = requests.get(p_url)
            print(r.content)
            html = json.loads(r.text)
            a = html['data'][0]['ip']
            b = html['data'][0]['port']
            val = '--proxy-server=http://' + str(a) + ':' + str(b)
            val2 = 'https://' + str(a) + ':' + str(b)
            p = {'https': val2}
            print('获取IP：',p)
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument(val)
            driver = webdriver.Chrome(executable_path='C:\\Program Files (x86)\\Python38-32\\chromedriver.exe', chrome_options=chrome_options)
            driver.set_page_load_timeout(8) #设置超时
            driver.set_script_timeout(8)
            url='https://i.meituan.com/shenzhen/'   #美团深圳首页
            url2='https://meishi.meituan.com/i/?ci=30&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1'#美食页面
            try:
                driver.get(url)
                time.sleep(2.5)
                c1=driver.get_cookies()
                now = time.time()
                driver.get(url2)
                tt=time.time()-now
                print(tt)
                time.sleep(0.5)
                #ip速度测试，打开时间大于3S的NG
                if tt < 3:
                    c=driver.get_cookies()
                    driver.quit()
                    print('*******************')
                    # print(c1)
                    # print(c)
                    print(len(c1),len(c))
                    #判断cookie是否完整，正常的长度应该是18
                    if len(c)>17:
                        mark=1
                        print('fuck')
                        print(c)
                        try:
                            x = {}
                            for line in c:
                                print(line['name'])
                                print(line['value'])
                                x[line['name']]=line['value']
                                # pass
                                #将cookie合成字符串，以便添加到header中，字符串较长就分了两段处理
                            # print('x')
                            # print(x)
                            # co1='__mta='+x['__mta']+'; client-id='+x['client-id']+'; IJSESSIONID='+x['IJSESSIONID']+'; iuuid='+x['iuuid']+'; ci=30; cityname=%E6%B7%B1%E5%9C%B3; latlng=; webp=1; _lxsdk_cuid='+x['_lxsdk_cuid']+'; _lxsdk='+x['_lxsdk']
                            # co2='; __utma='+x['__utma']+'; __utmc='+x['__utmc']+'; __utmz='+x['__utmz']+'; __utmb='+x['__utmb']+'; i_extend='+x['i_extend']+'; uuid='+x['uuid']+'; _hc.v='+x['_hc.v']+'; _lxsdk_s='+x['_lxsdk_s']
                            # co=co1+co2
                            co = ''
                            for line in x:
                                co = co + line + '=' + x[line] + ';'
                            print(co)
                            return(p,co,  x['uuid'])
                        except Exception as identifier:
                            print(identifier)
                            pass
                        x={}
                    
                    else:
                        print('缺少Cookie,长度：',len(c))
                else:
                    print('超时')
                    driver.quit()
                    time.sleep(3)
            except:
                driver.quit()
                pass
        pass
    except Exception:
        time.sleep(3)
        getCookie()
        pass
 
# getCookie()
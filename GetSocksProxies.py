# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 15:02:28 2018
curl --socks4 131.196.143.123:50489 http://ifcfg.co
@author: fuwen
"""

from bs4 import BeautifulSoup
import pymongo,requests,re,random,time,json

BilibiliIpUrl = 'https://api.live.bilibili.com/ip_service/v1/ip_service/get_ip_addr'
MyProxiesList = [{'https': 'https://127.0.0.1:1080'}, {'https': 'Socks5://144.34.181.207:1080'},{'https': 'Socks5://104.224.132.132:1080'}]


while True :
    myclient  = pymongo.MongoClient('mongodb://fuwenyue:pass4Top@ds029638.mlab.com:29638/socks_proxies')
    mydb = myclient['socks_proxies']
    ProxiesCol = mydb['Proxies']
    SavedProxiesList = ProxiesCol.find({},{ "_id": 0, "https": 1})
    SavedProxiesList = [Proxies for Proxies in SavedProxiesList]
    while True :
        print('正在尝试连接……')
        try :
            Proxies = random.choice(MyProxiesList)
            Response = requests.get('https://www.socks-proxy.net/',proxies = Proxies,timeout = 15)
            print('连接成功！')
            break
        except Exception :
            print('连接失败，即将重新尝试连接。')
    
    Soup = BeautifulSoup(Response.text, 'lxml')       
    IpTable = Soup.select('#proxylisttable > tbody > tr')
    IpList = [re.findall('<td>(.*?)</td>',str(IpRow)) for IpRow in IpTable]                      
    ProxiesList = [{'https':'%s://%s:%s'%(Ip[3],Ip[0],Ip[1])} for Ip in IpList]
    
    for Proxies in ProxiesList :
        if Proxies in SavedProxiesList :
            print('代理已存在，跳过……')
            continue
        else :
            pass
        try :
            Response = requests.get(BilibiliIpUrl ,proxies = Proxies, timeout=10)
            IpJson = json.loads(Response.text)
            country = IpJson['data']['country']
            province = IpJson['data']['province']
            city = IpJson['data']['city']
            Proxies['location'] = country + province + city
            Proxies['creattime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            Proxies['update'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            x = ProxiesCol.insert_one(Proxies)
            print('ProxiesSaved')
    
        except :
            print('ProxiesError')
    time.sleep(300)
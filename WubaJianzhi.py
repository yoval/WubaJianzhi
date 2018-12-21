# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pymongo, requests, random, time


def GetCityList() :
    CityCol = mydb['wubacity']
    CityUrlList = CityCol.find({},{ "_id": 0, "DetailUrl": 1})
    CityUrlList = [CityUrl['DetailUrl'] for CityUrl in CityUrlList]
    return CityUrlList

def GetProxiesList() :
    ProxiesCol = mydb['Proxies']
    ProxiesList = ProxiesCol.find().sort('update',-1).limit(500) # 降序，获取最新的代理
    ProxiesList = [{'https':Proxies['https']} for Proxies in ProxiesList]
    return ProxiesList

ua = UserAgent()
myclient  = pymongo.MongoClient('mongodb://fuwenyue:pass4Top@ds029638.mlab.com:29638/socks_proxies')
mydb = myclient['socks_proxies']
LocalClient= pymongo.MongoClient("mongodb://127.0.0.1:27017")
LocalDB = LocalClient["WuBaTongcheng"]
LocalCol = LocalDB["jianzhi"]
RecordDate = time.strftime("%Y-%m-%d", time.localtime())
UrlDicts = LocalCol.find({},{"_id": 0,"Link":1})
GettedUrlList = [UrlDict["Link"] for UrlDict in UrlDicts]
CityUrlList = GetCityList()
ProxiesList = GetProxiesList()

for CityUrl in CityUrlList :
    while True :
        print('正在获取城市页面内容……')
        try :
            Proxies = random.choice(ProxiesList)
            CityResponse = requests.get(CityUrl, headers = {"User-Agent":ua.random},proxies = Proxies, timeout = 20 )
            print('获取成功！')
            break
        except :
            ProxiesList.remove(Proxies)
            print('无法连接，已移除当前代理，当前剩余%d代理'%len(ProxiesList))
    CityResponse.encoding = 'utf-8'
    CityHtml = CityResponse.text
    CitySoup = BeautifulSoup(CityHtml,'lxml')
    if CitySoup.title.string == '请输入验证码':
        ProxiesList.remove(Proxies)
        print('需输入验证码，已移除当前代理，当前剩余%d代理'%len(ProxiesList))
        continue
    City = CitySoup.select('body > div.mainbox > div.main > div.crumbs_navigation > a') # 获取当前城市
    if City :
        City = City[0].text
    else :
        continue
    City = City.replace('58同城','')
    print('当前城市：'+ City)
    WorkItems = CitySoup.find('div',class_='items')
    JianzhiUrls = [Item.find('a').get('href') for Item in WorkItems.find_all('h2')]# 所有兼职职位链接
    print('共获取%d个职位链接'%len(JianzhiUrls))
    JianzhiUrls = [i for i in JianzhiUrls if len(i)<300] # 去除职位链接中推广信息
    print('去除推广信息后共有%d个职位链接'%len(JianzhiUrls))
    JianzhiUrls = ['https:'+ JianzhiUrl for JianzhiUrl in JianzhiUrls] # 补全链接
    JianzhiUrls = [i for i in JianzhiUrls if i not in GettedUrlList] # 去除职位链接中已录入数据库链接
    print('去除已录入后共有%d个职位链接'%len(JianzhiUrls))
    for JianzhiUrl in JianzhiUrls :
        while True :
            print('正在获取兼职页面内容……')
            try :
                Proxies = random.choice(ProxiesList)
                JianzhiResponse = requests.get(JianzhiUrl, headers = {"User-Agent":ua.random},proxies = Proxies, timeout = 20 )
                print('获取成功！')
                break
            except :
                ProxiesList.remove(Proxies)
                print('无法连接，已移除当前代理，当前剩余%d代理'%len(ProxiesList))
        JianzhiResponse.encoding = 'utf-8'
        JianzhiHtml = JianzhiResponse.text
        DetailsSoup = BeautifulSoup(JianzhiHtml, 'lxml')
        if DetailsSoup.title.string == '请输入验证码':
            ProxiesList.remove(Proxies)
            print('需要输入验证码，已移除当前代理，当前剩余%d代理'%len(ProxiesList))
            continue
        if DetailsSoup.h1 :
            pass
        else :
            print('该职位已停止招聘')
            continue
        DetailsTitle = DetailsSoup.h1.string
        DetailsContent = DetailsSoup.select('#content > div.left > div.xq.b.padd > p')
        if DetailsContent :
            pass
        else :
            continue
        DetailsContent = DetailsContent[0].text
        Company = DetailsSoup.select('#content > div.right > div.gsjs.b > div.gsjs1 > h2 > a')[0].text
        Price = DetailsSoup.select('#content > div.left > div.head.b > div.info > div.price > span:nth-of-type(1)')[0].text
        x = LocalCol.insert_one({"DetailsTitle":DetailsTitle,"DetailsContent":DetailsContent,"Company":Company,"Price":Price,"City":City,"Link":JianzhiUrl,"RecordDate":RecordDate})
        print('保存ID :', x.inserted_id)
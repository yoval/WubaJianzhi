# 58同城兼职抓取

**需用到mongo数据库，**提前准备col 1。

![mark](http://imgs.bizha.top/blog/20181205/pLwhq7HgTHo2.png?imageslim)



抓取58同城**全国**兼职信息**第一页**，并导入数据库。

- GetSocksProxies.py

  通过`https://www.socks-proxy.net`抓取代理，并通过`https://api.live.bilibili.com/ip_service/v1/ip_service/get_ip_addr`验证链接、地区。

  ![mark](http://imgs.bizha.top/blog/20181205/FJT1NW6eUs7Y.png?imageslim)

- WubaJianzhi.py

  利用 GetSocksProxies.py 获取的代理，抓取58同城兼职信息。

  ![mark](http://imgs.bizha.top/blog/20181205/v5nyUetc1X7a.png?imageslim)

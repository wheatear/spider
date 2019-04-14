#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request as ulb
from lxml import etree
import urllib

class SpiderProxies(object):
    def __init__(self):
        self.dSites = {"kuaidaili": "https://www.kuaidaili.com/free/inha/",
                 "xicidaili": "https://www.xicidaili.com/",
                 "89ip": "http://www.89ip.cn/"}
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
                   "Connection": "keep-alive",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                   "Accept-Language": "zh-CN,zh;q=0.9"}
        http_handler = ulb.HTTPSHandler()
        opener = ulb.build_opener(http_handler)

    def loadPage(self):
        url = self.dSites["xicidaili"]
        http_handler = ulb.HTTPSHandler()
        opener = ulb.build_opener(http_handler)
        request = ulb.Request(url,headers=self.headers)
        response = opener.open(request)
        return response

    def dealProxy(self,response):
        charset = response.headers.get_content_charset()
        html = etree.HTML(response.read().decode(charset))
        proxiesTable = html.xpath("//tr[td/@class='country']")
        # [country,ip,port,address,anonymous,type,timetolive,check]
        aHttpProxies = []
        aHttpsProxies = []
        for proxy in proxiesTable:
            proxyTr = proxy.xpath('./td')
            proxyInfo = []
            for item in proxyTr:
                proxyInfo.append(item.text)
            if proxyInfo[5] == 'HTTP':
                aHttpProxies.append(proxyInfo)
            elif proxyInfo[5] == 'HTTPS':
                aHttpsProxies.append(proxyInfo)
        return (aHttpProxies,aHttpsProxies)


    def getProxies(self):
        response = self.loadPage()
        return self.dealProxy(response)


if __name__ == "__main__":
    spiderProxy = SpiderProxies()
    aFreeProxies = spiderProxy.getProxies()
    print('http proxies: %d' % len(aFreeProxies[0]))
    for p in aFreeProxies[0]:
        print(p)

    print('https proxies: %d' % len(aFreeProxies[1]))
    for p in aFreeProxies[1]:
        print(p)

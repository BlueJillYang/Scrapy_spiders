#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import time
import sys
import scrapy
import json
import redis
import urllib
import requests
import urlparse
from scrapy.http import Request
from scrapy import Selector
from scrapy.http import FormRequest
from scrapy.utils.response import get_base_url
from scrapy import signals
# from scrapy.xlib.pydispatch import dispatcher
# from SpeciSpiders.items import DataItem
# from bc_crawler_ba.configs.special_config import SpecialConfig
# from bc_crawler_ba.sources.data_clean import create_pubtime,create_medianame
from ..items import DataItem

reload(sys)
sys.setdefaultencoding('utf-8')


class jsntgcjsw(scrapy.Spider):
    name = "jsntgcjsw"
    start_urls = [
        # "http://www.ntcetc.cn/ntztb/YW_Info/ZaoBiaoReport/MoreReportList_NT_CopyCZ.aspx?area=nts&CategoryName=%E5%B8%82%E7%BA%A7 PN", #招标
        # "http://www.ntcetc.cn/ntztb/YW_Info/ZaoBiaoReport/MoreReportList_NT_CopyCZ.aspx?area=ntkfq&CategoryName=%E5%8D%97%E9%80%9A%E5%BC%80%E5%8F%91%E5%8C%BA PN",
        # "http://www.ntcetc.cn/ntztb/YW_Info/ZaoBiaoReport/MoreReportList_NT_CopyCZ.aspx?area=tz&CategoryName=%E9%80%9A%E5%B7%9E%E5%8C%BA PN",
        # "http://www.ntcetc.cn/ntztb/YW_Info/ZaoBiaoReport/MoreReportList_NT_CopyCZ.aspx?area=qds&CategoryName=%E5%90%AF%E4%B8%9C%E5%B8%82 PN",
        # "http://www.ntcetc.cn/ntztb/YW_Info/ZaoBiaoReport/MoreReportList_NT_CopyCZ.aspx?area=hms&CategoryName=%E6%B5%B7%E9%97%A8%E5%B8%82 PN",
        # "http://www.ntcetc.cn/ntztb/YW_Info/ZaoBiaoReport/MoreReportList_NT_CopyCZ.aspx?area=rgs&CategoryName=%E5%A6%82%E7%9A%8B%E5%B8%82 PN",
        # "http://www.ntcetc.cn/ntztb/YW_Info/ZaoBiaoReport/MoreReportList_NT_CopyCZ.aspx?area=hax&CategoryName=%E6%B5%B7%E5%AE%89%E5%8E%BF PN",
        # "http://www.ntcetc.cn/ntztb/YW_Info/ZaoBiaoReport/MoreReportList_NT_CopyCZ.aspx?area=rds&CategoryName=%E5%A6%82%E4%B8%9C%E5%8E%BF PN",
        # "http://www.ntcetc.cn/ntztb/YW_Info/ZaoBiaoReport/MoreReportList_NT_CopyCZ.aspx?area=bhyq&CategoryName=%E6%BB%A8%E6%B5%B7%E5%9B%AD%E5%8C%BA PN",
        #
        # "http://www.ntcetc.cn/ntztb/YW_Info/ZhongBiaoGS/MoreResultList_NT_CopyCZ.aspx?area=nts&CategoryName=%E5%B8%82%E7%BA%A7 RN", #中标
        # "http://www.ntcetc.cn/ntztb/YW_Info/ZhongBiaoGS/MoreResultList_NT_CopyCZ.aspx?area=ntkfq&CategoryName=%E5%8D%97%E9%80%9A%E5%BC%80%E5%8F%91%E5%8C%BA RN",
        # "http://www.ntcetc.cn/ntztb/YW_Info/ZhongBiaoGS/MoreResultList_NT_CopyCZ.aspx?area=tz&CategoryName=%E9%80%9A%E5%B7%9E%E5%8C%BA RN",
        # "http://www.ntcetc.cn/ntztb/YW_Info/ZhongBiaoGS/MoreResultList_NT_CopyCZ.aspx?area=qds&CategoryName=%E5%90%AF%E4%B8%9C%E5%B8%82 RN",
        # "http://www.ntcetc.cn/ntztb/YW_Info/ZhongBiaoGS/MoreResultList_NT_CopyCZ.aspx?area=hms&CategoryName=%E6%B5%B7%E9%97%A8%E5%B8%82 RN",
        # "http://www.ntcetc.cn/ntztb/YW_Info/ZhongBiaoGS/MoreResultList_NT_CopyCZ.aspx?area=rgs&CategoryName=%E5%A6%82%E7%9A%8B%E5%B8%82 RN",
        # "http://www.ntcetc.cn/ntztb/YW_Info/ZhongBiaoGS/MoreResultList_NT_CopyCZ.aspx?area=hax&CategoryName=%E6%B5%B7%E5%AE%89%E5%8E%BF RN",
        # "http://www.ntcetc.cn/ntztb/YW_Info/ZhongBiaoGS/MoreResultList_NT_CopyCZ.aspx?area=rds&CategoryName=%E5%A6%82%E4%B8%9C%E5%8E%BF RN",
        #
        # "http://www.ntcetc.cn/ntztb/YW_Info/ZiGeYS/MoreYSList_FromCZ.aspx?categoryNum=006 PN", #资格预审
        # "http://www.ntcetc.cn/ntztb/ShowInfo/moreinfo.aspx?categoryNum=018 RN",   #中标候选人
        # "http://www.ntcetc.cn/ntztb/YW_Info/ZuiGaoXJ/MoreZGXJList.aspx PN"  #最高限价
    ]
    Debug = True
    doredis = True
    source = u"南通市工程建设网"
    # configure = SpecialConfig()
    post_params = []
    lost_counts = 0   #被过滤个数
    custom_settings = {"DOWNLOAD_TIMEOUT":30.0} #本地跑不需要，测试环境需要，不然超时

    def __init__(self,start_url=None,history=True):
        super(jsntgcjsw, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
            self.post_params.append({"url":job.split()[0],"ba_type":job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)
        self.history = history

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_read_redis.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

    def start_requests(self):
        for channel in self.post_params:
            url = channel['url']
            # if self.doredis and self.expire_redis.exists(url):
            #    continue
            yield Request(url=url,method='get',meta={"ba_type":channel["ba_type"],"page_parse":True,"page_index":"1"},callback=self.parse_link)

    def get__EVENTTARGET(self,response,id):
         __EVENTTARGET = response.xpath("//div[@id='"+ id + "']//a[last()]/@href").extract() or \
                            response.xpath("//div[@id='"+ id + "']//a[1]/@href").extract()
         __EVENTTARGET = __EVENTTARGET[0]
         __EVENTTARGET = re.search(r"'(.*?)'",__EVENTTARGET).group(1)
         return __EVENTTARGET

    def parse_link(self, response):   #这个就别整样式了，弄成map后期维护起来看代码都要半天  以后有空再优化结构吧
        id_type = ""
        if 'ZaoBiaoReport' in response.url: #招标
            id_type = 'MoreXiangMuList1_tdcontent'
        if 'ZhongBiaoGS' in response.url: #中标
            id_type = 'morezhongbiaolist1_tdcontent'
        if 'ZiGeYS' in response.url: #资格预审
            id_type = 'MoreZGYSGSList1_tdcontent'
        if 'ZuiGaoXJ' in response.url: #最高限价
            id_type = 'MoreZGYSGSList1_tdcontent'
        #//td[@id='MoreXiangMuList1_tdcontent']//a[@onclick]/@onclick 例子
        urls = response.xpath("//td[@id='"+id_type+"']//a[@onclick]/@onclick").extract()
        titles = response.xpath("//td[@id='"+id_type+"']//a[@onclick]/text()").extract()
        pubtimes = response.xpath("//td[@id='"+id_type+"']//tr/td[3]/text()").extract()

        if 'ShowInfo' in response.url:   #中标候选人
            id_type = 'MoreInfoList1_tdcontent'
            urls = response.xpath("//td[@id='"+id_type+"']//a/@href").extract()
            titles = response.xpath("//td[@id='"+id_type+"']//a/text()").extract()
            pubtimes = response.xpath("//td[@id='"+id_type+"']//tr/td[3]/text()").extract()

        for index,url in enumerate(urls):
            if 'openZhuanYeWin' in url:  #招标
                id = re.search(r"\d+",url).group(0)
                if 'ZaoBiaoReport' in response.url:  #招标
                    final = urlparse.urljoin(response.url,'./XiangMuZhuanYeGongGao.aspx?ID=' + id)
                else:  #中标
                    final = urlparse.urljoin(response.url,'./ZhuanYeZhongBiaoDetailInfo.aspx?ID=' + id)
            elif 'openWinNew' in url:    #资格预审
                id = re.findall(r"'(.*?)'",url)
                final = urlparse.urljoin(response.url,'./ViewZGYSDetailNew.aspx?RowID='+ id[0] + "&bdguid=" + id[1])
            elif 'openWin' in url:
                id = re.search(r"\d+",url).group(0)
                if 'ZiGeYS' in response.url: #资格预审
                    final = urlparse.urljoin(response.url,'./ViewZGYSDetail.aspx?RowID=' + id)
                elif 'ZaoBiaoReport' in response.url: #招标
                    final = urlparse.urljoin(response.url,'./XiangMuDetailInfo.aspx?ID=' + id)
                else:#中标
                    final = urlparse.urljoin(response.url,'./ZhongBiaoDetailInfo.aspx?ID=' + id)
            elif 'window.open' in url:   #这个基本是通用
                url_new = re.search(r"\"(.*?)\"",url)
                if url_new:
                    if 'http' not in url_new.group(1):
                        url_new = "./" + url_new.group(1)  #不带http链接
                    else:
                        url_new = url_new.group(1)  #兼容最高限价的部分详细页链接  真是乱七八糟的网站   完整http链接
                    final = urlparse.urljoin(response.url,url_new)
                else:
                    if "http" in url and "//" not in url:#这网站错误数据真多，容错1，缺少“//”  以及整个就是截取错误
                        url_new = "http://" + re.search(r"\"(www.*?)\"",url).group(1)
                        final = url_new
            else:
                final = re.search(r"\"(.*?)\"",url) #招标 中标
                if final:
                    final = final.group(0)
                else:
                    final = url  #候选人

            # if self.doredis and self.expire_redis.exists(final):
            #     continue
            title = titles[index].strip()
            pubtime = pubtimes[index].strip() + " 00:00"
            if "www.tzzbb.com" in final: #适配招标采购---通州区  废弃网站 "www.tzzbb.com"
                self.lost_counts += 1
                print self.lost_counts,"通州区旧网站被过滤...TZ",response.meta["page_index"],title,final
                pass
            else:
                print "有效连接",response.meta["page_index"],title,final
                yield Request(url=final,method='get',meta={"ba_type":response.meta["ba_type"],"title":title,"pubtime":pubtime},callback=self.parse_item)

        page = 0
        __EVENTTARGET = ""
        lastPage = response.xpath("//div[@id='MoreXiangMuList1_Pager']//font[2]/b/text()").extract()   #招标
        if len(lastPage) > 0:
            page = int(re.search("/(\d+)",lastPage[0]).group(1))
            __EVENTTARGET = self.get__EVENTTARGET(response,'MoreXiangMuList1_Pager')

        lastPage = response.xpath("//div[@id='morezhongbiaolist1_Pager']//font[2]/b/text()").extract()   #中标
        if len(lastPage) > 0:
            page = int(re.search("/(\d+)",lastPage[0]).group(1))
            __EVENTTARGET = self.get__EVENTTARGET(response,'morezhongbiaolist1_Pager')

        lastPage = response.xpath("//div[@id='MoreZGYSGSList1_Pager']//font[2]/b/text()").extract()   #资格预审
        if len(lastPage) > 0:
            page = int(re.search("/(\d+)",lastPage[0]).group(1))
            __EVENTTARGET = self.get__EVENTTARGET(response,'MoreZGYSGSList1_Pager')

        lastPage = response.xpath("//div[@id='MoreInfoList1_Pager']//font[2]/b/text()").extract()   #中标候选人
        if len(lastPage) > 0:
            page = int(re.search(r"\d+",lastPage[0]).group(0))
            __EVENTTARGET = self.get__EVENTTARGET(response,'MoreInfoList1_Pager')

        lastPage = response.xpath("//div[@id='MoreZGYSGSList1_Pager']//font[2]/b/text()").extract()   #最高限价
        if len(lastPage) > 0:
            page = int(re.search("/(\d+)",lastPage[0]).group(1))
            __EVENTTARGET = self.get__EVENTTARGET(response,'MoreZGYSGSList1_Pager')

        if self.history and page > 1 and response.meta["page_parse"]:
                __VIEWSTATE = response.xpath("//input[@id='__VIEWSTATE']/@value").extract()[0]
                __VIEWSTATEGENERATOR = response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").extract()[0]
                __EVENTVALIDATION = response.xpath("//input[@id='__EVENTVALIDATION']/@value").extract()
                if len(__EVENTVALIDATION) > 0:
                    __EVENTVALIDATION = __EVENTVALIDATION[0]
                else:
                    __EVENTVALIDATION = ""   #适配 中标候选人  这个频道没这个参数

                # for i in range(2,int(page)+1):
                for i in range(2,3):
                    # if i>2:
                    #     break
                    formdata={
                        "__VIEWSTATE":__VIEWSTATE,
                        "__VIEWSTATEGENERATOR":__VIEWSTATEGENERATOR,
                        "__EVENTTARGET":__EVENTTARGET,
                        "__EVENTARGUMENT": str(i),
                        "__EVENTVALIDATION":__EVENTVALIDATION,
                    }
                    yield FormRequest(url=response.url,meta={"ba_type":response.meta["ba_type"],"page_parse":False,"page_index":str(i)},method='post',formdata=formdata,callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()

        item["pubtime"] = response.meta["pubtime"]
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省南通市'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.meta["title"]
        #依次为 招标/中标/资格预审/中标候选人/最高限价
        content = response.xpath("//span[@id='tdContent1']").extract() or \
                  response.xpath("//span[@id='InfoDetail1_spnContent']").extract() or \
                  response.xpath("//*[@id='grdList']").extract() or \
                  response.xpath("//table[@id='Table1']").extract() or \
                  response.xpath("//td[@id='tdContent']").extract() or \
                  response.xpath("//table[@width='90%' and @align='center']").extract()
        item['content'] = content[0]

        if item['pubtime'] and item['title'] and item['content']:
            print self.lost_counts   #被过滤数
            yield item




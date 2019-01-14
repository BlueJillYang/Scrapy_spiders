# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy import signals
import sys
import os
import codecs
import time
from scrapy.xlib.pydispatch import dispatcher
import xlrd
# from xlutils.copy import copy
# import xlsxwriter

reload(sys)
sys.setdefaultencoding("utf-8")

class BidtestPipeline(object):
    def __init__(self):
        self.folder = "E:/testinfo"
        self.xlsCount = 1
        self.xlsCountPassed = 1
        dispatcher.connect(self.initialize, signals.spider_opened)
        dispatcher.connect(self.finalize, signals.spider_closed)

    def initialize(self, spider):
        #创建json
        self.result_name = os.path.join(self.folder, spider.name+"_%d.json"%int(time.time()))
        self.resultf = codecs.open(self.result_name,'w',encoding='utf-8')

        #创建xlsx
        # self.result_nameXls = os.path.join(self.folder, spider.name+"_%d.xlsx"%int(time.time()))
        # self.workbook = xlsxwriter.Workbook(self.result_nameXls)
        # self.worksheet = self.workbook.add_worksheet('values')
        # self.worksheet.write(0, 0, u"标题")
        # self.worksheet.write(0, 1, u"发布时间")
        # self.worksheet.write(0, 2, u"链接地址")
        #
        # self.result_nameXlsPassed = os.path.join(self.folder, spider.name+"_passed"+"_%d.xlsx"%int(time.time()))
        # self.workbook2 = xlsxwriter.Workbook(self.result_nameXlsPassed)
        # self.worksheet2 = self.workbook2.add_worksheet('values')
        # self.worksheet2.write(0, 0, u"标题")
        # self.worksheet2.write(0, 1, u"发布时间")
        # self.worksheet2.write(0, 2, u"链接地址")

    def process_item(self, item, spider):
        #写入json
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.resultf.write(line)
        # if not item["passed"]:
        #     #写入xlsx
        #     self.worksheet.write(self.xlsCount, 0, item["title"])
        #     self.worksheet.write(self.xlsCount, 1, item["pubtime"])
        #     self.worksheet.write_url(self.xlsCount, 2, item['url'])
        #     self.xlsCount += 1
        # else:
        # #写入被过滤掉的item
        #     self.worksheet2.write(self.xlsCountPassed, 0, item["title"])
        #     self.worksheet2.write(self.xlsCountPassed, 1, item["pubtime"])
        #     self.worksheet2.write_url(self.xlsCountPassed, 2, item['url'])
        #     self.xlsCountPassed += 1


        # return item

    def finalize(self, spider):
        #关闭json读写流
        self.resultf.close()

        #保存xlsx文件
        # self.workbook.close()
        #保存被过滤文件
        # self.workbook2.close()

        if os.path.getsize(self.result_name) <= 0:
            print "Has no item in result filt, delete it!!!"
            os.remove(self.result_name)
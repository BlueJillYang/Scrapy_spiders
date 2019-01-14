# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy import signals
import sys
import os
import codecs
import time
from scrapy.xlib.pydispatch import dispatcher
import xlrd
import csv
import codecs


class GuangmingPipeline(object):
    def __init__(self):
        # self.file = codecs.open('test_for_status_code.csv', 'a', encoding='utf-8')
        self.folder = '/home/python/Desktop/Test_spiders/Csv_Json_Log/Json/'
        self.count = 0
        # self.csvFile = open('/home/python/Desktop/Test_spiders/Csv_Json_Log/Test_result_01.csv', 'w')
        # fieldnames = ('Title', 'Pubtime', 'url', 'Content')
        # self.writer = csv.DictWriter(self.csvFile, fieldnames=fieldnames)
        dispatcher.connect(self.initialize, signals.spider_opened)

    def initialize(self, spider):
        #创建json
        self.FileName= os.path.join(self.folder, spider.name+".json")
        # self.FileName= os.path.join(self.folder, spider.name+"_%d.json"%int(time.time()))
        self.jsonFile= codecs.open(self.FileName,'w',encoding='utf-8')

    def __del__(self):
        # self.file.close() self.csvFile
        # self.csvFile.close()
        self.jsonFile.close()

    def process_item(self, item, spider):
        ## csv写入
        # self.writer.writerow({'Title': item['title'], 'Pubtime': item['pubtime'],
        #                       'url': item['url'], 'Content': item['content'][:30]})
        # content = json.dumps(dict(item), ensure_ascii=False) + "\n"

        # json写入
        # self.file.write(content)
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.jsonFile.write(line)
        self.count += 1
        print 'pipeline, spider.name={}, already_parsed:{}'.format(spider.name, self.count)

        return item
    # def __init__(self):
    #     self.folder = "testinfo"
    #     self.xlsCount = 1
    #     self.xlsCountPassed = 1
    #     dispatcher.connect(self.initialize, signals.spider_opened)
    #     dispatcher.connect(self.finalize, signals.spider_closed)
    #
    # def initialize(self, spider):
    #     #创建json
    #     self.result_name = os.path.join(self.folder, spider.name+"_%d.json"%int(time.time()))
    #     self.resultf = codecs.open(self.result_name,'w',encoding='utf-8')
    #
    #     #创建xlsx
    #     # self.result_nameXls = os.path.join(self.folder, spider.name+"_%d.xlsx"%int(time.time()))
    #     # self.workbook = xlsxwriter.Workbook(self.result_nameXls)
    #     # self.worksheet = self.workbook.add_worksheet('values')
    #     # self.worksheet.write(0, 0, u"标题")
    #     # self.worksheet.write(0, 1, u"发布时间")
    #     # self.worksheet.write(0, 2, u"链接地址")
    #     #
    #     # self.result_nameXlsPassed = os.path.join(self.folder, spider.name+"_passed"+"_%d.xlsx"%int(time.time()))
    #     # self.workbook2 = xlsxwriter.Workbook(self.result_nameXlsPassed)
    #     # self.worksheet2 = self.workbook2.add_worksheet('values')
    #     # self.worksheet2.write(0, 0, u"标题")
    #     # self.worksheet2.write(0, 1, u"发布时间")
    #     # self.worksheet2.write(0, 2, u"链接地址")
    #
    # def process_item(self, item, spider):
    #     #写入json
    #     line = json.dumps(dict(item), ensure_ascii=False) + "\n"
    #     self.resultf.write(line)
    #     # if not item["passed"]:
    #     #     #写入xlsx
    #     #     self.worksheet.write(self.xlsCount, 0, item["title"])
    #     #     self.worksheet.write(self.xlsCount, 1, item["pubtime"])
    #     #     self.worksheet.write_url(self.xlsCount, 2, item['url'])
    #     #     self.xlsCount += 1
    #     # else:
    #     # #写入被过滤掉的item
    #     #     self.worksheet2.write(self.xlsCountPassed, 0, item["title"])
    #     #     self.worksheet2.write(self.xlsCountPassed, 1, item["pubtime"])
    #     #     self.worksheet2.write_url(self.xlsCountPassed, 2, item['url'])
    #     #     self.xlsCountPassed += 1
    #
    #
    #     # return item
    #
    # def finalize(self, spider):
    #     #关闭json读写流
    #     self.resultf.close()
    #
    #     #保存xlsx文件
    #     # self.workbook.close()
    #     #保存被过滤文件
    #     # self.workbook2.close()
    #
    #     if os.path.getsize(self.result_name) <= 0:
    #         print "Has no item in result filt, delete it!!!"
    #         os.remove(self.result_name)

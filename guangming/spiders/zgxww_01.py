#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
__author__ = 'wjm'
import re
import time
import sys
import scrapy
import json
import codecs
import redis
import urllib
import requests
import urlparse
from scrapy.http import Request
import traceback
import datetime
from scrapy import Selector
# from scrapy.http import FormRequest
# from scrapy.utils.response import get_base_url
# from scrapy import signals
# from scrapy.xlib.pydispatch import dispatcher
# from SpeciSpiders.items import DataItem
# from bc_crawler.configs.special_config import SpecialConfig
from ..items import DataItem


class chinanews(scrapy.Spider):
    name = 'zgxww_01'
    start_urls = [
        "http://www.bt.chinanews.com/zhongya/index.shtml news",
        "http://www.yn.chinanews.com/pub/news/fashion/lvyou/ news",
        # "http://channel.chinanews.com/cns/cl/hwjy-hxdt.shtml news",
        # "http://channel.chinanews.com/cns/cl/edu-qzcy.shtml news",
        # "http://channel.chinanews.com/cns/cl/edu-jsyd.shtml news",
        # "http://channel.chinanews.com/cns/cl/tw-lasq.shtml news",
        # "http://channel.chinanews.com/cns/cl/tw-lajl.shtml news",
        # "http://www.sx.chinanews.com/4/2011/0720/66.html news",
        # "http://channel.chinanews.com/cns/cl/ny-mt.shtml news",
        # "http://www.bt.chinanews.com/zhuangao/index.shtml news",
        # "http://www.fj.chinanews.com/new/jryw/list.shtml news",
        # "http://www.gd.chinanews.com/index/zx.html news",
        # "http://channel.chinanews.com/cns/cl/edu-tszs.shtml news",
        # "http://channel.chinanews.com/cns/cl/gj-gjzj.shtml news",
        # "http://www.bt.chinanews.com/Art/shufa/ news",
        # "http://channel.chinanews.com/cns/cl/estate-qyj.shtml news",
        # "http://www.yn.chinanews.com/pub/news/world/keji/ news",
        # "http://channel.chinanews.com/cns/cl/edu-qzjy.shtml news",
        # "http://channel.chinanews.com/cns/cl/edu-zkzx.shtml news",
        # "http://www.bt.chinanews.com/shehui/index.shtml news",
        # "http://channel.chinanews.com/cns/cl/edu-xxgl.shtml news",
        # "http://channel.chinanews.com/cns/cl/edu-yyks.shtml news",
        # "http://www.yn.chinanews.com/pub/news/fashion/yule/ news",
        # "http://channel.chinanews.com/cns/cl/it-jdxw.shtml news",
        # "http://www.yn.chinanews.com/pub/news/fashion/jiankang/ news",
        # "http://channel.chinanews.com/cns/cl/tw-dlyw.shtml news",
        # "http://channel.chinanews.com/cns/cl/life-jrgz.shtml news",
        # "http://www.yn.chinanews.com/pub/zxft/ news",
        # "http://www.ln.chinanews.com/shishang/ news",
        # "http://www.yn.chinanews.com/pub/news/southasia/ news",
        # "http://www.yn.chinanews.com/pub/news/yunnan/ news",
        # "http://www.bt.chinanews.com/shituan/index.shtml news",
        "http://www.hn.chinanews.com/news/qwsp/ news",
        # "http://channel.chinanews.com/cns/cl/it-qydt.shtml news",
        # "http://www.gz.chinanews.com/qsyh/index.shtml news",
        # "http://channel.chinanews.com/cns/cl/tw-jmdt.shtml news",
        # "http://channel.chinanews.com/cns/cl/tw-twyw.shtml news",
        # "http://channel.chinanews.com/cns/cl/edu-fmxt.shtml news",
        # "http://www.bt.chinanews.com/gongsi/index.shtml news",
        # "http://www.bt.chinanews.com/fazhi/index.shtml news",
        # "http://channel.chinanews.com/cns/cl/tw-jsdt.shtml news",
        # "http://www.bt.chinanews.com/tupian/index.shtml news",
        # "http://www.shx.chinanews.com/kjww.html news",
        # "http://www.bj.chinanews.com/4/2009/0306/12.html news",
        # "http://channel.chinanews.com/cns/cl/estate-gy.shtml news",
        # "http://channel.chinanews.com/cns/cl/edu-xyztc.shtml news",
        # "http://channel.chinanews.com/cns/cl/tw-lydl.shtml news",
        # "http://www.gd.chinanews.com/index/cnstv.html news",
        # "http://channel.chinanews.com/video/showchannel?tid=4&currentpage=0&pagenum=16&_= news",
        # "http://www.fj.chinanews.com/new/dsxw/list.shtml news",
        # "http://channel.chinanews.com/cns/cl/it-dzsw.shtml news",
        # "http://www.ln.chinanews.com/jiaoyu news",
        # "http://channel.chinanews.com/cns/cl/estate-yt.shtml news",
        # "http://channel.chinanews.com/cns/cl/hwjy-jxyd.shtml news",
        # "http://channel.chinanews.com/cns/cl/it-itftj2.shtml news",
        # "http://www.ln.chinanews.com/caijing/ news",
        # "http://www.bt.chinanews.com/lvyou/index.shtml news",
        # "http://channel.chinanews.com/cns/cl/hwjy-cybx.shtml news",
        # "http://www.hi.chinanews.com/gundong/yule.html news",
        # "http://channel.chinanews.com/cns/cl/edu-zcdt.shtml news",
        # "http://www.sx.chinanews.com/linfen/list/3.html news",
        # "http://channel.chinanews.com/cns/cl/tw-ztjz.shtml news",
        # "http://www.gd.chinanews.com/index/zxzt.html news",
        # "http://finance.chinanews.com/#rmbhy news",
        # "http://house.chinanews.com/ news",
        # "http://www.bt.chinanews.com/jingji/index.shtml news",
        # "http://www.jx.chinanews.com/travel/ news",
        # "http://www.bt.chinanews.com/bingtuan/index.shtml news",
        # "http://www.chinanews.com/entertainment/photo/yltkphoto-1.html news",
        # "http://www.bj.chinanews.com/focus/11.html news",
        # "http://www.gs.chinanews.com/gsyw1.html news",
        "http://www.heb.chinanews.com/4/20111018/335.shtml news",
        # "http://www.chinanews.com/health/index.shtml news",
        # "http://www.yn.chinanews.com/pub/news/world/guoji/ news",
        # "http://www.hn.chinanews.com/jrhn/340/ newspaper",
        # "http://www.chinanews.com/edu.shtml news",
        # "http://www.bt.chinanews.com/yuanjiang/index.shtml news",
        # "http://www.bt.chinanews.com/shipin/index.shtml news",
        # "http://www.yn.chinanews.com/pub/video/zixun/ news",
        # "http://www.yn.chinanews.com/pub/news/world/pinglun/ news",
        # "http://www.hn.chinanews.com/news/qcxw/ news",
        # "http://www.bt.chinanews.com/liandui/index.shtml news",
        # "http://www.hn.chinanews.com/news/zfqy/ news",
        # "http://www.js.chinanews.com/comment/ news",
        # "http://www.js.chinanews.com/4/17.html news",
        # "http://www.js.chinanews.com/76/hzzx.html news",
        # "http://www.js.chinanews.com/photo/highlights/ news",
        # "http://www.js.chinanews.com/photo/citynews/ news",
        # "http://www.js.chinanews.com/photo/sports/ news",
        # "http://www.js.chinanews.com/photo/business/ news",
        # "http://www.js.chinanews.com/photo/science/ news",
        # "http://www.js.chinanews.com/photo/fashion/ news",
        # "http://www.js.chinanews.com/76/2.html news",
        # "http://www.sc.chinanews.com/ChengduNews/ms/index.shtml news",
        # "http://www.sc.chinanews.com/ChengduNews/rd/index.shtml news",
        # "http://www.sc.chinanews.com/ChengduNews/mtbd/index.shtml news",
        # "http://www.sc.chinanews.com/ChengduNews/bm/index.shtml news",
        # "http://www.sc.chinanews.com/ChengduNews/qx/index.shtml news",
        # "http://www.sc.chinanews.com/ChengduNews/qt/index.shtml news",
        # "http://www.chinanews.com/jiaoyu.shtml news",
        # "http://channel.chinanews.com/cns/cl/gn-gcdt.shtml news",
        # "http://channel.chinanews.com/cns/cl/gn-zcdt.shtml news",
        # "http://channel.chinanews.com/cns/cl/gn-rsbd.shtml news",
        # "http://channel.chinanews.com/cns/cl/gj-zxsjg.shtml news",
        # "http://channel.chinanews.com/u/gj-rw.shtml news",
        # "http://channel.chinanews.com/u/fsh.shtml news",
        # "http://channel.chinanews.com/u/rdzz.shtml news",
        # "http://channel.chinanews.com/u/gn-rjbw.shtml news",
        # "http://channel.chinanews.com/u/gn-dyxc.shtml news",
        # "http://channel.chinanews.com/cns/cl/cj-msrd.shtml news",
        # "http://www.chinanews.com/business/gd.shtml news",
        # "http://www.chinanews.com/house/gd.shtml news",
        # "http://it.chinanews.com/it/gd.shtml news",
        # "http://www.chinanews.com/energy/gd.shtml news",
        # "http://channel.chinanews.com/cns/cl/business-rw.shtml news",
        # "http://channel.chinanews.com/cns/cl/stock-scyw.shtml news",
        # "http://channel.chinanews.com/cns/cl/auto-cqrw.shtml news",
        # "http://channel.chinanews.com/cns/cl/auto-cyd.shtml news",
        # "http://channel.chinanews.com/cns/cl/ga-zmrs.shtml news",
        # "http://channel.chinanews.com/cns/cl/tw-rw.shtml news",
        # "http://channel.chinanews.com/cns/cl/tw-lahd.shtml news",
        # "http://channel.chinanews.com/cns/cl/tw-jjtw.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-lszs.shtml news",
        # "http://channel.chinanews.com/u/hr/cgfx.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-qjdt.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-qxcz.shtml news",
        # "http://channel.chinanews.com/cns/cl/yl-mxnd.shtml news",
        # "http://channel.chinanews.com/cns/cl/yl-ypkb.shtml news",
        # "http://channel.chinanews.com/cns/cl/cul-rwzf.shtml news",
        # "http://channel.chinanews.com/cns/cl/cul-sckgd.shtml news",
        # "http://channel.chinanews.com/cns/cl/ty-bdjj.shtml news",
        # "http://www.chinanews.com/shipin/m/tt/views.shtml news",
        # "http://www.chinanews.com/shipin/m/wy/wy-yl/views.shtml news",
        # "http://www.chinanews.com/ty/gun-news.html news",
        # "http://www.chinanews.com/entertainment.shtml news",
        # "http://www.chinanews.com/shipin/m/wy/wy-cul/views.shtml news",
        # "http://photo.chinanews.com/photo/zxhb.html news",
        # "http://photo.chinanews.com/photo/more/1.html news",
        # "http://photo.chinanews.com/photo/gnjj.html news",
        # "http://photo.chinanews.com/photo/shbt.html news",
        # "http://photo.chinanews.com/photo/gjbl.html news",
        # "http://photo.chinanews.com/photo/ylty.html news",
        # "http://photo.chinanews.com/photo/shmy.html news",
        # "http://photo.chinanews.com/photo/jskj.html news",
        # "http://photo.chinanews.com/photo/gatq.html news",
        # "http://photo.chinanews.com/tp/chart/index.shtml news",
        # "http://channel.chinanews.com/video/showchannel?lanmu1=rd-rd&currentpage=0&pagenum=16&_= news",
        # "http://channel.chinanews.com/video/showchannel?tid=4&currentpage=0&pagenum=16&_= news",
        # "http://channel.chinanews.com/video/showchannel?channel1=gn&currentpage=0&pagenum=16&_= news",
        # "http://channel.chinanews.com/video/showchannel?channel1=sh&currentpage=0&pagenum=16&_= news",
        # "http://channel.chinanews.com/video/showchannel?channel1=gj&currentpage=0&pagenum=16&_= news",
        # "http://channel.chinanews.com/video/showchannel?lanmu1=jq-mil&currentpage=0&pagenum=16&_= news",
        # "http://channel.chinanews.com/video/showchannel?channel1=wy&currentpage=0&pagenum=16&_= news",
        # "http://channel.chinanews.com/video/showchannel?channel1=cj&currentpage=0&pagenum=16&_= news",
        # "http://channel.chinanews.com/video/showchannel?channel1=ga&currentpage=0&pagenum=16&_= news",
        # "http://www.chinanews.com/theory.shtml news",
        # "http://channel.chinanews.com/cns/cl/ll-llqy.shtml news",
        # "http://channel.chinanews.com/cns/cl/ll-sjts.shtml news",
        # "http://channel.chinanews.com/cns/cl/ll-dsdj.shtml news",
        # "http://channel.chinanews.com/cns/cl/ll-xzly.shtml news",
        # "http://www.chinanews.com/jiankang.shtml news",
        # "http://channel.chinanews.com/cns/cl/life-mstj.shtml news",
        # "http://channel.chinanews.com/cns/cl/wine-rwzf.shtml news",
        # "http://channel.chinanews.com/cns/cl/wine-sp.shtml news",
        # "http://www.chinanews.com/piaowu/hot-more.html news",
        # "http://www.ah.chinanews.com/focus/5.html news",
        # "http://www.ah.chinanews.com/focus/6.html news",
        # "http://www.ah.chinanews.com/focus/7.html news",
        # "http://www.ah.chinanews.com/focus/8.html news",
        # "http://www.ah.chinanews.com/focus/9.html news",
        # "http://www.ah.chinanews.com/focus/10.html news",
        # "http://www.ah.chinanews.com/focus/12.html news",
        # "http://www.ah.chinanews.com/focus/4.html news",
        # "http://www.ah.chinanews.com/focus/14.html news",
        # "http://www.ah.chinanews.com/focus/15.html news",
        # "http://www.ah.chinanews.com/focus/18.html news",
        # "http://www.ah.chinanews.com/focus/19.html news",
        # "http://www.ah.chinanews.com/focus/20.html news",
        # "http://www.ah.chinanews.com/focus/26.html news",
        # "http://www.ah.chinanews.com/focus/27.html news",
        # "http://www.ah.chinanews.com/focus/28.html news",
        # "http://www.ah.chinanews.com/focus/29.html news",
        # "http://www.ah.chinanews.com/focus/30.html news",
        # "http://www.ah.chinanews.com/focus/31.html news",
        # "http://www.ah.chinanews.com/focus/32.html news",
        # "http://www.ah.chinanews.com/focus/33.html news",
        # "http://www.ah.chinanews.com/focus/34.html news",
        # "http://www.ah.chinanews.com/focus/35.html news",
        # "http://www.ah.chinanews.com/focus/36.html news",
        # "http://www.ah.chinanews.com/focus/37.html news",
        # "http://www.ah.chinanews.com/focus/38.html news",
        # "http://www.ah.chinanews.com/focus/39.html news",
        # "http://www.ah.chinanews.com/focus/40.html news",
        # "http://www.ah.chinanews.com/focus/41.html news",
        # "http://www.ah.chinanews.com/focus/42.html news",
        # "http://www.ah.chinanews.com/focus/43.html news",
        # "http://www.ah.chinanews.com/focus/44.html news",
        # "http://www.ah.chinanews.com/focus/45.html news",
        # "http://www.ah.chinanews.com/focus/46.html news",
        # "http://www.ah.chinanews.com/focus/13.html news",
        # "http://www.ah.chinanews.com/focus/47.html news",
        # "http://www.ah.chinanews.com/focus/48.html news",
        # "http://www.ah.chinanews.com/focus/49.html news",
        # "http://www.ah.chinanews.com/focus/50.html news",
        # "http://www.ah.chinanews.com/focus/51.html news",
        # "http://www.ah.chinanews.com/focus/52.html news",
        # "http://www.ah.chinanews.com/focus/53.html news",
        # "http://www.ah.chinanews.com/focus/54.html news",
        # "http://www.ah.chinanews.com/focus/55.html news",
        # "http://www.ah.chinanews.com/focus/56.html news",
        # "http://www.ah.chinanews.com/focus/57.html news",
        # "http://www.ah.chinanews.com/focus/58.html news",
        # "http://www.ah.chinanews.com/focus/21.html news",
        # "http://www.ah.chinanews.com/focus/59.html news",
        # "http://www.ah.chinanews.com/focus/22.html news",
        # "http://www.ah.chinanews.com/focus/23.html news",
        # "http://www.ah.chinanews.com/focus/24.html news",
        # "http://www.ah.chinanews.com/focus/60.html news",
        # "http://www.ah.chinanews.com/focus/61.html news",
        # "http://www.ah.chinanews.com/focus/11.html news",
        # "http://www.bj.chinanews.com/focus/1.html news",
        # "http://www.bj.chinanews.com/focus/3.html news",
        # "http://www.bj.chinanews.com/focus/8.html news",
        # "http://www.bj.chinanews.com/focus/10.html news",
        # "http://www.cq.chinanews.com/more/zxsbdcq.shtml news",
        # "http://www.cq.chinanews.com/more/jucq.shtml news",
        # "http://www.cq.chinanews.com/more/lhcq.shtml news",
        # "http://www.cq.chinanews.com/more/xzcq.shtml news",
        # "http://www.cq.chinanews.com/more/31.shtml news",
        # "http://www.cq.chinanews.com/more/45.shtml news",
        # "http://www.cq.chinanews.com/more/48.shtml news",
        # "http://www.cq.chinanews.com/more/44.shtml news",
        # "http://www.cq.chinanews.com/more/49.shtml news",
        # "http://www.cq.chinanews.com/more/50.shtml news",
        # "http://www.cq.chinanews.com/more/51.shtml news",
        # "http://www.cq.chinanews.com/more/52.shtml news",
        # "http://www.cq.chinanews.com/more/53.shtml news",
        # "http://www.cq.chinanews.com/more/54.shtml news",
        # "http://www.cq.chinanews.com/more/56.shtml news",
        # "http://www.cq.chinanews.com/more/55.shtml news",
        # "http://www.cq.chinanews.com/more/59.shtml news",
        # "http://www.cq.chinanews.com/more/58.shtml news",
        # "http://www.cq.chinanews.com/more/60.shtml news",
        # "http://www.cq.chinanews.com/more/66.shtml news",
        # "http://www.cq.chinanews.com/more/65.shtml news",
        # "http://www.cq.chinanews.com/more/180.shtml news",
        # "http://www.cq.chinanews.com/more/182.shtml news",
        # "http://www.cq.chinanews.com/more/173.shtml news",
        # "http://www.cq.chinanews.com/more/181.shtml news",
        # "http://www.cq.chinanews.com/more/183.shtml news",
        # "http://www.cq.chinanews.com/more/172.shtml news",
        # "http://www.cq.chinanews.com/more/185.shtml news",
        # "http://www.cq.chinanews.com/more/186.shtml news",
        # "http://www.cq.chinanews.com/more/178.shtml news",
        # "http://www.cq.chinanews.com/more/4.shtml news",
        # "http://www.cq.chinanews.com/more/5.shtml news",
        # "http://www.cq.chinanews.com/more/11.shtml news",
        # "http://www.cq.chinanews.com/more/szqx.shtml news",
        # "http://www.cq.chinanews.com/more/10.shtml news",
        # "http://www.cq.chinanews.com/more/23.shtml news",
        # "http://www.cq.chinanews.com/more/26.shtml news",
        # "http://www.cq.chinanews.com/more/21.shtml news",
        # "http://www.cq.chinanews.com/more/jyxw.shtml news",
        # "http://www.cq.chinanews.com/more/25.shtml news",
        # "http://www.cq.chinanews.com/more/33.shtml news",
        # "http://www.cq.chinanews.com/more/gatq.shtml news",
        # "http://www.cq.chinanews.com/more/32.shtml news",
        # "http://www.cq.chinanews.com/more/sqpl.shtml news",
        # "http://www.cq.chinanews.com/more/zxfw.shtml news",
        # "http://www.fj.chinanews.com/fjnews/ttgz/list.html news",
        # "http://www.fj.chinanews.com/fjnews/sjkfj/list.html news",
        # "http://www.fj.chinanews.com/fjnews/fjzzs/list.html news",
        # "http://www.fj.chinanews.com/fjnews/qlxdb/list.html news",
        # "http://www.fj.chinanews.com/fjnews/jsxw/list.html news",
        # "http://www.fj.chinanews.com/fjnews/zxyc/list.html news",
        # "http://www.fj.chinanews.com/fjnews/zbgat/list.html news",
        # "http://www.fj.chinanews.com/fjnews/zxsp/list.html news",
        # "http://www.fj.chinanews.com/fjnews/wz/list.html news",
        # "http://www.fj.chinanews.com/fjnews/all_news.html news",
        # "http://www.gs.chinanews.com/gdxw/index.html news",
        # "http://www.gs.chinanews.com/qykx1/m1.html news",
        # "http://www.gs.chinanews.com/lywx1/m1.html news",
        # "http://www.gs.chinanews.com/rsrm/m1.html news",
        # "http://www.gs.chinanews.com/tyxw1/m1.html news",
        # "http://www.gs.chinanews.com/wsxw/m1.html news",
        # "http://www.gs.chinanews.com/tpxw1/m1.html news",
        # "http://www.gs.chinanews.com/qzlx1/m1.html news",
        # "http://www.gs.chinanews.com/dscy/m1.html news",
        # "http://www.gs.chinanews.com/slxy1/m1.html news",
        # "http://www.gs.chinanews.com/gsly1/m1.html news",
        # "http://www.gs.chinanews.com/sp/xwsd.html news",
        # "http://www.gs.chinanews.com/sp/shbl.html news",
        # "http://www.gs.chinanews.com/sp/wyly.html news",
        # "http://www.gs.chinanews.com/sp/kjtw.html news",
        # "http://www.gs.chinanews.com/sp/jjzf.html news",
        # "http://www.gs.chinanews.com/jrtt1/m1.html news",
        # "http://www.gs.chinanews.com/hwkgs1/m1.html news",
        # "http://www.gs.chinanews.com/gsgs60/m1.html news",
        # "http://www.gs.chinanews.com/ktszt/m1.html news",
        # "http://www.gs.chinanews.com/lzdl/m1.html news",
        # "http://www.gs.chinanews.com/mtkxq/m1.html news",
        # "http://www.gs.chinanews.com/lshzt/m1.html news",
        # "http://www.gs.chinanews.com/gshszh/m1.html news",
        # "http://www.gz.chinanews.com/jujiaoguizhou/index.shtml news",
        # "http://www.gz.chinanews.com/haiwaikanguizhou/index.shtml news",
        # "http://www.gz.chinanews.com/guanzhu/index.shtml news",
        # "http://www.gz.chinanews.com/xiaokang/index.shtml news",
        # "http://www.gz.chinanews.com/lvyou/index.shtml news",
        # "http://www.gz.chinanews.com/shenghuo/index.shtml news",
        # "http://www.gz.chinanews.com/jujiaoguizhou/news/index.shtml news",
        # "http://www.gz.chinanews.com/jujiaoguizhou/zhengwurenshi/index.shtml news",
        # "http://www.gz.chinanews.com/jujiaoguizhou/cnsztsjw/index.shtml news",
        # "http://www.gz.chinanews.com/guanzhu/kanguizhou/index.shtml news",
        # "http://www.gz.chinanews.com/guanzhu/fangtan/index.shtml news",
        # "http://www.gz.chinanews.com/shizhou/index.shtml news",
        # "http://www.gz.chinanews.com/xiaokang/chanjing/index.shtml news",
        # "http://www.gz.chinanews.com/xiaokang/shengtai/index.shtml news",
        # "http://www.gz.chinanews.com/xiaokang/jiaotong/index.shtml news",
        # "http://www.gz.chinanews.com/xiaokang/dangjian/index.shtml news",
        # "http://www.gz.chinanews.com/shehui/minsheng/index.shtml news",
        # "http://www.gz.chinanews.com/shehui/jingfa/index.shtml news",
        # "http://www.gz.chinanews.com/shehui/tiyu/index.shtml news",
        # "http://www.gz.chinanews.com/shehui/gongyi/index.shtml news",
        # "http://www.gz.chinanews.com/lvyou/dongtai/index.shtml news",
        # "http://www.gz.chinanews.com/lvyou/yuanchengtai/index.shtml news",
        # "http://www.gz.chinanews.com/lvyou/jingqu/index.shtml news",
        # "http://www.gz.chinanews.com/shenghuo/qiyezixun/index.shtml news",
        # "http://www.gz.chinanews.com/shenghuo/qiche/index.shtml news",
        # "http://www.gz.chinanews.com/shenghuo/jiangkang/index.shtml news",
        # "http://www.gd.chinanews.com/index/spzx.html news",
        # "http://www.gd.chinanews.com/index/heib.html news",
        # "http://www.gd.chinanews.com/index/hongb.html news",
        # "http://www.gx.chinanews.com/top/ news",
        # "http://www.gx.chinanews.com/sz/ news",
        # "http://www.gx.chinanews.com/cj/ news",
        # "http://www.gx.chinanews.com/sh/ news",
        # "http://www.gx.chinanews.com/kjwt/ news",
        # "http://www.gx.chinanews.com/gatq/ news",
        # "http://www.gx.chinanews.com/dmsz/ news",
        # "http://www.gx.chinanews.com/dmjj/ news",
        # "http://www.gx.chinanews.com/dmsh/ news",
        # "http://www.gx.chinanews.com/dmwt/ news",
        # "http://www.gx.chinanews.com/gxgd/ news",
        # "http://www.gx.chinanews.com/ly/ news",
        # "http://www.gx.chinanews.com/jr/ news",
        # "http://www.gx.chinanews.com/qc/ news",
        # "http://www.gx.chinanews.com/video/ news",
        # "http://www.gx.chinanews.com/jqzh/ news",
        # "http://www.gx.chinanews.com/xfwq/ news",
        # "http://www.gx.chinanews.com/mt/ news",
        # "http://www.gx.chinanews.com/special/gxzy/ news",
        # "http://www.gx.chinanews.com/special/lzjx/ news",
        # "http://www.gx.chinanews.com/special/lzjt/ news",
        # "http://www.gx.chinanews.com/special/lbfy/ news",
        # "http://www.hi.chinanews.com/travel/more/19.html news",
        # "http://www.hi.chinanews.com/travel/more/20.html news",
        # "http://www.hi.chinanews.com/travel/more/22.html news",
        # "http://www.hi.chinanews.com/travel/more/21.html news",
        # "http://www.hi.chinanews.com/travel/more/31.html news",
        # "http://www.hi.chinanews.com/travel/more/27.html news",
        # "http://www.hi.chinanews.com/jrtt.html news",
        # "http://www.hi.chinanews.com/gundong/shxw.html news",
        # "http://www.hi.chinanews.com/gundong/hnzw.html news",
        # "http://www.hi.chinanews.com/gundong/jyxw.html news",
        # "http://www.hi.chinanews.com/gundong/guoji.html news",
        # "http://www.hi.chinanews.com/gundong/wenshi.html news",
        # "http://www.hi.chinanews.com/gundong/tiyu.html news",
        # "http://www.hi.chinanews.com/nk/more/45.html news",
        # "http://www.hi.chinanews.com/nk/more/44.html news",
        # "http://www.hi.chinanews.com/nk/more/48.html news",
        # "http://www.hi.chinanews.com/nk/more/50.html news",
        # "http://www.hi.chinanews.com/nk/more/51.html news",
        # "http://www.hi.chinanews.com/nk/more/52.html news",
        # "http://www.hi.chinanews.com/nk/more/54.html news",
        # "http://www.hi.chinanews.com/nk/more/55.html news",
        # "http://www.hi.chinanews.com/nk/more/59.html news",
        # "http://www.hi.chinanews.com/nk/more/49.html news",
        # "http://www.hi.chinanews.com/nk/more/46.html news",
        # "http://www.hi.chinanews.com/nk/more/47.html news",
        # "http://www.hi.chinanews.com/nk/more/53.html news",
        # "http://www.hi.chinanews.com/nk/more/58.html news",
        # "http://www.hi.chinanews.com/movie/more/170.html news",
        # "http://www.hi.chinanews.com/movie/more/169.html news",
        # "http://www.hi.chinanews.com/movie/more/171.html news",
        # "http://www.hi.chinanews.com/movie/more/172.html news",
        # "http://www.hi.chinanews.com/movie/more/173.html news",
        # "http://www.hi.chinanews.com/movie/more/174.html news",
        # "http://www.hi.chinanews.com/movie/more/176.html news",
        # "http://www.hi.chinanews.com/picmore/6.html news",
        # "http://www.hi.chinanews.com/picmore/7.html news",
        # "http://www.hi.chinanews.com/picmore/8.html news",
        # "http://www.hi.chinanews.com/picmore/9.html news",
        # "http://www.hi.chinanews.com/picmore/10.html news",
        # "http://www.hi.chinanews.com/shiyao/more/177.html news",
        # "http://www.hi.chinanews.com/shiyao/more/178.html news",
        # "http://www.hi.chinanews.com/shiyao/more/181.html news",
        # "http://www.hi.chinanews.com/shiyao/more/188.html news",
        # "http://www.hi.chinanews.com/shiyao/more/184.html news",
        # "http://www.hi.chinanews.com/shiyao/more/212.html news",
        # "http://www.hi.chinanews.com/shiyao/more/187.html news",
        # "http://www.hi.chinanews.com/zixun/more/64.html news",
        # "http://www.hi.chinanews.com/zixun/more/79.html news",
        # "http://www.hi.chinanews.com/gundong/zhbb.html news",
        # "http://www.hi.chinanews.com/gundong/yliao.html news",
        # "http://www.hi.chinanews.com/gundong/72.html news",
        # "http://www.hi.chinanews.com/gundong/qdfl.html news",
        # "http://www.hi.chinanews.com/gundong/wbhn.html news",
        # "http://www.hi.chinanews.com/zixun/more/60.html news",
        # "http://www.hi.chinanews.com/zixun/more/62.html news",
        # "http://www.hi.chinanews.com/zixun/more/61.html news",
        # "http://www.hi.chinanews.com/zixun/more/63.html news",
        # "http://www.hi.chinanews.com/zixun/more/76.html news",
        # "http://www.hi.chinanews.com/zixun/more/78.html news",
        # "http://www.hi.chinanews.com/zixun/more/77.html news",
        # "http://www.hi.chinanews.com/zixun/more/75.html news",
        # "http://www.hi.chinanews.com/gundong/qdjw.html news",
        # "http://www.heb.chinanews.com/hbzy/334.shtml news",
        # "http://www.heb.chinanews.com/jjjjj/445.shtml news",
        # "http://www.heb.chinanews.com/xaxq/469.shtml news",
        # "http://www.heb.chinanews.com/shfz/327.shtml news",
        # "http://www.heb.chinanews.com/fazhi/490.shtml news",
        # "http://www.heb.chinanews.com/cjzx/329.shtml news",
        # "http://www.heb.chinanews.com/kjww/331.shtml news",
        # "http://www.heb.chinanews.com/ylxc/493.shtml news",
        # "http://www.heb.chinanews.com/jkqg/355.shtml news",
        # "http://www.heb.chinanews.com/shenghuo/491.shtml news",
        # "http://www.heb.chinanews.com/fc/495.shtml news",
        # "http://www.heb.chinanews.com/jiankang/492.shtml news",
        # "http://www.heb.chinanews.com/zxjzkhb/321.shtml news",
        # "http://www.heb.chinanews.com/xabj/479.shtml news",
        # "http://www.heb.chinanews.com/part/69/hwkhb.html news",
        # "http://www.heb.chinanews.com/hbqs/476.shtml news",
        "http://www.heb.chinanews.com/zgxwzk/338.shtml news",
        "http://www.heb.chinanews.com/more/tupian.shtml news",
        # "http://www.ha.chinanews.com/news/hnxw/ news",
        # "http://www.ha.chinanews.com/news/jdtp/ news",
        # "http://www.ha.chinanews.com/news/hntx/ news",
        # "http://www.ha.chinanews.com/news/hncj/ news",
        # "http://www.ha.chinanews.com/news/hnjk/ news",
        # "http://www.ha.chinanews.com/news/hnly/ news",
        # "http://www.ha.chinanews.com/news/hnjy/ news",
        # "http://www.ha.chinanews.com/news/khn/ news",
        # "http://www.ha.chinanews.com/news/hnzf/ news",
        # "http://www.ha.chinanews.com/news/hncs/ news",
        # "http://www.ha.chinanews.com/news/hntc/index.shtml news",
        # "http://www.ha.chinanews.com/news/fphn/ news",
        # "http://www.ha.chinanews.com/news/aqkt/ news",
        # "http://www.ha.chinanews.com/news/hnty/index.shtml news",
        # "http://www.ha.chinanews.com/news/myhn/index.shtml news",
        # "http://www.ha.chinanews.com/news/jdxw/index.shtml news",
        # "http://www.ha.chinanews.com/news/jddt/index.shtml news",
        # "http://www.ha.chinanews.com/news/jdfl/index.shtml news",
        # "http://www.ha.chinanews.com/news/jdfy/index.shtml news",
        # "http://www.hb.chinanews.com/ss.html news",
        # "http://www.hb.chinanews.com/photo/hubei.html news",
        # "http://www.hb.chinanews.com/photo/world.html#main news",
        # "http://www.hb.chinanews.com/photo/ent.html#main news",
        # "http://www.hb.chinanews.com/photo/travel.html#main news",
        # "http://www.hb.chinanews.com/photo/fun.html#main news",
        # "http://www.hn.chinanews.com/news/hwmtkhn/index.shtml news",
        # "http://www.hn.chinanews.com/news/hwsj/ news",
        # "http://www.hn.chinanews.com/news/shsh/index.shtml news",
        # "http://www.hn.chinanews.com/news/gyyq/ news",
        # "http://www.hn.chinanews.com/news/dgzs/index.shtml news",
        # "http://www.hn.chinanews.com/news/xzwxfc/index.shtml news",
        # "http://www.hn.chinanews.com/news/gmaq/index.shtml news",
        # "http://www.hn.chinanews.com/news/zlts/index.shtml news",
        # "http://www.hn.chinanews.com/news/yhfw/index.shtml news",
        # "http://www.hn.chinanews.com/news/cjzx/index.shtml news",
        # "http://www.hn.chinanews.com/news/hnjj/index.shtml news",
        "http://www.hn.chinanews.com/news/sdbd/index.shtml news",
        "http://www.hn.chinanews.com/news/cjsxdt/index.shtml news",
        # "http://www.hlj.chinanews.com/focus/zfjw.html news",
        # "http://www.hlj.chinanews.com/focus/cjqy.html news",
        # "http://www.hlj.chinanews.com/focus/whly.html news",
        # "http://www.hlj.chinanews.com/focus/sgnksy.html news",
        # "http://www.hlj.chinanews.com/focus/dsbb.html news",
        # "http://www.hlj.chinanews.com/focus/blpt.html news",
        # "http://www.hlj.chinanews.com/focus/lylj.html news",
        # "http://www.js.chinanews.com/video/citynews/ news",
        # "http://www.js.chinanews.com/video/science/ news",
        # "http://www.js.chinanews.com/video/overseas/ news",
        # "http://www.js.chinanews.com/video/tour/ news",
        # "http://www.js.chinanews.com/video/special/ news",
        # "http://www.jl.chinanews.com/jlyw/index.shtml news",
        # "http://www.jl.chinanews.com/shidian/index.shtml news",
        # "http://www.jl.chinanews.com/hqrd/index.shtml news",
        # "http://www.jl.chinanews.com/gnyw/index.shtml news",
        # "http://www.jl.chinanews.com/tsjl/index.shtml news",
        # "http://www.jl.chinanews.com/szjj/index.shtml news",
        # "http://www.jl.chinanews.com/cjbd/index.shtml news",
        # "http://www.jl.chinanews.com/shms/index.shtml news",
        # "http://www.jl.chinanews.com/kjww/index.shtml news",
        # "http://www.jl.chinanews.com/sdgc/index.shtml news",
        # "http://www.jl.chinanews.com/tbgz/index.shtml news",
        # "http://www.jl.chinanews.com/rszl/index.shtml news",
        # "http://www.jl.chinanews.com/gclt/index.shtml news",
        # "http://www.jl.chinanews.com/jlly/index.shtml news",
        # "http://www.jl.chinanews.com/rsbd/index.shtml news",
        # "http://www.jl.chinanews.com/mqtj/index.shtml news",
        # "http://www.jl.chinanews.com/gatq/index.shtml news",
        # "http://www.jl.chinanews.com/msfq/index.shtml news",
        # "http://www.jl.chinanews.com/jkzx/index.shtml news",
        # "http://www.jl.chinanews.com/dcls/index.shtml news",
        # "http://www.jl.chinanews.com/wcjl/index.shtml news",
        # "http://www.jl.chinanews.com/bwrs/index.shtml news",
        # "http://www.jl.chinanews.com/hyhc/index.shtml news",
        # "http://www.jl.chinanews.com/qccy/index.shtml news",
        # "http://www.jl.chinanews.com/jwmtsjl/index.shtml news",
        # "http://www.jl.chinanews.com/zxsjzzl/index.shtml news",
        # "http://www.jl.chinanews.com/xwfbh/index.shtml news",
        # "http://www.ln.chinanews.com/shipin/index.shtml news",
        # "http://www.ln.chinanews.com/dfxw/index.shtml news",
        # "http://www.nmg.chinanews.com/zxxw/index.html news",
        # "http://www.nmg.chinanews.com/nmgxw/index.html news",
        # "http://www.nmg.chinanews.com/zxtp/index.html news",
        # "http://www.nmg.chinanews.com/kjww/index.html news",
        # "http://www.nmg.chinanews.com/zlqqzxd/index.html news",
        # "http://www.nmg.chinanews.com/msdt/index.html news",
        # "http://www.nmg.chinanews.com/hlnmg/index.html news",
        # "http://www.nmg.chinanews.com/shjd/index.html news",
        # "http://www.nmg.chinanews.com/jyzx/index.html news",
        # "http://www.nmg.chinanews.com/qyxw/index.html news",
        # "http://www.nmg.chinanews.com/nmgjy/index.html news",
        # "http://www.nmg.chinanews.com/bxsh/index.html news",
        # "http://www.nmg.chinanews.com/gatrd/index.html news",
        # "http://www.nmg.chinanews.com/zxsj/index.html news",
        # "http://www.qh.chinanews.com/yw/index.shtml news",
        # "http://www.qh.chinanews.com/hwkqh/index.shtml news",
        # "http://www.qh.chinanews.com/zxjzzqh/index.shtml news",
        # "http://www.qh.chinanews.com/qhsp/index.shtml news",
        # "http://www.qh.chinanews.com/dsp/index.shtml news",
        # "http://www.qh.chinanews.com/zb/index.shtml news",
        # "http://www.qh.chinanews.com/qhgd/index.shtml news",
        # "http://www.qh.chinanews.com/dj/index.shtml news",
        # "http://www.qh.chinanews.com/zq/index.shtml news",
        # "http://www.qh.chinanews.com/sh/index.shtml news",
        # "http://www.qh.chinanews.com/cj/index.shtml news",
        # "http://www.qh.chinanews.com/ty/index.shtml news",
        # "http://www.qh.chinanews.com/wy/index.shtml news",
        # "http://www.qh.chinanews.com/kj/index.shtml news",
        # "http://www.qh.chinanews.com/st/index.shtml news",
        # "http://www.qh.chinanews.com/xmt/index.shtml news",
        # "http://www.sx.chinanews.com/list/yaowen.html news",
        # "http://www.sx.chinanews.com/list/guanzhu.html news",
        # "http://www.sx.chinanews.com/list/shanxi.html news",
        # "http://www.sx.chinanews.com/list/bwsp.html news",
        # "http://www.sx.chinanews.com/list/jujiao.html news",
        # "http://www.sx.chinanews.com/list/shizheng.html news",
        # "http://www.sx.chinanews.com/list/caijing.html news",
        # "http://www.sx.chinanews.com/list/sxbaoxian.html news",
        # "http://www.sx.chinanews.com/list/bank.html news",
        # "http://www.sx.chinanews.com/list/shehui.html news",
        # "http://www.sx.chinanews.com/list/chengshi.html news",
        # "http://www.sx.chinanews.com/list/xingxian.html news",
        # "http://www.sx.chinanews.com/list/yaodu.html news",
        # "http://www.sx.chinanews.com/list/xtm.html news",
        # "http://www.sx.chinanews.com/list/lvyou.html news",
        # "http://www.sx.chinanews.com/list/wenhua.html news",
        # "http://www.sx.chinanews.com/list/jiaoyu.html news",
        # "http://www.sx.chinanews.com/list/tiyu.html news",
        # "http://www.sx.chinanews.com/health/list/8.html news",
        # "http://www.sx.chinanews.com/list/pinglun.html news",
        # "http://www.sx.chinanews.com/list/puzhou.html news",
        # "http://www.sx.chinanews.com/list/czcq.html news",
        # "http://www.sx.chinanews.com/list/pic.html news",
        # "http://www.sx.chinanews.com/linfen/list/2.html news",
        # "http://www.sx.chinanews.com/linfen/list/1.html news",
        # "http://www.sx.chinanews.com/linfen/list/3.html news",
        # "http://www.sx.chinanews.com/linfen/list/4.html news",
        # "http://www.sx.chinanews.com/linfen/list/5.html news",
        # "http://www.sx.chinanews.com/linfen/list/6.html news",
        # "http://www.sx.chinanews.com/linfen/list/7.html news",
        # "http://www.shx.chinanews.com/rsrm.html news",
        # "http://www.shx.chinanews.com/zwjs.html news",
        # "http://www.sh.chinanews.com/wenhua/index.shtml news",
        # "http://www.sh.chinanews.com/tiyu/index.shtml news",
        # "http://www.sh.chinanews.com/shishang/index.shtml news",
        # "http://www.sh.chinanews.com/yule/index.shtml news",
        # "http://www.sh.chinanews.com/ckzx/index.shtml news",
        # "http://www.sh.chinanews.com/chanjing/index.shtml news",
        # "http://www.sh.chinanews.com/jinrong/index.shtml news",
        # "http://www.sh.chinanews.com/loushi/index.shtml news",
        # "http://www.sh.chinanews.com/hgjj/index.shtml news",
        # "http://www.sh.chinanews.com/bdrd/index.shtml news",
        # "http://www.sh.chinanews.com/yljk/index.shtml news",
        # "http://www.sh.chinanews.com/kjjy/index.shtml news",
        # "http://www.sh.chinanews.com/fzzx/index.shtml news",
        # "http://www.sh.chinanews.com/fengxian/index.shtml news",
        # "http://www.sh.chinanews.com/ckgs/index.shtml news",
        # "http://www.sh.chinanews.com/dangjian/index.shtml news",
        # "http://www.sc.chinanews.com/scxw/index.shtml news",
        # "http://www.sc.chinanews.com/glgj/index.shtml news",
        # "http://www.sc.chinanews.com/bwbd/index.shtml news",
        # "http://www.sc.chinanews.com/tpxw/index.shtml news",
        # "http://www.sc.chinanews.com/szjj/index.shtml news",
        # "http://www.sc.chinanews.com/spxw/index.shtml news",
        # "http://www.sc.chinanews.com/szbd/index.shtml news",
        # "http://www.sc.chinanews.com/zxjzzsc/index.shtml news",
        # "http://www.sc.chinanews.com/gatq/index.shtml news",
        # "http://www.sc.chinanews.com/cjbd/index.shtml news",
        # "http://www.sc.chinanews.com/ylss/index.shtml news",
        # "http://www.sc.chinanews.com/hwmtksc/index.shtml news",
        # "http://www.sc.chinanews.com/shms/index.shtml news",
        # "http://www.sc.chinanews.com/lyxw/index.shtml news",
        # "http://www.sc.chinanews.com/whty/index.shtml news",
        # "http://www.sc.chinanews.com/shfw/index.shtml news",
        # "http://www.sc.chinanews.com/kjws/index.shtml news",
        # "http://www.sc.chinanews.com/fctt/index.shtml news",
        # "http://www.sc.chinanews.com/gsbd/index.shtml news",
        # "http://www.sc.chinanews.com/scyw/index.shtml news",
        # "http://www.sc.chinanews.com/zcdt/index.shtml news",
        # "http://www.xj.chinanews.com/tupian/pic.d.html?nid=61 news",
        # "http://www.xj.chinanews.com/tupian/pic.d.html?nid=62 news",
        # "http://www.xj.chinanews.com/xinjiang/xjyw.d.html?nid=63 news",
        # "http://www.xj.chinanews.com/xinjiang/xjyw.d.html?nid=64 news",
        # "http://www.xj.chinanews.com/xinjiang/xjyw.d.html?nid=65 news",
        # "http://www.xj.chinanews.com/xinjiang/xjyw.d.html?nid=66 news",
        # "http://www.xj.chinanews.com/xinjiang/xjyw.d.html?nid=67 news",
        # "http://www.xj.chinanews.com/xinjiang/xjyw.d.html?nid=68 news",
        # "http://www.xj.chinanews.com/xinjiang/xjyw.d.html?nid=69 news",
        # "http://www.xj.chinanews.com/xinjiang/xjyw.d.html?nid=70 news",
        # "http://www.xj.chinanews.com/xinjiang/xjyw.d.html?nid=71 news",
        # "http://www.xj.chinanews.com/xinjiang/xjyw.d.html?nid=72 news",
        # "http://www.xj.chinanews.com/tupian/pic.d.html?nid=73 news",
        # "http://www.xj.chinanews.com/xinjiang/xjyw.d.html?nid=74 news",
        # "http://www.xj.chinanews.com/xinjiang/xjyw.d.html?nid=75 news",
        # "http://www.bt.chinanews.com/xinjiang/index.shtml news",
        # "http://www.yn.chinanews.com/zxsd/index.shtml news",
        # "http://www.yn.chinanews.com/sp/index.shtml news",
        # "http://www.yn.chinanews.com/qw/index.shtml news",
        # "http://www.yn.chinanews.com/dmny/index.shtml news",
        # "http://www.yn.chinanews.com/fszx/index.shtml news",
        # "http://www.yn.chinanews.com/mztj/index.shtml news",
        # "http://www.yn.chinanews.com/stwm/index.shtml news",
        # "http://www.yn.chinanews.com/zsdt/index.shtml news",
        # "http://www.yn.chinanews.com/yl/index.shtml news",
        # "http://www.yn.chinanews.com/ly/index.shtml news",
        # "http://www.yn.chinanews.com/edu/index.shtml news",
        # "http://www.yn.chinanews.com/qyzx/index.shtml news",
        # "http://www.yn.chinanews.com/gyts/index.shtml news",
        # "http://www.yn.chinanews.com/car/index.shtml news",
        # "http://www.yn.chinanews.com/fc/index.shtml news",
        # "http://www.yn.chinanews.com/cj/index.shtml news",
        # "http://www.yn.chinanews.com/tpgj/index.shtml news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=50 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=272 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=273 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=276 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=277 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=278 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=280 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=282 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=281 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=283 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=285 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=287 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=291 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=288 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=289 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=290 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=292 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=293 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=294 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=295 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=297 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=299 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=302 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=303 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=304 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=305 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=301 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=307 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=313 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=308 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=309 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=310 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=311 news",
        # "http://www.zj.chinanews.com/yw/zjyw.d.html?nid=312 news",
        # "http://www.chinanews.com/photo/gnjj.html news",
        # "http://www.chinanews.com/photo/shbt.html news",
        # "http://www.gs.chinanews.com/whws1/m1.html news",
        # "http://www.chinanews.com/entertainment/photo/gzjtphoto-1.html news",
        # "http://www.chinanews.com/photo/ylty.html news",
        # "http://www.chinanews.com/scroll-news/news1.html news",
        # "http://www.gs.chinanews.com/kjxw1/m1.html news",
        # "http://www.gs.chinanews.com/wsqw1/m1.html news",
        # "http://www.gs.chinanews.com/gsyw1/m1.html news",
        # "http://www.gs.chinanews.com/dishi/gannan.htm news",
        # "http://www.gs.chinanews.com/zwrs1/m1.html news",
        # "http://www.gs.chinanews.com/shms1/m1.html news",
        # "http://www.gs.chinanews.com/fzxw/m1.html news",
        # "http://www.gs.chinanews.com/jjxw1/m1.html news",
        # "http://www.yn.chinanews.com/pub/caijing/ news",
        # "http://www.yn.chinanews.com/pub/news/world/guonei/ news",
        # "http://www.yn.chinanews.com/pub/news/sudi/ news",
        # "http://www.js.chinanews.com/business/ news",
        # "http://www.js.chinanews.com/citynews/ news",
        # "http://www.js.chinanews.com/sports/ news",
        # "http://www.js.chinanews.com/science/ news",
        # "http://www.js.chinanews.com/county/ news",
        # "http://www.js.chinanews.com/video/ news",
        # "http://www.gz.chinanews.com/shehui/index.shtml news",
        # "http://energy.chinanews.com/ news",
        # "http://it.chinanews.com/ news",
        # "http://channel.chinanews.com/cns/cl/mil-fwgc.shtml news",
        # "http://channel.chinanews.com/cns/cl/ga-cl.shtml news",
        # "http://www.gd.chinanews.com/index/wsbl.html news",
        "http://www.hn.chinanews.com/hnjjdy/jjzh/index1.html news",
        # "http://www.zj.chinanews.com/cj/zc/index.html news",
        # "http://www.zj.chinanews.com/sh/zjty/index.html news",
        # "http://www.zj.chinanews.com/sh/tycy/index.html news",
        # "http://www.zj.chinanews.com/qt/qtdt/index.html news",
        # "http://www.zj.chinanews.com/zjskzj.html news",
        # "http://www.zj.chinanews.com/jy/yey/index.html news",
        # "http://www.zj.chinanews.com/cj/jr/index.html news",
        # "http://www.zj.chinanews.com/sj/tj/index.html news",
        # "http://www.zj.chinanews.com/cj/zs/index.html news",
        # "http://www.zj.chinanews.com/sh/tsly/index.html news",
        # "http://www.zj.chinanews.com/qt/zhw/index.html news",
        # "http://www.zj.chinanews.com/qt/ssd/index.html news",
        # "http://www.zj.chinanews.com/wy/yy/index.html news",
        # "http://www.zj.chinanews.com/qt/qtws/index.html news",
        # "http://www.zj.chinanews.com/sj/sp/index.html news",
        # "http://www.zj.chinanews.com/qt/tsqt/index.html news",
        # "http://www.zj.chinanews.com/jy/zxx/index.html news",
        # "http://www.zj.chinanews.com/sj/jxzj/index.html news",
        # "http://www.zj.chinanews.com/wy/whzl/index.html news",
        # "http://www.zj.chinanews.com/qt/rwfc/index.html news",
        # "http://www.zj.chinanews.com/jy/yr/index.html news",
        # "http://www.zj.chinanews.com/wy/fy/index.html news",
        # "http://www.zj.chinanews.com/qt/hmzy/index.html news",
        # "http://www.zj.chinanews.com/wy/sp/index.html news",
        # "http://www.zj.chinanews.com/qt/gyh/index.html news",
        # "http://www.zj.chinanews.com/qt/zcgg/index.html news",
        # "http://www.zj.chinanews.com/sh/ysyl/index.html news",
        # "http://www.zj.chinanews.com/qt/qszs/index.html news",
        # "http://www.zj.chinanews.com/qt/qtjj/index.html news",
        # "http://www.zj.chinanews.com/jy/zgz/index.html news",
        # "http://www.hb.chinanews.com/gatq.html news",
        "http://www.heb.chinanews.com/4/20111018/325.shtml news",
        # "http://www.gd.chinanews.com/index/zxtp.html news",
        # "http://channel.chinanews.com/cns/cl/cul-kgfx.shtml news",
        # "http://channel.chinanews.com/u/cul/cul-whsp.shtml news",
        # "http://channel.chinanews.com/cns/cl/cul-gxzy.shtml news",
        # "http://channel.chinanews.com/cns/cl/hb-shgc.shtml news",
        # "http://channel.chinanews.com/cns/cl/auto-rscs.shtml news",
        # "http://channel.chinanews.com/u/cul/cul-xsjs.shtml news",
        # "http://channel.chinanews.com/cns/cl/cul-mjzy.shtml news",
        # "http://channel.chinanews.com/cns/cl/cul-shfz.shtml news",
        # "http://channel.chinanews.com/cns/cl/hwjy-lwxzw.shtml news",
        # "http://channel.chinanews.com/cns/cl/zgqj-sqfg.shtml news",
        # "http://channel.chinanews.com/cns/cl/hwjy-hjsp.shtml news",
        # "http://channel.chinanews.com/cns/cl/fortune-hjcp.shtml news",
        # "http://channel.chinanews.com/cns/cl/hb-zcqs.shtml news",
        # "http://channel.chinanews.com/cns/cl/hb-qgsd.shtml news",
        # "http://channel.chinanews.com/cns/cl/zgqj-hqnc.shtml news",
        # "http://channel.chinanews.com/cns/cl/fortune-lcs.shtml news",
        # "http://channel.chinanews.com/cns/cl/fortune-th.shtml news",
        # "http://channel.chinanews.com/cns/cl/estate-zxjzb.shtml news",
        # "http://channel.chinanews.com/cns/cl/fortune-yhj.shtml news",
        # "http://channel.chinanews.com/cns/cl/hwjy-zwjl.shtml news",
        # "http://channel.chinanews.com/cns/cl/fortune-ytjr.shtml news",
        # "http://channel.chinanews.com/u/cul/cul-whlx.shtml news",
        # "http://channel.chinanews.com/cns/cl/cul-bwg.shtml news",
        # "http://channel.chinanews.com/u/yl/djzb.shtml news",
        "http://www.heb.chinanews.com/4/20111018/343.shtml news",
        # "http://channel.chinanews.com/cns/cl/cul-wssm.shtml news",
        # "http://channel.chinanews.com/cns/cl/cul-xjgw.shtml news",
        # "http://www.chinanews.com/compatriot.shtml news",
        # "http://www.hi.chinanews.com/gundong/szxw.html news",
        # "http://www.hi.chinanews.com/gundong/jjxw.html news",
        # "http://www.hi.chinanews.com/gundong/dwnews.html news",
        # "http://channel.chinanews.com/cns/cl/hwjy-qzgx.shtml news",
        # "http://www.hb.chinanews.com/travel.html news",
        # "http://www.shx.chinanews.com/jcca.html news",
        # "http://www.js.chinanews.com/nomocracy/ news",
        "http://www.hn.chinanews.com/news/cnsdc/ news",
        # "http://www.bj.chinanews.com/focus/4.html news",
        # "http://www.bj.chinanews.com/focus/6.html news",
        # "http://www.bj.chinanews.com/focus/2.html news",
        # "http://www.bj.chinanews.com/focus/7.html news",
        # "http://www.bj.chinanews.com/focus/9.html news",
        # "http://www.fj.chinanews.com/new/pgt/list.shtml news",
        # "http://www.fj.chinanews.com/new/cjyw/list.shtml news",
        # "http://www.fj.chinanews.com/new/hwxq/list.shtml news",
        # "http://www.fj.chinanews.com/new/jjkd/list.shtml news",
        # "http://www.fj.chinanews.com/new/gacz/list.shtml news",
        # "http://www.fj.chinanews.com/new/xwrp/list.shtml news",
        # "http://www.fj.chinanews.com/new/thyw/list.shtml news",
        # "http://www.gs.chinanews.com/jywx1/m1.html news",
        # "http://www.gs.chinanews.com/jrtt1.html news",
        # "http://www.gs.chinanews.com/shms1.html news",
        # "http://www.gs.chinanews.com/yljd1.html news",
        # "http://www.gs.chinanews.com/jjxw1.html news",
        # "http://www.gs.chinanews.com/zwrs1.html news",
        # "http://www.shx.chinanews.com/shfz.html news",
        # "http://www.bj.chinanews.com/focus/5.html news",
        # "http://www.js.chinanews.com/overseas/ news",
        # "http://www.sx.chinanews.com/4/2009/0107/1.html news",
        # "http://www.hb.chinanews.com/cjxw.html news",
        # "http://www.hb.chinanews.com/jk.html news",
        # "http://www.hb.chinanews.com/shipin/more.html news",
        # "http://www.sx.chinanews.com/4/2009/0727/15.html news",
        # "http://www.sx.chinanews.com/4/2009/0728/21.html news",
        # "http://www.shx.chinanews.com/wmksx.html news",
        # "http://www.shx.chinanews.com/sxxw.html news",
        # "http://channel.chinanews.com/cns/cl/edu-jygg.shtml news",
        # "http://channel.chinanews.com/cns/cl/fortune-dfyh.shtml news",
        # "http://channel.chinanews.com/cns/cl/gj-sjkj.shtml news",
        # "http://channel.chinanews.com/cns/cl/hb-scwj.shtml news",
        # "http://www.hi.chinanews.com/gundong/guonei.html news",
        # "http://house.chinanews.com/#tudi news",
        # "http://channel.chinanews.com/cns/cl/estate-jjjj.shtml news",
        # "http://channel.chinanews.com/cns/cl/estate-om.shtml news",
        # "http://channel.chinanews.com/cns/cl/estate-tdxw.shtml news",
        # "http://channel.chinanews.com/cns/cl/estate-xf.shtml news",
        # "http://channel.chinanews.com/cns/cl/estate-zj.shtml news",
        # "http://www.shx.chinanews.com/dswy.html news",
        # "http://www.chinanews.com/news/tjyd/more_1.shtml news",
        # "http://channel.chinanews.com/cns/cl/it-sdpl.shtml news",
        # "http://channel.chinanews.com/cns/cl/life-sdd.shtml news",
        # "http://www.shx.chinanews.com/ylty.html news",
        # "http://www.hb.chinanews.com/kjww.html news",
        # "http://energy.chinanews.com/#lssh news",
        # "http://channel.chinanews.com/cns/cl/ny-xny.shtml news",
        # "http://channel.chinanews.com/cns/cl/ny-hn.shtml news",
        # "http://channel.chinanews.com/cns/cl/ny-sysh.shtml news",
        # "http://channel.chinanews.com/cns/cl/ny-trq.shtml news",
        # "http://channel.chinanews.com/cns/cl/ny-sldl.shtml news",
        # "http://www.chinanews.com/stock/gd.shtml news",
        # "http://www.chinanews.com/energy/news.shtml news",
        # "http://www.chinanews.com/stock/news.shtml news",
        # "http://www.chinanews.com/health.shtml news",
        # "http://www.chinanews.com/world.shtml news",
        # "http://www.chinanews.com/hb.shtml news",
        # "http://www.chinanews.com/keji.shtml news",
        # "http://finance.chinanews.com/cj/gd.shtml news",
        # "http://house.chinanews.com/#huanqiu news",
        # "http://house.chinanews.com/#ersf news",
        # "http://house.chinanews.com/#qynd news",
        # "http://house.chinanews.com/#jzkb news",
        # "http://house.chinanews.com/#dcq news",
        # "http://house.chinanews.com/#slc news",
        # "http://house.chinanews.com/#rtph news",
        # "http://house.chinanews.com/#sangy news",
        # "http://house.chinanews.com/#zyjff news",
        # "http://house.chinanews.com/#fdh news",
        # "http://house.chinanews.com/#wq news",
        # "http://house.chinanews.com/#gzdw news",
        # "http://house.chinanews.com/#kfsyl news",
        # "http://house.chinanews.com/#dcjr news",
        # "http://house.chinanews.com/#zxjc news",
        # "http://house.chinanews.com/#fq news",
        # "http://house.chinanews.com/#fqlb news",
        # "http://house.chinanews.com/#fqdtt news",
        # "http://house.chinanews.com/#dlh news",
        # "http://it.chinanews.com/#sdgc news",
        # "http://it.chinanews.com/#qydt news",
        # "http://it.chinanews.com/#sd news",
        # "http://it.chinanews.com/#rwsy news",
        # "http://it.chinanews.com/#bjb news",
        # "http://it.chinanews.com/#ztch news",
        # "http://it.chinanews.com/#zcjd news",
        # "http://it.chinanews.com/#yc news",
        # "http://it.chinanews.com/#jydq news",
        # "http://it.chinanews.com/#bg news",
        # "http://it.chinanews.com/#sj news",
        # "http://energy.chinanews.com/#qygy news",
        # "http://energy.chinanews.com/#dtsh news",
        # "http://energy.chinanews.com/#qqjz news",
        # "http://energy.chinanews.com/#lsxd news",
        # "http://energy.chinanews.com/#sysh news",
        # "http://energy.chinanews.com/#hn news",
        # "http://energy.chinanews.com/#yjzs news",
        # "http://energy.chinanews.com/#mt news",
        # "http://energy.chinanews.com/#trq news",
        # "http://energy.chinanews.com/#mq news",
        # "http://energy.chinanews.com/#stzxx news",
        # "http://energy.chinanews.com/#jnzz news",
        # "http://stock.chinanews.com/#gsnrb news",
        # "http://stock.chinanews.com/#dd-jrts news",
        # "http://stock.chinanews.com/#iframe-jrlzbk news",
        # "http://stock.chinanews.com/#tzzjy news",
        # "http://stock.chinanews.com/#qsyth news",
        # "http://stock.chinanews.com/#tabs2 news",
        # "http://stock.chinanews.com/#quanshang news",
        # "http://stock.chinanews.com/#ssgshhb news",
        # "http://stock.chinanews.com/#iframe-zssj news",
        # "http://stock.chinanews.com/#jijin news",
        # "http://stock.chinanews.com/#ggzz news",
        # "http://stock.chinanews.com/#iframe-qqgshq news",
        # "http://stock.chinanews.com/#jiaoyisuo news",
        # "http://stock.chinanews.com/#dd-gshqkb news",
        # "http://stock.chinanews.com/#ssgs news",
        # "http://stock.chinanews.com/#gzqh news",
        # "http://stock.chinanews.com/#jjp news",
        # "http://stock.chinanews.com/#iframe-hqzx news",
        # "http://channel.chinanews.com/cns/cl/zgqj-qsgc.shtml news",
        # "http://channel.chinanews.com/cns/cl/cul-cbdt.shtml news",
        # "http://channel.chinanews.com/cns/cl/cul-zsfy.shtml news",
        # "http://channel.chinanews.com/cns/cl/zgqj-qxsz.shtml news",
        # "http://channel.chinanews.com/cns/cl/cul-scpd.shtml news",
        # "http://channel.chinanews.com/cns/cl/fortune-zxjrb.shtml news",
        # "http://channel.chinanews.com/cns/cl/zgqj-fwjl.shtml news",
        # "http://channel.chinanews.com/u/sy/dsds.shtml news",
        # "http://channel.chinanews.com/u/yl/mixing.shtml news",
        # "http://channel.chinanews.com/cns/cl/zgqj-zgqx.shtml news",
        # "http://channel.chinanews.com/cns/cl/cul-wtjs.shtml news",
        # "http://channel.chinanews.com/cns/cl/zgqj-qjxx.shtml news",
        # "http://channel.chinanews.com/cns/cl/zgqj-yzyz.shtml news",
        # "http://channel.chinanews.com/cns/cl/hb-lcjn.shtml news",
        # "http://channel.chinanews.com/cns/cl/zgqj-qjxy.shtml news",
        # "http://channel.chinanews.com/cns/cl/hb-szlw.shtml news",
        # "http://channel.chinanews.com/cns/cl/zgqj-tpbd.shtml news",
        # "http://channel.chinanews.com/cns/cl/hb-wypp.shtml news",
        # "http://channel.chinanews.com/u/finance/gj.shtml news",
        # "http://channel.chinanews.com/cns/cl/fortune-whcp.shtml news",
        # "http://channel.chinanews.com/cns/cl/hwjy-hykt.shtml news",
        # "http://channel.chinanews.com/cns/cl/hb-hbtt.shtml news",
        # "http://channel.chinanews.com/cns/cl/auto-csh.shtml news",
        # "http://channel.chinanews.com/cns/cl/cul-whyc.shtml news",
        # "http://channel.chinanews.com/u/news/xyxy.shtml news",
        # "http://channel.chinanews.com/u/sy/music1.shtml news",
        # "http://channel.chinanews.com/cns/cl/hb-wysb.shtml news",
        # "http://channel.chinanews.com/cns/cl/cul-rwbk.shtml news",
        # "http://channel.chinanews.com/cns/cl/hb-gjss.shtml news",
        # "http://channel.chinanews.com/cns/cl/hb-rwmdm.shtml news",
        # "http://channel.chinanews.com/cns/cl/zgqj-gxjx.shtml news",
        # "http://channel.chinanews.com/cns/cl/zgqj-qkjc.shtml news",
        # "http://channel.chinanews.com/cns/cl/hb-mlyz.shtml news",
        # "http://channel.chinanews.com/cns/cl/hb-tgaq.shtml news",
        # "http://channel.chinanews.com/cns/cl/hwjy-hjzx.shtml news",
        # "http://channel.chinanews.com/cns/cl/fortune-zzyh.shtml news",
        # "http://channel.chinanews.com/cns/cl/fortune-cpjl.shtml news",
        # "http://channel.chinanews.com/cns/cl/zgqj-gqgs.shtml news",
        # "http://channel.chinanews.com/cns/cl/hb-jkys.shtml news",
        # "http://channel.chinanews.com/cns/cl/cul-ysxc.shtml news",
        # "http://channel.chinanews.com/cns/cl/hb-ghzh.shtml news",
        # "http://channel.chinanews.com/cns/cl/hwjy-xsxz.shtml news",
        # "http://channel.chinanews.com/cns/cl/hb-wssj.shtml news",
        # "http://channel.chinanews.com/cns/cl/hb-rzlt.shtml news",
        # "http://channel.chinanews.com/cns/cl/hwjy-xgzl.shtml news",
        # "http://channel.chinanews.com/cns/cl/auto-cxdb.shtml news",
        # "http://channel.chinanews.com/cns/cl/hb-ysnn.shtml news",
        # "http://channel.chinanews.com/cns/cl/yl-zykx.shtml news",
        # "http://channel.chinanews.com/u/finance/yw.shtml news",
        # "http://channel.chinanews.com/cns/cl/fortune-zqcp.shtml news",
        # "http://channel.chinanews.com/cns/cl/tw-msfq.shtml news",
        # "http://channel.chinanews.com/cns/cl/cul-rwcq.shtml news",
        # "http://channel.chinanews.com/cns/cl/cul-gjqt.shtml news",
        # "http://channel.chinanews.com/cns/cl/fortune-qhcp.shtml news",
        # "http://channel.chinanews.com/cns/cl/cul-cmyj.shtml news",
        # "http://channel.chinanews.com/cns/cl/tw-ylzy.shtml news",
        # "http://channel.chinanews.com/cns/cl/fortune-bxal.shtml news",
        # "http://channel.chinanews.com/cns/cl/hb-bfsj.shtml news",
        # "http://channel.chinanews.com/cns/cl/tw-tppd.shtml news",
        # "http://channel.chinanews.com/cns/cl/yl-zyy.shtml news",
        # "http://channel.chinanews.com/cns/cl/fortune-omjr.shtml news",
        # "http://channel.chinanews.com/cns/cl/hb-kjxz.shtml news",
        # "http://channel.chinanews.com/u/sy/dygd.shtml news",
        # "http://channel.chinanews.com/cns/cl/fortune-wzyh.shtml news",
        # "http://www.chinanews.com/fortune/news.shtml news",
        # "http://www.chinanews.com/mil/news.shtml news",
        # "http://www.chinanews.com/taiwan.shtml news",
        # "http://www.chinanews.com/estate.html news",
        # "http://www.chinanews.com/wenhua.shtml news",
        # "http://finance.chinanews.com/stock/gd.shtml news",
        # "http://www.chinanews.com/china.shtml news",
        # "http://www.chinanews.com/qiche.shtml news",
        # "http://channel.chinanews.com/cns/cl/ga-tlga.shtml news",
        # "http://channel.chinanews.com/cns/cl/mil-zgjqsclb.shtml news",
        # "http://channel.chinanews.com/cns/cl/mil-zgjqzgbhf.shtml news",
        # "http://channel.chinanews.com/cns/cl/mil-shyybqmw.shtml news",
        # "http://channel.chinanews.com/cns/cl/jk-mrhf.shtml news",
        # "http://channel.chinanews.com/cns/cl/cj-jjyw.shtml news",
        # "http://channel.chinanews.com/cns/cl/jk-ylgg.shtml news",
        # "http://channel.chinanews.com/cns/cl/gj-fxpl.shtml news",
        # "http://channel.chinanews.com/cns/cl/gj-rwbg.shtml news",
        # "http://channel.chinanews.com/cns/cl/fortune-zb.shtml news",
        # "http://channel.chinanews.com/cns/cl/fortune-yqgc.shtml news",
        # "http://channel.chinanews.com/cns/cl/jk-zypf.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-sqfg.shtml news",
        # "http://channel.chinanews.com/cns/cl/stock-gsxw.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-xywy.shtml news",
        # "http://channel.chinanews.com/cns/cl/fz-xfsd.shtml news",
        # "http://channel.chinanews.com/cns/cl/fz-flfg.shtml news",
        # "http://channel.chinanews.com/cns/cl/mil-gjjqwjdt.shtml news",
        # "http://channel.chinanews.com/cns/cl/cj-cfgcz.shtml news",
        # "http://channel.chinanews.com/cns/cl/gj-hqcz.shtml news",
        # "http://channel.chinanews.com/cns/cl/ty-ltzh.shtml news",
        # "http://channel.chinanews.com/cns/cl/cj-sczx.shtml news",
        # "http://channel.chinanews.com/cns/cl/fz-ldbz.shtml news",
        # "http://channel.chinanews.com/cns/cl/jk-jzzj.shtml news",
        # "http://channel.chinanews.com/cns/cl/ty-zhplc.shtml news",
        # "http://channel.chinanews.com/cns/cl/gj-qqjs.shtml news",
        # "http://channel.chinanews.com/u/hrdd.shtml news",
        # "http://channel.chinanews.com/cns/cl/ga-ms.shtml news",
        # "http://channel.chinanews.com/cns/cl/jk-hyxw.shtml news",
        # "http://channel.chinanews.com/cns/cl/jk-nxbj.shtml news",
        # "http://channel.chinanews.com/u/news/ffcl.shtml news",
        # "http://channel.chinanews.com/cns/cl/ga-kjww.shtml news",
        # "http://channel.chinanews.com/cns/cl/mil-gjjqjsqw.shtml news",
        # "http://channel.chinanews.com/cns/cl/fz-fztc.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-qsqx.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-hwbz.shtml news",
        # "http://channel.chinanews.com/cns/cl/ty-zqkp.shtml news",
        # "http://channel.chinanews.com/cns/cl/gj-oz.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-qzjy.shtml news",
        # "http://channel.chinanews.com/cns/cl/ga-ylmt.shtml news",
        # "http://channel.chinanews.com/u/ty/hytt.shtml news",
        # "http://channel.chinanews.com/cns/cl/ty-klsk.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-hydx.shtml news",
        # "http://channel.chinanews.com/cns/cl/gj-xxsh.shtml news",
        # "http://channel.chinanews.com/u/news/gnmtjc.shtml news",
        # "http://channel.chinanews.com/cns/cl/mil-shyymjfc.shtml news",
        # "http://channel.chinanews.com/cns/cl/ga-fzsj.shtml news",
        # "http://channel.chinanews.com/cns/cl/fz-jdrw.shtml news",
        # "http://channel.chinanews.com/cns/cl/cj-gjcj.shtml news",
        # "http://channel.chinanews.com/cns/cl/fz-hyjt.shtml news",
        # "http://channel.chinanews.com/cns/cl/jk-zcdt.shtml news",
        # "http://channel.chinanews.com/u/news/rsrm.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-hsfc.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-hrjy.shtml news",
        # "http://channel.chinanews.com/cns/cl/jk-jkpl.shtml news",
        # "http://channel.chinanews.com/cns/cl/jk-my.shtml news",
        # "http://channel.chinanews.com/cns/cl/ga-stwx.shtml news",
        # "http://channel.chinanews.com/cns/cl/fortune-lccp.shtml news",
        # "http://channel.chinanews.com/cns/cl/gj-zwgc.shtml news",
        # "http://channel.chinanews.com/cns/cl/ga-gaynd.shtml news",
        # "http://channel.chinanews.com/cns/cl/ty-zhqt.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-yytx.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-yyxq.shtml news",
        # "http://channel.chinanews.com/cns/cl/jk-yhzj.shtml news",
        # "http://channel.chinanews.com/cns/cl/mil-gjjqlbsm.shtml news",
        # "http://channel.chinanews.com/cns/cl/mil-zgjqxwfbh.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-hrry.shtml news",
        # "http://channel.chinanews.com/cns/cl/cj-alfx.shtml news",
        # "http://channel.chinanews.com/cns/cl/ga-sszqf.shtml news",
        # "http://channel.chinanews.com/cns/cl/ga-xxbp.shtml news",
        # "http://channel.chinanews.com/cns/cl/mil-zgjqgfgj.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-st-mz.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-hljt.shtml news",
        # "http://channel.chinanews.com/cns/cl/gj-cfjm.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-hrzxz.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-hwsh.shtml news",
        # "http://channel.chinanews.com/u/ty/zgxg.shtml news",
        # "http://channel.chinanews.com/cns/cl/mil-shyysjxy.shtml news",
        # "http://channel.chinanews.com/cns/cl/fz-sfgg.shtml news",
        # "http://channel.chinanews.com/cns/cl/jk-lxxt.shtml news",
        # "http://channel.chinanews.com/cns/cl/ty-nba.shtml news",
        # "http://channel.chinanews.com/cns/cl/mil-gjjqdqct.shtml news",
        # "http://channel.chinanews.com/cns/cl/ga-wsry.shtml news",
        # "http://channel.chinanews.com/cns/cl/cj-hgds.shtml news",
        # "http://channel.chinanews.com/cns/cl/ga-cjxw.shtml news",
        # "http://channel.chinanews.com/cns/cl/ty-lyyw.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-qzzc.shtml news",
        # "http://channel.chinanews.com/cns/cl/jk-bgjgl.shtml news",
        # "http://channel.chinanews.com/cns/cl/fz-tszj.shtml news",
        # "http://channel.chinanews.com/cns/cl/ty-pq.shtml news",
        # "http://channel.chinanews.com/cns/cl/gj-dqsj.shtml news",
        # "http://channel.chinanews.com/cns/cl/jk-jsjf.shtml news",
        # "http://channel.chinanews.com/cns/cl/jk-ysyy.shtml news",
        # "http://channel.chinanews.com/cns/cl/cj-chjxw.shtml news",
        # "http://channel.chinanews.com/cns/cl/ga-gamy.shtml news",
        # "http://channel.chinanews.com/cns/cl/cj-ctcf.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-trj.shtml news",
        # "http://channel.chinanews.com/cns/cl/jk-jtyx.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-hrshq.shtml news",
        # "http://channel.chinanews.com/cns/cl/gj-gjrw.shtml news",
        # "http://channel.chinanews.com/cns/cl/mil-jssp.shtml news",
        # "http://www.chinanews.com/life.shtml news",
        # "http://channel.chinanews.com/cns/cl/cj-fyrw.shtml news",
        # "http://channel.chinanews.com/cns/cl/mil-zgjqjgkj.shtml news",
        # "http://channel.chinanews.com/cns/cl/fortune-jg.shtml news",
        # "http://channel.chinanews.com/cns/cl/ty-gnzq.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-hrdt.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-rdgz.shtml news",
        # "http://channel.chinanews.com/cns/cl/mil-shyyzgzs.shtml news",
        # "http://channel.chinanews.com/cns/cl/fz-lfjc.shtml news",
        # "http://channel.chinanews.com/cns/cl/gj-wmck.shtml news",
        # "http://channel.chinanews.com/cns/cl/fz-qybh.shtml news",
        # "http://channel.chinanews.com/cns/cl/gj-yt.shtml news",
        # "http://channel.chinanews.com/cns/cl/fz-pajq.shtml news",
        # "http://channel.chinanews.com/cns/cl/jk-xpxz.shtml news",
        # "http://channel.chinanews.com/cns/cl/jk-gmsy.shtml news",
        # "http://channel.chinanews.com/cns/cl/ga-gw.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-lsbh.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-hszx.shtml news",
        # "http://channel.chinanews.com/cns/cl/fz-yfxz.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-hrwy.shtml news",
        "http://channel.chinanews.com/cns/cl/jk-shts.shtml news",
        # "http://channel.chinanews.com/cns/cl/ty-hjlw.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-zckd.shtml news",
        # "http://channel.chinanews.com/u/finance/gs.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-ymfb.shtml news",
        # "http://channel.chinanews.com/cns/cl/gj-bm.shtml news",
        # "http://channel.chinanews.com/cns/cl/fz-jjjf.shtml news",
        # "http://channel.chinanews.com/cns/cl/ty-gjzq.shtml news",
        # "http://channel.chinanews.com/cns/cl/jk-xljk.shtml news",
        # "http://channel.chinanews.com/cns/cl/fortune-jgdtyh.shtml news",
        # "http://channel.chinanews.com/cns/cl/gj-zd.shtml news",
        # "http://channel.chinanews.com/cns/cl/fz-xjlh.shtml news",
        # "http://channel.chinanews.com/cns/cl/mil-gjjqysjs.shtml news",
        # "http://channel.chinanews.com/cns/cl/ga-sh.shtml news",
        # "http://channel.chinanews.com/cns/cl/fz-ffcl.shtml news",
        # "http://channel.chinanews.com/cns/cl/jk-jbcs.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-hrgs.shtml news",
        # "http://channel.chinanews.com/cns/cl/hr-hwqz.shtml news",
        # "http://channel.chinanews.com/cns/cl/gj-sswh.shtml news",
        # "http://channel.chinanews.com/cns/cl/fortune-hlwjr.shtml news",
        # "http://channel.chinanews.com/u/cl/mil-zgjq.shtml news",
        # "http://www.gd.chinanews.com/index/gfgl.html news",
        # "http://www.gd.chinanews.com/index/nysz.html news",
        # "http://www.gd.chinanews.com/index/zxdc.html news",
        # "http://www.gd.chinanews.com/index/ztgot.html news",
        # "http://www.gd.chinanews.com/index/dfpd.html news",
        # "http://www.gd.chinanews.com/index/qxlf.html news",
        # "http://www.gd.chinanews.com/index/shyx.html news",
        # "http://www.gd.chinanews.com/index/rwgd.html news",
        # "http://www.gd.chinanews.com/index/lnrw.html news",
        # "http://www.gd.chinanews.com/index/gg.html news",
        # "http://www.gs.chinanews.com/gssj/index.shtml news",
        # "http://www.gd.chinanews.com/index/lnwh.html news",
        # "http://www.chinanews.com/economic.shtml news",
        # "http://stock.chinanews.com/#iframe-ggxcb news",
        # "http://stock.chinanews.com/#qsmdm news",
        # "http://stock.chinanews.com/#bjjt news",
        # "http://www.hb.chinanews.com/zixun.html news",
        # "http://www.shx.chinanews.com/szjj.html news",
        # "http://www.shx.chinanews.com/zltx.html news",
        # "http://www.gd.chinanews.com/index/whjy.html news",
        # "http://www.gd.chinanews.com/index/zxzxg.html news",
        # "http://www.gd.chinanews.com/index/hd.html news",
        # "http://www.gd.chinanews.com/index/gdsz.html news",
        # "http://www.gd.chinanews.com/index/kjyn.html news",
        # "http://www.gd.chinanews.com/index/gdfs.html news",
        # "http://www.gd.chinanews.com/index/shjk.html news",
        # "http://www.gd.chinanews.com/index/ls.html news",
        # "http://www.gd.chinanews.com/index/cxgd.html news",
        # "http://www.gd.chinanews.com/index/dqsj.html news",
        # "http://www.gd.chinanews.com/index/nsq.html news",
        # "http://www.gd.chinanews.com/index/kjgd.html news",
        # "http://www.gd.chinanews.com/index/hlwjr.html news",
        # "http://www.gd.chinanews.com/index/qcsh.html news",
        # "http://www.gd.chinanews.com/index/gdjj.html news",
        # "http://www.gd.chinanews.com/index/cstt.html news",
        # "http://www.gd.chinanews.com/index/gz.html news",
        # "http://www.gd.chinanews.com/index/gddt.html news",
        # "http://www.gd.chinanews.com/index/yjcj.html news",
        # "http://www.chinanews.com/society.shtml news",
        # "http://www.ln.chinanews.com/tiyu/index.shtml news",
        # "http://www.ln.chinanews.com/yule/index.shtml news",
        # "http://www.ln.chinanews.com/zxjzbln/index.shtml news",
        # "http://www.ln.chinanews.com/wenhua/index.shtml news",
        # "http://www.ln.chinanews.com/liaoning/index.shtml news",
        # "http://www.ln.chinanews.com/shenghuo/index.shtml news",
        # "http://www.ln.chinanews.com/shangye/index.shtml news",
        # "http://www.ln.chinanews.com/shishang/index.shtml news",
        # "http://www.ln.chinanews.com/keji/index.shtml news",
        # "http://www.ln.chinanews.com/jiankang/index.shtml news",
        # "http://www.ln.chinanews.com/caijing/index.shtml news",
        # "http://www.ln.chinanews.com/shehui/index.shtml news",
        # "http://www.ln.chinanews.com/guoji/index.shtml news",
        # "http://www.ln.chinanews.com/nongye/index.shtml news",
        # "http://www.ln.chinanews.com/guonei/index.shtml news",
        # "http://www.ln.chinanews.com/hwmtkln/index.shtml news",
        # "http://www.ln.chinanews.com/lvyou/index.shtml news",
        # "http://www.ln.chinanews.com/fangchan/index.shtml news",
        # "http://www.ln.chinanews.com/jiaoyu/index.shtml news",
        "http://www.heb.chinanews.com/4/20111018/327.shtml news",
        # "http://www.fj.chinanews.com/new/fjxw/list.shtml news",
        "http://www.fj.chinanews.com/new2015/jryw/list.html news",
        # "http://www.ha.chinanews.com/news/ news",
        # "http://www.hb.chinanews.com/gnxw.html news",
        # "http://www.hb.chinanews.com/xnc.html news",
        # "http://www.shx.chinanews.com/jzyx.html news",
        # "http://www.shx.chinanews.com/sqjz.html news",
        # "http://www.shx.chinanews.com/shmj.html news",
        # "http://www.shx.chinanews.com/ztbd.html news",
        # "http://www.shx.chinanews.com/mtsp.html news",
        "http://www.shx.chinanews.com/sssh.html news",
        # "http://www.shx.chinanews.com/zxsp.html news",
        # "http://www.hn.chinanews.com/hnjjdy/gzyj/index1.html news",
        # "http://www.hn.chinanews.com/hnjjdy/qyjw/index1.html news",
        # "http://www.hn.chinanews.com/hnjjdy/ldlt/index1.html news",
        # "http://www.hn.chinanews.com/hnjjdy/fzfl/index1.html news",
        # "http://www.hn.chinanews.com/news/jzyx/ news",
        # "http://www.hn.chinanews.com/news/lyxw/index.shtml news",
        # "http://www.hn.chinanews.com/news/cnsdc/index.shtml news",
        # "http://www.hn.chinanews.com/news/gatq/index.shtml news",
        # "http://www.hn.chinanews.com/news/shsh/ news",
        # "http://www.hn.chinanews.com/news/cjxx/ news",
        # "http://www.hn.chinanews.com/news/gnxw/ news",
        # "http://www.hn.chinanews.com/news/szws/ news",
        # "http://www.hn.chinanews.com/news/fcxw/ news",
        # "http://www.hn.chinanews.com/news/hnyw/index.shtml news",
        "http://www.hn.chinanews.com/news/gngj/ news",
        "http://www.hn.chinanews.com/news/sxdt/ news",
        # "http://www.hn.chinanews.com/news/tyxw/index.shtml news",
        # "http://www.hn.chinanews.com/news/kjww/ news",
        # "http://www.hn.chinanews.com/news/ylty/ news",
        "http://www.heb.chinanews.com/4/20111018/321.shtml news",
        # "http://www.chinanews.com/importnews.html news",
        # "http://www.sh.chinanews.com/swzx/index.shtml news",
        # "http://www.sh.chinanews.com/gatq/index.shtml news",
        # "http://www.sh.chinanews.com/ztbd/index.shtml news",
        # "http://www.sh.chinanews.com/szyw/index.shtml news",
        # "http://www.sh.chinanews.com/whty/index.shtml news",
        # "http://www.sh.chinanews.com/ckzx/ckzx-cyxx/index.shtml news",
        # "http://www.sh.chinanews.com/qxdt/index.shtml news",
        # "http://www.sh.chinanews.com/kjws/index.shtml news",
        # "http://www.sh.chinanews.com/ckzx/ckzx-hqck/index.shtml news",
        # "http://www.sh.chinanews.com/cjxw/index.shtml news",
        # "http://www.sh.chinanews.com/ckzx/ckzx-ckkj/index.shtml news",
        # "http://www.sh.chinanews.com/shms/index.shtml news",
        # "http://www.sh.chinanews.com/ckzx/ckzx-kcsd/index.shtml news",
        "http://www.sh.chinanews.com/spxw/index.shtml news",
        # "http://www.sh.chinanews.com/shxw/index.shtml news",
        "http://www.zj.chinanews.com/sh/jkcy/index.html news",
        # "http://www.zj.chinanews.com/qt/yss/index.html news",
        # "http://www.zj.chinanews.com/qt/kqt/index.html news",
        # "http://www.zj.chinanews.com/qt/hzzx/index.html news",
        # "http://www.zj.chinanews.com/sh/ztc/index.html news",
        # "http://www.zj.chinanews.com/jy/cy/index.html news",
        # "http://www.zj.chinanews.com/jy/kjs/index.html news",
        # "http://www.zj.chinanews.com/qt/ltpl/index.html news",
        # "http://www.zj.chinanews.com/jy/ky/index.html news",
        # "http://www.zj.chinanews.com/cj/gd/index.html news",
        # "http://www.zj.chinanews.com/wy/mx/index.html news",
        # "http://www.zj.chinanews.com/jy/gx/index.html news",
        # "http://www.zj.chinanews.com/jy/gk/index.html news",
        # "http://www.zj.chinanews.com/jy/zczj/index.html news",
        # "http://www.zj.chinanews.com/wy/ys/index.html news",
        # "http://www.zj.chinanews.com/jy/lx/index.html news",
        # "http://www.zj.chinanews.com/jy/sfks/index.html news",
        # "http://www.zj.chinanews.com/wy/tj/index.html news",
        # "http://www.sh.chinanews.com/tpxw/index.shtml news",
        # "http://www.sd.chinanews.com/more/news/4.html news",
        # "http://www.sd.chinanews.com/more/news/7.html news",
        # "http://www.sd.chinanews.com/more/news/10.html news",
        # "http://www.sd.chinanews.com/more/news/11.html news",
        # "http://www.sd.chinanews.com/more/news/1.html news",
        # "http://www.sd.chinanews.com/more/news/26.html news",
        # "http://www.sd.chinanews.com/more/news/6.html news",
        # "http://www.sd.chinanews.com/more/news/9.html news",
        # "http://www.sd.chinanews.com/more/news/5.html news",
        "http://www.sd.chinanews.com/more/news/12.html news",
        "http://www.bt.chinanews.com/kejiao/index.shtml news",
        "http://www.sx.chinanews.com/4/2009/0110/2.html news",
        "http://www.bj.chinanews.com/4/2009/0306/1.html news",
        "http://www.shx.chinanews.com/news/jjxw.shtml news",
        # "http://www.js.chinanews.com/highlights/ news",
        # "http://www.hb.chinanews.com/wbhb.html news",
        # "http://www.hb.chinanews.com/jzyx.html news",
        # "http://www.hb.chinanews.com/shxw.html news",
        "http://www.hb.chinanews.com/hbxw.html news",
        # "http://www.hb.chinanews.com/dsxw.html news",
        # "http://www.hb.chinanews.com/gjxw.html news",
        # "http://www.hb.chinanews.com/pinglun.html news",
        "http://www.heb.chinanews.com/4/20111018/326.shtml news",
        # "http://www.heb.chinanews.com/4/20111018/329.shtml news",
        # "http://www.chinanews.com/huaren.shtml news",
        # "http://www.gd.chinanews.com/gnxw.html news",
        # "http://www.chinanews.com/it.shtml news",
        "http://www.js.chinanews.com/photo/ news",
        # "http://www.chinanews.com/photo/shmy.html news",
        # "http://www.chinanews.com/photo/gatq.html news",
        # "http://www.chinanews.com/photo/more/1.html news",
        # "http://www.chinanews.com/photo/gjbl.html news",
        # "http://www.chinanews.com/photo/jskj.html news",
        "http://www.fj.chinanews.com/new2014/xmxw/list.shtml news",

    ]
    Debug = True
    doredis = True
    source = u"中国新闻网"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"DOWNLOAD_TIMEOUT": 120.0, "DOWNLOAD_DELAY": 0.25, "ROBOTSTXT_OBEY": False}
    sta = {"eff": 0, "inv": 0, "warn": 0, "all": 0, "inv2": 0, "no_title": 0, "no_time": 0, "no_medianame": 0}

    def print_info(self, info, flag="success", count=True):
        if flag == "error":
            color = "31"
            self.sta["inv"] += [0, 1][count]
        elif flag == "error2":
            color = "35"
            self.sta["inv2"] += [0, 1][count]
        elif flag == "warn":
            color = "33"
            self.sta["warn"] += [0, 1][count]
        else:
            self.sta["eff"] += [0, 1][count]
            color = "32"
        print('\033[0;'+color+';0m')
        print('*' * 100)
        if color == "31":
            print "抛出异常: ", info
            self.log.write(info+'\n')
        elif color == "33":
            print "警告： ", info
            self.log.write(info+'\n')
        else:
            print "信息: ", info
        print "统计: ",
        print "有效:", self.sta["eff"], " 无效: ", self.sta["inv"], " 警告: ", self.sta["warn"]," 人为失效:", self.sta["inv2"], \
            " 乐观总计:", self.sta["all"], " 去重后数量:", len(set(self.test_list)) ," 采集率:", "%.2f%%" % (float(self.sta["eff"])/float(len(set(self.test_list)) - self.sta["warn"]-self.sta["inv"])*100), \
            " 无发布源:", self.sta['no_medianame'], " 无时间:", self.sta['no_time'], " 无标题:", self.sta['no_title']
        print('*' * 100)
        print('\033[0m')

    def __init__(self, start_url=None):
        super(chinanews, self).__init__()
        # jobs = self.start_urls.split('|')
        self.test_list = list()
        self.log = codecs.open('URL_ERROR.log', 'a', encoding='utf-8')
        jobs = self.start_urls
        for job in jobs:
            self.post_params.append({"url": job.split()[0], "ba_type": job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)

    def __del__(self):
        self.log.close()

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

    def start_requests(self):
        for channel in self.post_params:
            yield Request(url=channel["url"], method='get', meta={"ba_type": channel["ba_type"]}, callback=self.parse_link)

    def get_parse_link_urls(self, response, url):   # 有改良方案，再说吧
        # 进入列表页　然后抽取列表页的详情页
        urls_list = [
            # url　xpath规则　待加入
            '//div[@class="content_list"]/ul/li/div[@class="dd_bt"]/a/@href',  # 时政滚动
            '//div[@class="content_list"]/ul/li/div/a/@href',  # 时政滚动
            '//div[contains(@class, "con2")]//a/@href',  # 时政半通用
            '//ul[contains(@class,"LB_list")]/li/h2/a/@href',  # 一带一路
            '//div[@class="sec_left_1"]/ul/li/a/@href',  # 广东
            '//div[@id="newsArea"]/ul/li/a/@href', # 云南旅游
            '//ul[contains(@class, "newsList")]//a/@href',  # 山西国际
            '//div[@class="libox"]/a/@href',  # 图文专稿
            '//li/div[@class="dd_bt"]/a/@href',  # 广东资讯
            '//div[@class="list"]/ul/li/a/@href',  # 时尚
            '//div[@class="list_li"]/a/@href',  # 福建导读
            '//div[@class="map_left"]/ul/li/a/@href',  # 云南 网友之声
            '//ul[@class="NLPul"]//span/a/@href',  # 趣味视频
            '//div[@id="frameContent1"]/div/div/a[contains(@class, "link")]/@href',  # 陕西频道
            '//table[@class="v12"]/following-sibling::table//tr//td/a/@href',  # 北京分频
            '//div[@class="content_list"]/ul/li//div/a/@href',  # CNSTV
            '//ul[@id="ul_news"]/li/div/a/@href',  # 福建新闻网
            '//div[@class="list_con"]/ul/li/div/a/@href',  # 福建新闻网
            '//ul[@class="news_list_ul"]/li/div/a/@href',  # 视频频道
            '//ul[contains(@class, "contentlist")][position()<51]/li/span/a/@href',
            '//ul[contains(@class, "contentlist")]/li[position()<101]/span/a/@href',  # 娱乐新闻
            '//ul[@class="list_16"]/li/a/@href',
            '//div[@class="pmbox1"]/a/@href',  # 热辣图库
            '//ul[contains(@class, "branch_list_ul")]/li/a/@href',  # 中新社北京分社
            '//div[@class="listbox"]/ul//li/a/@href',  # 甘肃要闻
            '//div[@class="left_zw"]/div/table//ul/li/a/@href',  # 河北新闻
            '//a[@class="title2"]/@href',  # 纵览天下
            '//ul[@id="JrhnNews"]/li/a/@href',  # 湖南新闻报
            '//div[@class="videoList"]/dl/dd/a/@href',  # 视频新闻
            '//div[@id="list"]/ul/li/a/@href',  # 江苏频道
            '//div[@class="list"]/div[@class="pic"]/a/@href',  # 江苏图片频道
            '//ul[@class="paging"]/li/a/@href',  # 成都频道
            '//div[@class="container"]/div[contains(@class, "img")]/div/a/@href',  # 中新图片频道
            '//div[@class="picdiv"]/div/a/@href',  # 图解新闻
            '//div[@id="news_list"]/ul/li[position()<50]/a/@href', # 演出频道 热门资讯
            '//ul[@id="DataList"]/li/a/@href',  # 重庆频道 每次重庆的频道都是单独一种 真有牌面
            '//ul[@id="listContainer"]/li/h2/a/@href',  # 福建频道
            '//ul[@id="ul_news"]/li/a/@href',  # 贵州频道
            '//span[@class="rt"]/following-sibling::a/@href',  # 广西频道
            '//ul[contains(@class, "contentlist")]/li[position()<101]//a/@href',  # 海南新闻
            '//ul[contains(@class, "contentlist")]/div[position()<101]//a/@href',  # 海南图片新闻
            '//ul[@id="tablelsw"]/li//a/@href',  # 海南养生频道  这个图片翻页又是新的一种
            '//div[contains(@class, "liebiao")]/ul/li/a/@href',  # 河南频道
            '//div[@id="content_list"]/p//a/@href',  # 湖北
            '//li[@class="Timg2"]/span[1]/a/@href',  # 湖北图片
            '//div[@class="news_list_box"]//a/@href',  # 黑龙江频道
            '//div[@id="sy_list_left"]//ul/li[position()<21]/a/@href',  # 内蒙古频道
            '//ul[@class="branch_list_ul paging"]/li[position()<41]/div[2]/a/@href',  # 上海频道
            '//div[@id="showtypeli"]/ul//tr/td/a/@href',  # 经济纵横
            '//div[@class="wz"]/ul[@class="e2"]//a/@href',  # 甘肃新闻
            '//div[@class="content-bt"]/a[1]/@href',  # 推荐阅读
            '//td[@id="TT"]/li[position()<51]/a/@href',  # 国内新闻
            '//div[@class="contents"]/ul/li/a/@href',  # 山西国内要闻
        ]
        for url_xpath in urls_list:
            if len(response.xpath(url_xpath).extract()) > 0:
                print url, " 本次套用:", url_xpath," 条目数:", len(response.xpath(url_xpath).extract())
                return url_xpath
        print response.url, " 没有适当规则"
        content = response.url + '  这个频道需要url规则!\n'
        self.log.write(content)

    def parse_link(self, response):
        try:
            if 'currentpage=0&' in response.url:
                # ajax接口处理
                urls = re.findall(r"url':\s?'(http:.+?.shtml)", response.body)
                # xpath = "None"
            else:
                xpath = self.get_parse_link_urls(response, response.url)
                urls = response.xpath(xpath).extract()
                self.sta["all"] += len(urls)
            for index, url in enumerate(urls):
                if '../' in url:
                    url = url.replace('../', '')
                final = urlparse.urljoin(response.url, url.strip())
                # 海南频道的2012和2013年的新闻会乱入 一：太旧了 二：会有无法解释的bug发生
                if 'chinanews' in final and ('2012-' not in final and '2013-' not in final and '/2012/' not in final):
                    self.test_list.append(final)
                    # if self.doredis and self.expire_redis.exists(final):
                    #    continue
                    yield Request(url=final, method='get',
                                  meta={"ba_type": response.meta["ba_type"], "parse_for_content": True},
                                  callback=self.parse_item, errback=self.parse_err_detail)
        except Exception,e:
            content = response.url + e.message
            self.log.write(content)

    def parse_err_detail(self, failure):
        response = failure.value.response
        self.print_info("页面异常: " + response.url + "  状态：" + str(response.status), "error")

    def parse_item(self, response):
        try:
            if response.meta["parse_for_content"]:
                item = DataItem()

                # 标题
                title1 = response.xpath('//div[@id="xw_title"]/h2') or \
                         response.xpath('//div[@id="newsTitle"]') or \
                         response.xpath('//div[@id="biaoti"]') or \
                         response.xpath('//div[@class="thi_left_1"]/h2') or \
                         response.xpath('//div[@class="blkContainerSblk"]/h1') or \
                         response.xpath('//div[@class="content-title"]') or \
                         response.xpath('//div[@class="con-titl"]') or \
                         response.xpath('//div[@class="con_titl"]') or \
                         response.xpath('//div[@class="newbiaoti"]/strong') or \
                         response.xpath('//td[@id="content"]//strong') or \
                         response.xpath('//div[@id="mian"]/div/i') or \
                         response.xpath('//div[@class="window1"]/div[@class="h6"]') or \
                         response.xpath('//div[contains(@class, "biaoti")]') or \
                         response.xpath('//td[@id="content"]/table[1]/tbody[1]/tr[1]/td[1]') or \
                         response.xpath('//div[@class="neir_bt"]') or \
                         response.xpath('//div[@class="title"]/h1') or \
                         response.xpath('//div[@class="title"]') or \
                         response.xpath('//div[@class="c_title"]') or \
                         response.xpath('//div[@id="title"]') or \
                         response.xpath('//div[@class="pagetitle"]') or \
                         response.xpath('//dt[@class="wryh"]') or \
                         response.xpath('//span[@id="txtTitle"]') or \
                         response.xpath('//div[@class="neiron_title"]') or \
                         response.xpath('//div[@class="news_title"]') or \
                         response.xpath('//td[contains(@class, "black_titnews")]') or \
                         response.xpath('//h1[@id="tit"]') or \
                         response.xpath('//h1') or \
                         response.xpath('//div[@class="left_five1"]') or \
                         response.xpath('//div[@class="cms-news-article-title"]/span') or \
                         response.xpath('//div[@class="neiyect"]/h3') or \
                         response.xpath('//div[@class="incont_t"]/h2') or \
                         response.xpath('//div[@class="atitle"]/div[@class="f_l"]') or \
                         response.xpath('//div[@class="listbox"]/div[@class="dd"]')
                         # response.xpath('//head/title')  # 云南每日专题  没时间 没来源
                item["title"] = ""
                if len(title1) > 0:
                    item['title'] = title1[0].xpath('string(.)').extract()[0].strip()
                if item["title"] == "":
                    self.print_info(response.url + "  这个详细页无标题！！！", "warn", False)
                    self.sta['no_title'] += 1
                    item["title"] = response.xpath("//title/text()").extract()[0]


                # 发布时间
                # pubtime1 存放 text()等不用再处理的
                pubtime1 = response.xpath('//strong/li/a/div/text()').extract()

                pubtime2 = response.xpath('//div[@class="left-time"]//div[@class="left-t"]') or \
                           response.xpath('//div[@id="xw_xinxi"]/span[1]') or \
                           response.xpath('//div[@class="cms-news-article-title-source"]') or \
                           response.xpath('//p[@class="fabushijian"]') or \
                           response.xpath('//div[@class="neiron_hh"]/li[1]') or \
                           response.xpath('//div[@id="newsInfo"]') or \
                           response.xpath('//div[@id="sendday"]') or \
                           response.xpath('//div[@class="thi_left_1"]/dl/dt') or \
                           response.xpath('//div[@class="artInfo"]/span[@id="pub_date"]') or \
                           response.xpath('//div[@class="con_time"]/ul/li[1]') or \
                           response.xpath('//div[contains(@class, "content-time")]/div[1]') or \
                           response.xpath('//div[@id="anthornew"]') or \
                           response.xpath('//div[@id="anthor"]') or \
                           response.xpath('//div[@class="video_con"]/p/span[1]') or \
                           response.xpath('//div[@class="tit-bar fl"]/span[3]') or \
                           response.xpath('//div[@class="t3"]/following-sibling::div[1]') or \
                           response.xpath('//div[@class="window21"]/div[@class="h5"]') or \
                           response.xpath('//div[@class="biaoti"]/following-sibling::div[@class="suoying"]') or \
                           response.xpath('//div[@class="atime"]') or \
                           response.xpath('//div[@class="p1"]') or \
                           response.xpath('//div[@id="time"]') or \
                           response.xpath('//div[@class="news_info"]/span[1]') or \
                           response.xpath('//div[@class="addtime"]') or \
                           response.xpath('//div[@class="pagetop"]') or \
                           response.xpath('//div[@class="c_info"]/div[@class="f_l"]') or \
                           response.xpath('//dl[@class="headline"]/dd/span[1]') or \
                           response.xpath('//div[@class="left_five2"]') or \
                           response.xpath('//div[@class="neiyectime"]') or \
                           response.xpath('//div[@id="xw_xinxi"]/span[1]') or \
                           response.xpath('//div[contains(@class, "laiyuan")]') or \
                           response.xpath(u'//td[contains(text(), "发布时间")]') or \
                           response.xpath(u'//div[contains(text(), "来源")]') or \
                           response.xpath(u'//span[contains(text(), "时间")]') or \
                           response.xpath(u'//*[contains(text(), "来源")]') or \
                           response.xpath('//h1/following-sibling::span') or \
                           response.xpath('//h1/following-sibling::p') or \
                           response.xpath('//div[@class="zwbei01 div_12px zw_01"]')
                    # response.xpath('//td[@class="jiathis_style"]/ancestor::tr/td[1]') or \
                           # response.xpath('//div[@class="xdd"]/table/tbody/tr/td[1]')

                # print pubtime1,'----',pubtime2
                item['pubtime'] = ''
                if len(pubtime1) > 0:
                    print pubtime1
                    item['pubtime'] = re.search(r'\d{4}.\d{1,2}.\d{1,2}\s+\d{1,2}[:：]\d{1,2}', pubtime1[0]).group(0)
                if len(pubtime2) > 0 and len(pubtime1) == 0:
                    pubtime2 = pubtime2[0].xpath('string(.)').extract()[0].strip().replace("年", "-").replace("月",
                                                                                                             "-").replace(
                        "日", " ")
                    if re.search(r"(\d{4}-\d{1,2}-\d{1,2}.+\d)", pubtime2):
                        # 这里re规则 作了些修改 可能后续有不兼容的情况
                        # 出现了不需要的字段 虽然不影响
                        item["pubtime"] = re.search(r"(2\d{3}-\d{1,2}-\d{1,2}.+\d)", pubtime2).group(0)
                    elif re.search(r"2\d+", pubtime2):
                        # item["pubtime"] = re.search(r"(\d{4}.\d{1,2}.\d{1,2}\s\d{1,2}:\d{1,2})",
                        item["pubtime"] = re.search(r"(2\d+.+\d)",
                                                    pubtime2.replace(".", "-")).group(0)
                    elif 'Last-Modified' in response.headers:
                        item['pubtime'] = datetime.datetime.strptime(response.headers["Last-Modified"],
                                                                     '%a, %d %b %Y %H:%M:%S GMT').strftime(
                            "%Y-%m-%d %H:%M")

                if len(pubtime2) == 0 and len(pubtime1) == 0:
                    self.print_info(response.url + "  这个详细页无发布时间！！！", "warn", False)
                    self.sta['no_time'] += 1
                    pubtime3 = re.findall(r"published.+at.+(\d{4}.+:\d{2})", response.body)
                    # print 'response.headers: ', response.headers
                    if len(pubtime3) > 0:
                        item["pubtime"] = pubtime3[0]

                    elif 'Last-Modified' in response.headers:
                        item['pubtime'] = datetime.datetime.strptime(response.headers["Last-Modified"],
                                                                     '%a, %d %b %Y %H:%M:%S GMT').strftime(
                            "%Y-%m-%d %H:%M")
                    elif 'Date' in response.headers:
                        item['pubtime'] = datetime.datetime.strptime(response.headers["Date"], '%a, %d %b %Y %H:%M:%S GMT').strftime("%Y-%m-%d %H:%M")
                item['pubtime'] = item['pubtime'].replace("  "," ")
                middle_pubtime = re.search(r'2\d{3}.\d{1,2}.\d{1,2}\s?\d{1,2}.\d{1,2}', item['pubtime'])
                middle_pubtime1 = re.search(r'2\d{3}.\d{1,2}.\d{1,2}\s?', item['pubtime'])
                if middle_pubtime:
                    item['pubtime'] = middle_pubtime.group()
                elif middle_pubtime1:
                    item['pubtime'] = middle_pubtime1.group()
                elif 'Last-Modified' in response.headers:
                    item['pubtime'] = datetime.datetime.strptime(response.headers["Last-Modified"],
                                                                 '%a, %d %b %Y %H:%M:%S GMT').strftime(
                                                                                                "%Y-%m-%d %H:%M")

                # 来源
                item['medianame'] = ""

                # medianame1 是存放需要string()处理的xpath规则
                medianame1 = response.xpath('//div[@class="left-time"]//div[@class="left-t"]') or \
                             response.xpath(u'//div[@class="suoying"][contains(text(), "来源")]') or \
                             response.xpath('//div[@class="suoying"]') or \
                             response.xpath('//div[@class="cms-news-article-title-source"]') or \
                             response.xpath('//div[@id="xw_xinxi"]/span[2]') or \
                             response.xpath('//div[@id="newsInfo"]/a') or \
                             response.xpath('//p[@class="fabulaiyuan"]') or \
                             response.xpath('//div[@id="newsInfo"]') or \
                             response.xpath('//div[@class="biaoti"]/following-sibling::div[@class="suoying"]') or \
                             response.xpath('//div[@class="biaoti"]/following-sibling::div[@class="suoying"]/a') or \
                             response.xpath('//div[@class="thi_left_1"]/dl/dt') or \
                             response.xpath('//div[@class="artInfo"]/span[@id="media_name"]') or \
                             response.xpath('//div[@class="con_time"]/ul/li[2]') or \
                             response.xpath('//div[contains(@class, "content-time")]/div[2]') or \
                             response.xpath(u'//div[@id="anthor"][contains(text(), "来源")]') or \
                             response.xpath('//div[@class="video_con"]/p/span[2]') or \
                             response.xpath('//div[@class="tit-bar fl"]/span[1]') or \
                             response.xpath('//div[@class="window23"]/div[@class="h5"]/a') or \
                             response.xpath('//div[@class="atime"]') or \
                             response.xpath('//div[@class="news_info"]/strong[1]') or \
                             response.xpath('//div[@class="p1"]') or \
                             response.xpath('//div[@id="come"]') or \
                             response.xpath('//div[@class="c_info"]/div[@class="f_l"]') or \
                             response.xpath('//div[@class="nrfbtime"]/span/i') or \
                             response.xpath('//div[@class="other"]/div[@class="l"]') or \
                             response.xpath('//div[@class="pagetop"]') or \
                             response.xpath('//dl[@class="headline"]/dd/span[2]/a') or \
                             response.xpath('//div[contains(@class, "laiyuan")]') or \
                             response.xpath('//div[@class="left_five2"]') or \
                             response.xpath('//div[@class="neiyecontent"]/following-sibling::em') or \
                             response.xpath('//div[@class="neiron_hh"]/li[2]') or \
                             response.xpath('//div[@class="window23"]/div[@class="h5"]') or \
                             response.xpath(u'//td/div[contains(text(), "来源")]') or \
                             response.xpath('//div[@align]/ancestor::div[@class="none"]') or \
                             response.xpath(u'//span[contains(text(), "来源")]') or \
                             response.xpath(u'//p[contains(text(), "来源")][position()=last()]') or \
                             response.xpath(u'//em[contains(text(), "来源")]') or \
                             response.xpath('//h1/following-sibling::span') or \
                             response.xpath('//h1/following-sibling::p') or \
                             response.xpath(u'//td[contains(text(), "发布时间")]')
                            # response.xpath(u'//div[contains(text(), "来源")]') or \
                            # response.xpath('//td[@class="jiathis_style"]/ancestor::tr/td[1]') or \
                             # response.xpath('//div[@class="xdd"]/table/tbody/tr/td[1]')
                # medianame2 存放的是最终的xpath规则
                medianame2 = response.xpath('//div[@id="xw_xinxi"]/span[2]/text()').extract()

                medianame3 = response.xpath('//div[@id="anthornew"]')
                if len(medianame1) > 0:
                    medianame1 = medianame1.xpath('string(.)').extract()[0].strip()
                    if len(re.findall(ur"(来源|出处|来自|稿源|出自|来源于)", medianame1)) > 0:
                        # 这里会有一个坑 来源： 后面没了 有些网站没有来源还把来源：3个字写上去  来源: 中新网 编辑|作者：xxx 还有这种格式
                        if not re.search(u'来源[：:]\s*$', medianame1):
                            item['medianame'] = re.search(ur'.*?(来源|出处|来自|稿源|出自|来源于)\s*[：:]\s*(\S*)\s?', medianame1).group(2).strip()
                    else:
                        item["medianame"] = medianame1.strip()

                if len(medianame2) > 0 and len(medianame1) == 0:
                    item["medianame"] = medianame2[0].strip()

                if len(medianame3) > 0 and len(medianame2) == 0 and len(medianame1) == 0:
                    medianame3 = medianame3.xpath('string(.)').extract()[0]
                    item['medianame'] = medianame3.split()[0]

                # print 'medianame: ', item['medianame'].split()
                if len(item['medianame'].split()) > 1:
                    item['medianame'] = item['medianame'].split()[0]
                # 查询是否有其他字段乱入
                if re.search(r'\s', item['medianame']):
                    item['medianame'] = item['medianame'].split()[0]

                if u'参与互动' in item['medianame']:
                    item['medianame'] = re.search(ur'(.+)参与互动.+', item['medianame']).group(1)

                if u'编辑' in item['medianame']:
                    item['medianame'] = u'中国新闻网'

                if u'作者' in item['medianame']:
                    item['medianame'] = u'中国新闻网'

                if u"年" in item["medianame"] and u"月" in item["medianame"]:
                    self.print_info(item['title'] + " " + response.url + "  这个来源包括了时间，检查！！！", "warn", False)
                    item["medianame"] = u"中国新闻网"

                if item["medianame"] == "":
                    # self.print_info(item['title'] + " " + response.url + "  这个详细页无来源！！！", "warn", False)
                    self.print_info(item['title'] + " " + response.url + "  这个详细页无来源！！！", "warn", False)
                    self.sta['no_medianame'] += 1
                    item["medianame"] = u"中国新闻网"
                # print item["medianame"]


                # 种类/地区/源/收集时间/url
                item["type"] = response.meta["ba_type"]
                if "//gj" in response.url:
                    item['area'] = u'国际'
                else:
                    item['area'] = u'全国'
                item['source'] = self.source
                item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
                item['url'] = response.url

                # 内容
                content = response.xpath('//div[@id="MyContent"]').extract() or \
                          response.xpath('//div[contains(@class, "content-time")]/following-sibling::div[not(@class)]').extract() or \
                          response.xpath('//div[@class="left_zw"]').extract() or \
                          response.xpath('//div[@id="newsText"]').extract()or \
                          response.xpath('//td[@id="TT"]').extract()or \
                          response.xpath('//div[@id="artibody"]').extract() or \
                          response.xpath('//div[@id="xw_content"]').extract() or \
                          response.xpath('//div[@id="zoom"]').extract() or \
                          response.xpath('//div[@id="txt"]').extract() or \
                          response.xpath('//div[@class="txt"]').extract() or \
                          response.xpath('//div[@class="con_con"]').extract() or \
                          response.xpath('//div[@class="art-con"]').extract() or \
                          response.xpath('//div[@class="content_desc"]').extract() or \
                          response.xpath('//div[@id="d1d"]').extract() or \
                          response.xpath('//div[@id="cont_show"]').extract() or \
                          response.xpath('//div[@id="window"]/ancestor::div[@id="container"]').extract() or \
                          response.xpath('//div[@class=" branch_con_text"]').extract() or \
                          response.xpath('//div[@class="zhenwen"]/..').extract() or \
                          response.xpath('//div[@class="article-content"]').extract() or \
                          response.xpath('//div[@class="neiron_kong"]').extract() or \
                          response.xpath('//div[@class="content"]').extract() or \
                          response.xpath('//div[@class="main"]').extract() or \
                          response.xpath('//div[@class="wz"]').extract() or \
                          response.xpath('//td[@id="content"]').extract() or \
                          response.xpath('//div[@class="nrfbtime"]/span/i').extract() or \
                          response.xpath('//div[@class="picnr_con"]').extract() or \
                          response.xpath('//div[@class="pagecon"]').extract() or \
                          response.xpath('//div[@id="content"]').extract() or \
                          response.xpath('//div[@id="ArticleCnt"]').extract() or \
                          response.xpath('//div[@id="eFramePic"]').extract() or \
                          response.xpath('//div[@id="ArticleBody"]').extract() or \
                          response.xpath('//div[contains(@class,"tp_bdiv dh-")]').extract() or \
                          response.xpath('//div[contains(@class, "bigdiv4")]').extract() or \
                          response.xpath('//div[@id="content_text"]').extract() or \
                          response.xpath('//td[contains(@class, "black_titnews")]/ancestor::tr/following-sibling::tr[last()]').extract() or \
                          response.xpath('//div[@class="left_five3"]').extract() or \
                          response.xpath('//div[@class="cms-news-article-content-block"]').extract() or \
                          response.xpath('//div[@id="txt_content"]').extract() or \
                          response.xpath('//div[@class="incont_txt"]').extract() or \
                          response.xpath('//div[@class="neiyecontent"]').extract() or \
                          response.xpath('//div[@class="t3"]').extract() or \
                          response.xpath('//div[@class="thi_left_1"]/dl').extract() or \
                          response.xpath('//div[@class=" row-fluid content-time "]/following-sibling::div[@style]').extract()
                if len(content) > 0:
                    item['content'] = content[0]
                    if item['content'] == "":
                        content0 = response.url
                        self.log.write(content0)
                        raise Exception("无详细内容！！！！")
                else:
                    print "error url: ",response.url
                    raise Exception("正文内容未获取成功!!! "+ response.url)

                # 页数 ，图片类的要翻页
                total_pages = response.xpath("//span[@id='showTotal']/text()").extract() or \
                              response.xpath("//a[@class='ptfontcon'][2]/@href").extract()

                total_pages1 = response.xpath('//span[@class="cC00"]/ancestor::span[@id="total"]')

                # 又是另一种翻页规则
                total_pages2 = response.xpath('//span[@id="_function_code_page"]//*[contains(text(), "[")]') or \
                               response.xpath('//span[@id="_function_code_page"]/p/a[last()-1]')

                if len(total_pages) > 0:
                    # total_pages = int(re.search(ur"(\d+).", total_pages[0]).group(1)
                    total_pages = int(total_pages[0])

                elif len(total_pages1) > 0:
                    total_pages1 = int(re.search(r'1/(\d{1,2})', response.body).group(1))

                elif len(total_pages2) > 0:
                    num = total_pages2.xpath('string(.)').extract()[0]
                    try:
                        # 如果上一页 下一页在test_page中，认为不是图片类
                        test_page = re.search(r'\D{2,5}', num).group(0)
                        total_pages2 = 1
                    except Exception, e:
                        total_pages2 = int(re.search(r'[(\d+)]', num).group(0))

                else:
                    total_pages = 1
                    total_pages1 = 1
                    total_pages2 = 1

                if total_pages == []:
                    total_pages = 1
                if total_pages1 == []:
                    total_pages1 = 1
                if total_pages2 == []:
                    total_pages2 = 1

                if total_pages > 1:
                    # 翻页规则　需要定制
                    # url = response.url.replace(".htm","_2.htm")
                    page = int(re.search(r'/(\d+).shtml', response.url).group(1))
                    # for i in range(1, total_pages+1):
                    page_nav = page + 1
                    final_page = page + total_pages -1
                    url_str = '/%d.shtml'%page_nav
                    url = response.url.rpartition('/')[0] + url_str
                    print '处理 total_pages 图片类 %s'%url
                    yield Request(url=url,method='get',
                                  meta={"ba_type": response.meta["ba_type"],"item": item,
                                        "parse_for_content": False,"total_pages": total_pages,"current_page": 2, "final_page": final_page},
                                  callback=self.parse_item,errback=self.parse_err_detail)

                elif total_pages1 > 1:
                    url = response.url + '#p=2'
                    print '处理 total_pages1 图片类 %s'%url
                    yield Request(url=url,method='get',
                                  meta={"ba_type": response.meta["ba_type"],"item": item,
                                        "parse_for_content": False,"total_pages": total_pages1,"current_page": 2, "final_page": "total_page1"},
                                  callback=self.parse_item,errback=self.parse_err_detail)

                elif total_pages2 > 1:
                    url = response.url.rpartition('.')[0] + '_2.%s'%response.url.rpartition('.')[-1]
                    print '处理 total_pages2 图片类 %s'%url
                    yield Request(url=url,method='get',
                                  meta={"ba_type": response.meta["ba_type"],"item": item,
                                        "parse_for_content": False,"total_pages": total_pages2,"current_page": 2, "final_page": "total_page2"},
                                  callback=self.parse_item,errback=self.parse_err_detail)

                else:
                    if len(response.xpath("//*[@id='gmweqxiu']").extract()) > 0:
                        self.print_info("被主动舍弃的详细页: " + response.url + " 原因: 无content",  "warn")
                        pass
                    else:
                        if item['pubtime'] and item['title'] and item['content']:
                            self.print_info("发布时间: " + item['pubtime'] + " 标题: " + item["title"] +'\n'+ " 发布源: " + item['medianame'] + " url: " + response.url + "  共1页")
                            yield item
            else:
                # 中国新闻网的翻页不一样 这段代码特殊点
                print '图片翻页类: 正在处理 %s'%response.url
                item = response.meta["item"]
                final_page = response.meta["final_page"]
                total_pages = response.meta["total_pages"]
                content = response.xpath('//div[@id="cont_show"]').extract() or \
                          response.xpath('//div[@id="eFramePic"]').extract() or \
                          response.xpath('//div[contains(@class,"tp_bdiv dh-")]').extract() or \
                          response.xpath('//div[contains(@class, "bigdiv3")]').extract() or \
                          response.xpath('//div[@id="txt_content"]').extract() or \
                          response.xpath('//td[@id="TT"]').extract() or \
                          response.xpath('//div[@class=" row-fluid content-time "]/following-sibling::div[@style]').extract()

                if len(content) > 0:
                    content = content[0]
                item["content"] += "\n" + content

                if int(response.meta["current_page"]) == int(response.meta["total_pages"]):
                    if item['pubtime'] and item['title'] and item['content']:
                        self.print_info("发布时间: " + item['pubtime'] + " 标题: "+item["title"] +'\n' + " 发布源: " + item['medianame'] + " url: " + response.url + "  共" + str(response.meta["current_page"]) + "页")
                        yield item
                elif final_page == "total_page1":
                    # 因为两个图片频道完全不一样 需要新写一个方法
                    url = response.url.split('#')[0] + '#p=%d'%(int(response.meta['current_page'])+1)
                    yield Request(url=url,method='get',
                                  meta={"ba_type":response.meta["ba_type"],"item":item,
                                        "parse_for_content":False,"total_pages":response.meta["total_pages"],"current_page": response.meta["current_page"] + 1, "final_page": "total_page1"},
                                  callback=self.parse_item,errback=self.parse_err_detail)
                elif final_page == "total_page2":
                    # 又是一个新 翻页规则
                    url = response.url.rpartition('_')[0] + '_%d.%s'%(response.meta['current_page']+1, response.url.rpartition('.')[-1])
                    yield Request(url=url,method='get',
                                  meta={"ba_type":response.meta["ba_type"],"item":item,
                                        "parse_for_content":False,"total_pages":response.meta["total_pages"],"current_page": response.meta["current_page"] + 1, "final_page": "total_page2"},
                                  callback=self.parse_item,errback=self.parse_err_detail)
                else:
                    page = int(re.search(r'/(\d+).shtml', response.url).group(1))
                    if page < final_page:
                        # for i in range(1, total_pages+1):
                        page_nav = page + 1
                        url_str = '/%d.shtml'%page_nav
                        url = response.url.rpartition('/')[0] + url_str
                        # url = response.url.replace("_"+ str(response.meta["current_page"]) + ".htm","_" + str(response.meta["current_page"] + 1 ) +".htm")
                        yield Request(url=url,method='get',
                                      meta={"ba_type":response.meta["ba_type"],"item":item,
                                            "parse_for_content":False,"total_pages":response.meta["total_pages"],"current_page": response.meta["current_page"] + 1, "final_page": final_page},
                                      callback=self.parse_item,errback=self.parse_err_detail)
        except Exception:
            if len(response.xpath("//title/text()").extract()) > 0 and \
                    (u"页面没有找到" in response.xpath("//title/text()").extract()[0] or u"出错啦" in response.xpath("//title/text()").extract()[0]):
                self.print_info(traceback.format_exc() + "url:" + response.url + "  status: "+str(response.status), "error")
            else:
                self.print_info(traceback.format_exc() + "url:" + response.url + "  status: "+str(response.status), "error2")


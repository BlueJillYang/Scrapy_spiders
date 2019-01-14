# -*- coding: utf-8 -*-

# Scrapy settings for guangming project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'guangming'

SPIDER_MODULES = ['guangming.spiders']
NEWSPIDER_MODULE = 'guangming.spiders'

LOG_LEVEL = 'ERROR'
LOG_FILE = 'Debug.log'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'guangming.middlewares.GuangmingSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'guangming.middlewares.GuangmingDownloaderMiddleware': 543,
   # 'guangming.middlewares.Proxy_choice': 123,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'guangming.pipelines.GuangmingPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

PROXIES = [
   'https://119.101.116.85:9999',
   'http://119.101.113.162:9999',
   'https://119.101.115.164:9999',
   'http://119.39.238.25:9999',
   'http://119.101.118.93:9999',
   'https://119.101.117.15:9999',
   'http://119.101.118.134:9999',
   'https://119.101.116.63:9999',
   'https://222.95.175.136:9999',
   'http://119.101.113.106:9999',
   'https://119.101.114.84:9999',
   'http://119.101.112.135:9999',
   'http://119.101.116.136:9999',
   'https://119.101.115.194:9999',
   'http://119.39.238.94:9999',
   'https://119.101.116.159:9999',
   'https://119.101.118.59:9999',
   'https://119.101.115.11:9999',
   'https://110.52.235.215:9999',
   'http://119.101.114.82:9999',
   'https://119.101.113.21:9999',
   'https://119.101.114.28:9999',
   'https://125.123.136.14:9999',
   'http://119.101.116.105:9999',
   'https://119.101.112.138:9999',
   'http://171.41.82.86:9999',
   'https://58.55.135.14:9999',
   'https://121.61.24.51:9999',
   'http://110.52.235.10:9999',
   'http://119.101.112.228:9999',
   'http://111.181.58.6:9999',
   'https://119.101.117.106:9999',
   'https://119.101.117.181:9999',
   'http://27.24.167.102:9999',
   'https://119.101.118.160:9999',
   'https://119.101.114.155:9999',
   'https://119.101.112.71:9999',
   'http://119.101.112.246:9999',
   'http://125.123.142.118:9999',
   'https://118.122.92.252:37901',
   'http://119.101.118.146:9999',
   'https://119.101.117.159:9999',
   'http://113.128.8.204:9999',
   'http://119.101.118.79:9999',
   'https://119.101.112.219:9999',
   'https://119.101.116.66:9999',
   'https://119.101.118.156:9999',
   'https://119.101.118.109:9999',
   'http://119.101.113.181:9999',
   'http://119.101.113.198:9999',
   'https://119.101.113.231:9999',
   'http://119.101.117.1:9999',
   'https://119.101.116.207:9999',
   'https://119.101.113.207:9999',
   'https://119.101.114.233:9999',
   'https://119.101.117.26:9999',
]

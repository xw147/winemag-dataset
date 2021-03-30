'''
Created on 11 Mar 2021

@author: haha
'''

import scrapy.cmdline
from scrapy.crawler import CrawlerProcess
from winemag.spiders.winemag_spider import WinemagSpider





if __name__ == '__main__':
    # start spider from command line
#     scrapy.cmdline.execute(argv=['scrapy', 'crawl', 'winemag',
#                                  '-a', '-a start_page=1',
#                                  '-a', '-a end_page=1',
#                                   '-o', 'review.csv',
#                                  '-t', 'csv'])

# start spider 
#     process = CrawlerProcess()
#     process.crawl(WinemagSpider, start_page=1, end_page=6)
#     process.start()
    
    pass
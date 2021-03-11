'''
Created on 11 Mar 2021

@author: haha
'''

import scrapy.cmdline

if __name__ == '__main__':
    scrapy.cmdline.execute(argv=['scrapy', 'crawl', 'winemag',
                                 '-a', '-a start_page=1',
                                 '-a', '-a end_page=1',
                                  '-o', 'review.csv',
                                 '-t', 'csv'])
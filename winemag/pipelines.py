# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter
from scrapy.pipelines.images import ImagesPipeline
from scrapy import signals
import logging as log



class DuplicateURLsPipeline(object):

    def __init__(self):
        self.urls_seen = set()
        
        

    def process_item(self, item, spider):
        log.info("I'm processing the following item {}".format(item))
        
        print("=================================================")
        
        if item['url'] in self.urls_seen:
            raise DropItem('URL processed. Dropping {}'.format(item['url']))
        else:
            self.urls_seen.add(item['url'])
            return item
        


class ImagesDownloadPipeline(ImagesPipeline):
    
    def file_path(self, request, response=None, info=None):
        """
        重写ImagesPipeline类的file_path方法
        实现：下载下来的图片命名是以校验码来命名的，该方法实现保持原有图片命名
        :return: 图片路径
        """
        image_guid = request.url.split('/')[-1]   # 取原url的图片命名
        return 'full/%s' % (image_guid)
    
    def get_media_requests(self, item, info):
        """
        遍历image_urls里的每一个url，调用调度器和下载器，下载图片
        :return: Request对象
        图片下载完毕后，处理结果会以二元组的方式返回给item_completed()函数
        """
        for image_url in item['imgUrl']:
            yield Request(image_url)
 
    def item_completed(self, results, item, info):
        """
        将图片的本地路径赋值给item['image_paths']
        :param results:下载结果，二元组定义如下：(success, image_info_or_failure)。
        第一个元素表示图片是否下载成功；第二个元素是一个字典。
        如果success=true，image_info_or_error词典包含以下键值对。失败则包含一些出错信息。
         字典内包含* url：原始URL * path：本地存储路径 * checksum：校验码
        :param item:
        :param info:
        :return:
        """
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")   # 如果没有路径则抛出异常
        item['image_paths'] = image_paths
        return item




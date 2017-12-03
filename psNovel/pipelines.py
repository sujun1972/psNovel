# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from psNovel.items import Novel, Chapter


class PsnovelPipeline(object):
    def process_item(self, item, spider):
        print(item)
        if isinstance(item, Novel):
            print("this is Novel")
        if isinstance(item, Chapter):
            print("this is Chapter")
        input("---------")
        return item

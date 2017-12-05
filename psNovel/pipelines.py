# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from psNovel.items import Novel, Chapter
from scrapy.pipelines.images import ImagesPipeline


class PsnovelPipeline(object):
    def process_item(self, item, spider):
        print(item)
        if isinstance(item, Novel):
            print("this is Novel")
        if isinstance(item, Chapter):
            print("this is Chapter")
        return item


class PosterPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        image_name = image_guid.replace('.'.join(image_guid.split('.')[0:-1]), request.meta['image_name'])
        return 'full/%s' % (image_name)

    def thumb_path(self, request, thumb_id, response=None, info=None):
        image_guid = thumb_id + response.url.split('/')[-1]
        return 'thumbs/%s/%s.jpg' % (thumb_id, image_guid)

    def get_media_requests(self, item, info):
        if isinstance(item, Novel):
            for image_url in item['image_urls']:
                yield scrapy.Request(image_url, meta={'image_name': item["id"]})

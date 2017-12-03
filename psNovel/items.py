# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Novel(scrapy.Item):
    id = scrapy.Field()
    # 作品名称
    title = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 文案
    intro = scrapy.Field()
    # 封面图片
    poster = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
    # 标签
    tags = scrapy.Field()
    # 关键字
    key_leadings = scrapy.Field()
    key_supportings = scrapy.Field()
    key_other = scrapy.Field()
    # 文章类型
    genre = scrapy.Field()
    # 作品视角
    view = scrapy.Field()
    # 作品风格
    style = scrapy.Field()
    # 作品系列
    series = scrapy.Field()
    # 文章进度
    updateStatus = scrapy.Field()
    # 全文字数
    wordCount = scrapy.Field()
    # 是否出版
    published = scrapy.Field()
    # 是否已签约
    signed = scrapy.Field()
    # 网站简评
    comment = scrapy.Field()


class Chapter(scrapy.Item):
    novel_id = scrapy.Field()
    chapter_id = scrapy.Field()
    chapter_content = scrapy.Field()
    chapter_summary = scrapy.Field()
    chapter_title = scrapy.Field()
    chapter_group = scrapy.Field()
    chapter_url = scrapy.Field()
    chapter_vip = scrapy.Field()
    chapter_word_count = scrapy.Field()
    chapter_updated = scrapy.Field()
    chapter_locked = scrapy.Field()

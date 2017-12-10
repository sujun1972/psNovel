# -*- coding: utf-8 -*-

from psNovel.mysql import *


class NovelRecord(object):
    id = 0
    title = ""
    author = ""
    intro = ""
    poster = ""
    images = ""
    image_urls = ""
    tags = ""
    key_leadings = ""
    key_supportings = ""
    key_other = ""
    genre = ""
    view = ""
    style = ""
    series = ""
    updateStatus = ""
    wordCount = ""
    published = ""
    signed = ""
    comment = ""

    def __init__(self):
        self.id = 0
        self.title = ""
        self.author = ""
        self.intro = ""
        self.poster = ""
        self.images = ""
        self.image_urls = ""
        self.tags = ""
        self.key_leadings = ""
        self.key_supportings = ""
        self.key_other = ""
        self.genre = ""
        self.view = ""
        self.style = ""
        self.series = ""
        self.updateStatus = ""
        self.wordCount = ""
        self.published = ""
        self.signed = ""
        self.comment = ""


    def exists(self):
        if self.id == 0:
            return True
        mysql_query = "SELECT `id` FROM novel WHERE `id` = %s" % self.id
        DB = MysqlNovelDB(mysql_query)
        res = DB.execute()
        print(res)
        input("--------------")


    def insert(self):
        pass


    def update(self):
        pass
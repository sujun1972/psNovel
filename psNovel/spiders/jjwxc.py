# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from psNovel.items import Novel, Chapter
from bs4 import *
from urllib import parse


class JjwxcSpider(scrapy.Spider):
    name = 'jjwxc'
    allowed_domains = ['jjwxc.net']

    def start_requests(self):
        urls = [
            # 'http://www.jjwxc.net/onebook.php?novelid=1888526',
            'http://www.jjwxc.net/onebook.php?novelid=3160517'
            # 'http://www.jjwxc.net/onebook.php?novelid=65066'
        ]
        for url in urls:
            novel_id = url.split("?novelid=")[-1]
            yield scrapy.Request(url=url, callback=self.parse, meta={'novel_id': novel_id})

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        novel_id = response.meta.get('novel_id')
        novel = Novel()
        novel['id'] = novel_id
        novel['title'] = response.xpath('//span[@class="bigtext"]//span/text()').extract_first()
        novel['author'] = response.xpath('//span[@itemprop="author"]/text()').extract_first()

        novel['intro'] = soup.find('div', {"id": "novelintro"}).text

        novel_metadata = response.xpath('//ul[@name="printright"]/li').extract()
        # 第一行：文章类型
        novel['genre'] = Selector(text=novel_metadata[0]).xpath('//span[@itemprop="genre"]/text()').extract_first()\
            .strip()
        # 第二行：作品视角
        novel['view'] = Selector(text=novel_metadata[1]).xpath('//li/text()').extract_first().strip()

        # 第三行：作品风格
        novel['style'] = Selector(text=novel_metadata[2]).xpath('//li/text()').extract_first().strip()

        # 第四行：作品系列
        novel['series'] = Selector(text=novel_metadata[3]).xpath('//span[@itemprop="series"]/text()').extract_first()\
            .strip()

        # 第五行：文章进度
        if (Selector(text=novel_metadata[4]).xpath('//span[@itemprop="updataStatus"]/font')):
            novel['updateStatus'] = Selector(text=novel_metadata[4]).xpath(
                '//span[@itemprop="updataStatus"]/font/text()') \
                .extract_first().strip()
        else:
            novel['updateStatus'] = Selector(text=novel_metadata[4]).xpath('//span[@itemprop="updataStatus"]/text()')\
                .extract_first().strip()

        # 第六行：全文字数
        novel['wordCount'] = Selector(text=novel_metadata[5]).xpath('//span[@itemprop="wordCount"]/text()')\
            .extract_first().strip()

        # 第七行：是否出版
        published = BeautifulSoup(novel_metadata[6], "lxml").text
        novel['published'] = published.replace("是否出版：", "").replace("（联系出版）", "").strip()

        # 第八行：签约状态
        novel['signed'] = Selector(text=novel_metadata[7]).xpath('//font/text()').extract_first().strip()

        comment = Selector(text=novel_metadata[8]).xpath('//div[@id="marknovel_message"]/text()')
        if comment:
            novel['comment'] = comment.extract_first()
        else:
            novel['comment'] = ''

        poster = parse.urlsplit(soup.find('img', {"itemprop": "image"})["src"]).path.split('/')[-1]
        poster_url = soup.find('img', {"itemprop": "image"})["src"]
        novel["poster"] = poster
        novel["images"] = [poster]
        novel["image_urls"] = [poster_url]

        tags = []
        html_tags = soup.findAll("div", {"class": "smallreadbody"})[-1].findAll("font")
        for html_tag in html_tags:
            tags.append(html_tag.text.strip())
        novel["tags"] = '|'.join(tags)

        html_keys = soup.findAll("div", {"class": "smallreadbody"})[-1].find("span", {"class": "bluetext"}).text
        key_array = html_keys.replace("搜索关键字：", "").split("┃")
        key_leadings = key_array[0].replace("主角：", "").strip().split("，")
        key_supportings = key_array[1].replace("配角：", "").strip().split("，")
        key_other = key_array[2].replace("其它：", "").strip().split("，")

        novel["key_leadings"] = key_leadings
        novel["key_supportings"] = key_supportings
        novel["key_other"] = key_other

        soup_table = soup.find("table", {"id": "oneboolt"})

        soup_lines = soup_table.findAll('tr')[3:-1]
        current_group = ""
        for soup_line in soup_lines:
            soup_tds = soup_line.findAll("td")
            if len(soup_tds) == 1:
                current_group = soup_tds[0].text
            else:
                chapter = Chapter()
                if soup_tds[1].find('a').has_attr("href"):
                    chapter['chapter_vip'] = "No"
                    chapter['chapter_url'] = soup_tds[1].find('a')['href']
                else:
                    chapter['chapter_vip'] = "Yes"
                    chapter['chapter_url'] = soup_tds[1].find('a')['rel']
                chapter['novel_id'] = novel_id
                chapter['chapter_group'] = current_group
                chapter['chapter_id'] = soup_tds[0].text.strip()
                chapter['chapter_title'] = soup_tds[1].text.strip()
                chapter['chapter_summary'] = soup_tds[2].text.strip()
                chapter['chapter_word_count'] = soup_tds[3].text.strip()
                if(len(soup_tds) == 5):
                    chapter['chapter_updated'] = soup_tds[4].text.strip()
                else:
                    chapter['chapter_updated'] = soup_tds[5].text.strip()
                if (chapter['chapter_vip'] == "No"):
                    yield scrapy.Request(url=chapter['chapter_url'],
                                         callback=self.parse_chapter, meta={'chapter': chapter})
        yield(novel)

    def parse_chapter(self, response):
        chapter = response.meta.get('chapter')

        soup = BeautifulSoup(response.body, "lxml")
        soup_text = soup.find("div", {"class": "noveltext"})
        soup_divs = soup.findAll("div")
        for soup_div in soup_divs:
            soup_div.extract()
        soup_hrs = soup.findAll("hr")
        for soup_hr in soup_hrs:
            soup_hr.extract()
        str_content = str(soup_text).replace("<br/>", "\r\n").replace('<hr size="1"/>', "")
        soup_content = BeautifulSoup(str_content, "lxml").text
        chapter_lines = []
        lines = (str(soup_content).split("\r\n"))
        for line in lines:
            chapter_lines.append(line.strip())
        chapter_content = "\r\n".join(chapter_lines)
        chapter['chapter_content'] = chapter_content

        yield(chapter)

import re

import sys
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentdir)
from items import postItem
import scrapy
import psycopg2

class WdBlogSpider(scrapy.Spider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'wd_blog'
    start_urls = [
        "http://wdxtub.com/",
        # "http://wdxtub.com/page/2/",
        # "http://wdxtub.com//2016/08/19/tea-wine-friend/"
    ]

    def __init__(self):
        # for i in range(2, 61):
        #     self.start_urls += ["http://wdxtub.com/page/%d/" % i]

        conn = psycopg2.connect(database="postgres", user="postgres", host="db", port="5432")
        query_cu = conn.cursor()
        query_cu.execute('SELECT link FROM interviews_post')
        tuple_list = query_cu.fetchall()
        self.link_tuple = ()
        for t in tuple_list:
            self.link_tuple += t
        query_cu.close()
        conn.close()

    def parse(self, response):
        a_list = response.xpath("//article[@class='post post-type-normal ']//a[@class='post-title-link']/@href").extract()
        # print len(a_list)
        # self.parse_page(response)

        for a in a_list:
            # print a
            url = "http://wdxtub.com" + a
            if not self.is_dup(url):
                # print "Yielding New Request :" + a_href
                yield scrapy.Request(url, callback=self.parse_page)


    def parse_page(self, response):
        # print response.url
        title = response.xpath("//h1[@class='post-title']/text()").extract_first().encode('utf-8')
        title = re.sub(r"(')|(\n)|( )", "", title)

        time = response.xpath("//time[@itemprop='dateCreated']/@datetime").extract_first().encode('utf-8')

        p_list = response.xpath("//div[@class='post-body']//p/text()").extract()

        desc = ""
        for p in p_list:
            desc += p.encode('utf-8')

        tag = response.xpath("//span[@class='post-category']//span[@itemprop='name']/text()").extract_first().encode('utf-8')
        tag += " wdxtub "

        item = postItem()
        item['title'] = self.process_content(title)
        item['link'] = self.process_content(response.url)
        item['create_time'] = self.process_content(time)
        item['source'] = "wdxtub.com"
        item['source_link'] = "http://wdxtub.com/"
        item['desc'] = self.process_content(desc)
        item['tag'] = self.process_content(tag)

        yield item

        # yield {
        #     'name': "qwe",
        #     'description': "qwe",
        #     'link': "qwe",
        # }


    def is_dup(self, url):
        if url in self.link_tuple:
            return True
        else:
            return False

    def process_content(self, content):
        desc = re.sub(r"(')", "", content)
        return desc

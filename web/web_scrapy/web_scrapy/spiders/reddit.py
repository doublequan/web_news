import re

import sys
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentdir)
from items import postItem
import scrapy
import re
import psycopg2


class RedditSpider(scrapy.Spider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'reddit'
    start_urls = [
        "https://www.reddit.com/r/technology",
        "https://www.reddit.com/r/nba",
        "https://www.reddit.com/r/science/",
        "https://www.reddit.com/r/news/",
        "https://www.reddit.com/r/cmu",
    ]
    MAX_PAGE = 300

    def __init__(self):
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
        url_list = response.xpath("//ul[@class='flat-list buttons']/li[@class='first']/a/@href").extract()
        real_url_list = response.xpath("//div[@class='entry unvoted']/p[@class='title']/a/@href").extract()

        if len(url_list) != len(real_url_list):
            for i in range(0, 50):
                print "FUCK!!!!!! NOT EQUAL!!!"
            return

        # for post in post_list:
        #     title = post.xpath("p[@class='title']/a/text()").extract_first().encode('utf-8')
        #     url = post.xpath("p[@class='title']/a/@href").extract_first().encode('utf-8')
        #     time = post.xpath("p[@class='tagline']/time/@datetime").extract_first().encode('utf-8')
        #     source = "reddit"
        #     print time


        # title_list =
        # print len(url_list)
        # self.parse_page(response)

        for i in xrange(0, len(url_list)):
            # print url
            # url = url.encode("utf-8")
            if not self.is_dup(real_url_list[i]):
                # print "Yielding New Request :" + a_href
                if real_url_list[i] == url_list[i]:
                    continue
                if real_url_list[i].startswith("https://www.reddit.com"):
                    continue
                if not real_url_list[i].startswith("http"):
                    continue
                yield scrapy.Request(url_list[i], callback=self.parse_page)

        next_url = response.xpath("//span[@class='next-button']/a/@href").extract_first()
        if self.MAX_PAGE > 0:
            self.MAX_PAGE -= 1
            yield scrapy.Request(next_url, callback=self.parse)


    def parse_page(self, response):
        # print response.text
        posts = response.xpath("//div[@class='entry unvoted']")
        title = posts.xpath("p[@class='title']/a/text()").extract_first().encode('utf-8')
        # title = re.sub(r"(')|(\n)", "", title)

        url = posts.xpath("p[@class='title']/a/@href").extract_first().encode('utf-8')
        if not str(url).startswith("http"):
            url = response.url

        time = posts.xpath("p[@class='tagline']/time/@datetime").extract_first()
        if time:
            time = time.encode('utf-8')
        else:
            return

        tag = posts.xpath("p[@class='title']/span[@class='linkflairlabel']/text()").extract_first()
        if tag:
            tag = tag.encode('utf-8') + " "
        else:
            tag = ""

        match = re.search(r"(?<=/r/)\w+(?=/comments)", response.url)
        if match:
            tag += match.group(0) + " "
        tag += "Reddit "

        desc = ""

        # print posts.extract()

        # comments = response.xpath("//div[@class='sitetable nestedlisting']//div[class='entry unvoted']")
        # comments = response.xpath("//div[class='entry unvoted']")
        for comment in posts[1:]:
            auther = comment.xpath("p[@class='tagline']/a[2]/text()").extract_first()
            if auther:
                auther = auther.encode('utf-8')
                content = ""
                contents = comment.xpath("form/div/div/p/text()").extract()
                for p in contents:
                    content += p
                desc += auther + ": " + content + "\n"


        # print "**********"
        # print title
        # print desc
        # print url
        # print time
        # print tag
        # print "**********"

        item = postItem()
        item['title'] = self.escape_string(title)
        item['link'] = self.process_content(url)
        item['create_time'] = self.process_content(time)
        item['source'] = "reddit"
        item['source_link'] = "https://www.reddit.com/"
        item['desc'] = self.escape_string(desc)
        item['tag'] = self.escape_string(tag)
        yield item

    def is_dup(self, url):
        # print "!!!!!!!!!!!!!!!!" + url + "!!!!!!!!!!!!!!!!!!!"

        # self.query_cu.execute('SELECT * FROM interviews_post WHERE link = %s'
        #                       , (url,))
        # rst = self.query_cu.fetchall()

        # print self.link_tuple

        if url in self.link_tuple:
            print url, "exist"
            return True
        else:
            print url, "hit"
            return False

    def process_content(self, content):
        desc = re.sub(r"(')", "", content)
        return desc

    def process_title_desc(self, content):
        desc = re.sub(r"(')|(/)", "", content)
        return desc

    def escape_string(self, desc):
        desc = re.sub(r"(')|(\")|($)|(\t)|(\r)|(\\)", "", desc)
        return desc
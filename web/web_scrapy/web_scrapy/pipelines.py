# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2


class CheckDuplication(object):
    def process_item(self, item, spider):
        return item


class AddTag(object):
    def process_item(self, item, spider):

        return item


class PutIntoDB(object):
    def __init__(self):
        self.conn = psycopg2.connect(database="postgres", user="postgres", host="db", port="5432")

    def process_item(self, item, spider):
        # print "*****************process items****************"

        # print item['title']
        # print item['link']
        # print item['create_time']
        # print item['source']
        # print item['desc']
        # print item['tag']
        cu = self.conn.cursor()

        cu.execute("INSERT INTO interviews_post (title, link, create_time, source, description, tag, source_link)"
                   " VALUES (%s, %s, %s, %s, %s, %s, %s);", (
            item['title'],
            item['link'],
            "'" + item['create_time'] + "'",
            item['source'],
            item['desc'],
            item['tag'],
            item['source_link']
        ))

        self.conn.commit()
        cu.close()
        return item
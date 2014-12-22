# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

from extractJoke.save_to_mongo import SaveToMongo

class SaveJokePipeline(object):
    def open_spider(self, spider):
        self._db = SaveToMongo()
        self._db.clear_data()

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self._db.save_data(dict(item))
        raise DropItem("handler over")

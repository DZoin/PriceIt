# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import logging

class DistrictsPipeline(object):
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(item)
        if len(self.items) >= 128:
            self.insert_current_items()
        return item

    def insert_current_items(self):
        items = self.items
        self.items = []
        with sqlite3.connect("/home/zoin/workspace/RealEstateAdvisor/realEstate.sqlite") as db:
            cursor = db.cursor()
            names = [(it['name'],) for it in items]
            try:
                cursor.executemany('''INSERT OR REPLACE INTO Districts(Name)
                                      VALUES(?)''', names)
            except sqlite3.IntegrityError:
                db.rollback()
            else:
                db.commit()

    def close_spider(self, spider):
        self.insert_current_items()
        
class EstatesPipeline(object):
    def __init__(self):
        self.estates = []

    def process_item(self, item, spider):
        self.estates.append(item)
        if len(self.estates) >= 128:
            self.insert_current_items()
        return item

    def insert_current_items(self):
        estates = self.estates
        self.estates = []
        with sqlite3.connect("/home/zoin/workspace/RealEstateAdvisor/realEstate.sqlite") as db:
            cursor = db.cursor()
            inData = [(estate['price'], estate['area'], estate['district']) for estate in estates]
            districts = [(estate['district'],) for estate in estates]
            try:
                cursor.executemany('''INSERT OR REPLACE INTO Districts(Name)
                                      VALUES(?)''', districts)
                cursor.executemany('''INSERT OR REPLACE INTO RealEstates(Price, Area, District)
                                      VALUES(?,?,(SELECT ID from Districts WHERE Name LIKE ? COLLATE NOCASE))''', inData)
            except sqlite3.IntegrityError:
                db.rollback()
            else:
                db.commit()

    def close_spider(self, spider):
        self.insert_current_items()

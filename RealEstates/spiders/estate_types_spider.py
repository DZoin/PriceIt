import scrapy
import sqlite3

class RealEstateAdvisorSpider(scrapy.Spider):
    name = "estateTypes"
    start_urls = [
        'http://www.imoti.com/pcgi/search.cgi?act=2&pn=1&curr=1&sort=1'
    ]
    def parse(self, response):
        with sqlite3.connect("/home/zoin/workspace/RealEstateAdvisor/realEstate.sqlite") as db:
            cursor = db.cursor()
            for item in response.xpath('//*[@id="gr1"]/child::node()/label/text()').extract():
                try:
                    cursor.execute('''INSERT INTO RealEstateType(Name)
                               VALUES(?)''', (item,))
                except sqlite3.IntegrityError:
                    db.rollback()
                else:
                    db.commit()

            for item in response.xpath('//*[@id="gr2"]/child::node()/label/text()').extract():
                try:
                    cursor.execute('''INSERT INTO RealEstateType(Name)
                               VALUES(?)''', (item,))
                except sqlite3.IntegrityError:
                    db.rollback()
                else:
                    db.commit()

            for item in response.xpath('//*[@id="gr3"]/child::node()/label/text()').extract():
                try:
                    cursor.execute('''INSERT INTO RealEstateType(Name)
                               VALUES(?)''', (item,))
                except sqlite3.IntegrityError:
                    db.rollback()
                else:
                    db.commit()

            for item in response.xpath('//*[@id="gr4"]/child::node()/label/text()').extract():
                try:
                    cursor.execute('''INSERT INTO RealEstateType(Name)
                               VALUES(?)''', (item,))
                except sqlite3.IntegrityError:
                    db.rollback()
                else:
                    db.commit()

            for item in response.xpath('//*[@id="gr5"]/child::node()/label/text()').extract():
                try:
                    cursor.execute('''INSERT INTO RealEstateType(Name)
                               VALUES(?)''', (item,))
                except:
                    db.rollback()
                else:
                    db.commit()

            for item in response.xpath('//*[@id="gr6"]/child::node()/label/text()').extract():
                try:
                    cursor.execute('''INSERT INTO RealEstateType(Name)
                               VALUES(?)''', (item,))
                except:
                    db.rollback()
                else:
                    db.commit()

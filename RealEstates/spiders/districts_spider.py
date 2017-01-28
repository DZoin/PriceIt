import scrapy
import sqlite3

class RealEstateAdvisorSpider(scrapy.Spider):
    name = "districtsSpider"
    start_urls = [
        'https://bg.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:\
%D0%9A%D0%B2%D0%B0%D1%80%D1%82%D0%B0%D0%BB%D0%B8_%D0%B8_%D0%B6%D0%B8%D0%BB%D0%B8%D1%89%D0%BD%D0\
%B8_%D0%BA%D0%BE%D0%BC%D0%BF%D0%BB%D0%B5%D0%BA%D1%81%D0%B8_%D0%BD%D0%B0_%D0%A1%D0%BE%D1%84%D0%B8%D1%8F'
    ]
    def parse(self, response):
        with sqlite3.connect("/home/zoin/workspace/RealEstateAdvisor/realEstate.sqlite") as db:
            cursor = db.cursor()
            for item in response.xpath('//*[@id="mw-pages"]/div/div/child::node()/ul/li/a/text()').extract():
                try:
                    cursor.execute('''INSERT INTO Districts(Name)
                               VALUES(?)''', (item,))
                except sqlite3.IntegrityError:
                    db.rollback()
                else:
                    db.commit()

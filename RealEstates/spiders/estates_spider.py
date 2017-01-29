import scrapy
import sys
sys.path.append('/home/zoin/workspace/RealEstateAdvisor/RealEstates')
from items import EstatesItem
import re
import logging

class RealEstateAdvisorSpider(scrapy.Spider):
    name = "estatesSpider"
    custom_settings = {
	'ITEM_PIPELINES': {
	    'RealEstates.pipelines.EstatesPipeline': 400
	}
    }
    def start_requests(self):
        for count in range(1, 250):
            yield scrapy.Request('http://www.imoti.com/pcgi/results.cgi?page={0}&searchres=01ezf991&pn=1&sort=1&nraion=43&curr=2'.format(count), callback=self.parse)
        
    def parse(self, response):
        for next_url in response.xpath('/html/body/div[3]/div[3]/div[1]/div/child::node()/a/@href').extract():
            request = scrapy.Request('http://www.imoti.com/pcgi/' + next_url, callback = self.parse_inner)
            yield request

    def parse_inner(self, response):
        #self.logger.info('Got successful response from {}'.format(response.url))
        estate = EstatesItem()
        title = response.xpath('/html/body/div[5]/div[2]/div[1]/h1/span/text()').extract_first()
        priceString = response.xpath('/html/body/div[5]/div[2]/div[1]/div/text()').extract_first()
        areaString = response.xpath('/html/body/div[5]/div[2]/ul/li[2]/div[1]/div[2]/div[1]/span/text()').extract_first()
        if not title or not priceString or not areaString:
            return
        else:
            price = re.sub(r"\D", "", priceString.encode('utf-8'))
            area = re.sub(r"\D", "", areaString.encode('utf-8'))
            titleTokens = title.split(", ")
            estate['district'] = titleTokens[1]
            estate['area'] = area.decode('utf-8')
            estate['price'] = price.decode('utf-8')
            yield estate
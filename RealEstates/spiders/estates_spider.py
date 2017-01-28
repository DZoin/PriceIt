import scrapy
import sys
sys.path.append('/home/zoin/workspace/RealEstateAdvisor/RealEstates')
from items import EstatesItem
import re

class RealEstateAdvisorSpider(scrapy.Spider):
    name = "estatesSpider"
    custom_settings = {
	'ITEM_PIPELINES': {
	    'RealEstates.pipelines.EstatesPipeline': 400
	}
    }
    def start_requests(self):
        for count in (1, 2):
            yield scrapy.Request('http://www.imoti.com/pcgi/results.cgi?page=%d&searchres=01ezf991&pn=1&sort=1&nraion=43&curr=2' % count, callback=self.parse_inner)
        
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
            price = re.sub(r"\D", "", areaString.encode('utf-8'))
            titleTokens = title.split(", ")
            estate['district'] = titleTokens[1].encode('utf-8')
            estate['area'] = area
            estate['price'] = price
            yield estate
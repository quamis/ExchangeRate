from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from ExchangeRate.items import ExchangerateItem
import re

class BNRSpider(BaseSpider):
	name = "BNR"
	allowed_domains = ["www.bnr.ro"]
	start_urls = [
		"http://www.bnro.ro/nbrfxrates.xml",
	]

	def parse(self, response):
		# remove namespace definitions
		responseNew = response.replace(body=re.sub(' xmlns="[^"]+"', '', response.body, count=1))
		hxs = Selector(responseNew)
		item = ExchangerateItem()
		
		item['EUR_buy'] = float(hxs.xpath('//Body//Cube//Rate[@currency="EUR"]/text()').extract()[0])
		item['EUR_sell'] = float(hxs.xpath('//Body//Cube//Rate[@currency="EUR"]/text()').extract()[0])
		
		item['USD_buy'] = float(hxs.xpath('//Body//Cube//Rate[@currency="USD"]/text()').extract()[0])
		item['USD_sell'] = float(hxs.xpath('//Body//Cube//Rate[@currency="USD"]/text()').extract()[0])
		
		item['GBP_buy'] = float(hxs.xpath('//Body//Cube//Rate[@currency="GBP"]/text()').extract()[0])
		item['GBP_sell'] = float(hxs.xpath('//Body//Cube//Rate[@currency="GBP"]/text()').extract()[0])
		
		item['CHF_buy'] = float(hxs.xpath('//Body//Cube//Rate[@currency="CHF"]/text()').extract()[0])
		item['CHF_sell'] = float(hxs.xpath('//Body//Cube//Rate[@currency="CHF"]/text()').extract()[0])
		
		return [item]
		
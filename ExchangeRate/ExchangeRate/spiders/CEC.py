from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from ExchangeRate.items import ExchangerateItem
import re

class CECSpider(BaseSpider):
	name = "CEC"
	allowed_domains = ["www.cec.ro"]
	start_urls = [
		"https://www.cec.ro/curs-valutar",
	]

	def parse(self, response):
		hxs = Selector(response)
		item = ExchangerateItem()
        
		item['EUR_buy'] = float(hxs.xpath('//table[contains(@class, "views-table")]//td/div[contains(text(), "EUR")]/../../td[4]/text()').extract()[0].strip())
		item['EUR_sell'] = float(hxs.xpath('//table[contains(@class, "views-table")]//td/div[contains(text(), "EUR")]/../../td[5]/text()').extract()[0].strip())
		
		item['USD_buy'] = float(hxs.xpath('//table[contains(@class, "views-table")]//td/div[contains(text(), "USD")]/../../td[4]/text()').extract()[0].strip())
		item['USD_sell'] = float(hxs.xpath('//table[contains(@class, "views-table")]//td/div[contains(text(), "USD")]/../../td[5]/text()').extract()[0].strip())
		
		item['GBP_buy'] = float(hxs.xpath('//table[contains(@class, "views-table")]//td/div[contains(text(), "GBP")]/../../td[4]/text()').extract()[0].strip())
		item['GBP_sell'] = float(hxs.xpath('//table[contains(@class, "views-table")]//td/div[contains(text(), "GBP")]/../../td[5]/text()').extract()[0].strip())

		item['CHF_buy'] = float(hxs.xpath('//table[contains(@class, "views-table")]//td/div[contains(text(), "CHF")]/../../td[4]/text()').extract()[0].strip())
		item['CHF_sell'] = float(hxs.xpath('//table[contains(@class, "views-table")]//td/div[contains(text(), "CHF")]/../../td[5]/text()').extract()[0].strip())
		
		return [item]
		
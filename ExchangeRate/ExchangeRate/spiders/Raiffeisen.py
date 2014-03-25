from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from ExchangeRate.items import ExchangerateItem
import re

class RaiffeisenSpider(BaseSpider):
	name = "Raiffeisen"
	allowed_domains = ["www.raiffeisen.ro"]
	start_urls = [
		"http://www.raiffeisen.ro/curs-valutar",
	]

	def parse(self, response):
		hxs = Selector(response)
		item = ExchangerateItem()
		
		item['EUR_buy'] =  float(hxs.xpath('//div[@class="rzbContentTextNormal"]//table//td[contains(text(), "EUR")]/../td[4]/text()').extract()[0])
		item['EUR_sell'] = float(hxs.xpath('//div[@class="rzbContentTextNormal"]//table//td[contains(text(), "EUR")]/../td[5]/text()').extract()[0])
		
		item['USD_buy'] =  float(hxs.xpath('//div[@class="rzbContentTextNormal"]//table//td[contains(text(), "USD")]/../td[4]/text()').extract()[0])
		item['USD_sell'] = float(hxs.xpath('//div[@class="rzbContentTextNormal"]//table//td[contains(text(), "USD")]/../td[5]/text()').extract()[0])
		
		item['GBP_buy'] =  float(hxs.xpath('//div[@class="rzbContentTextNormal"]//table//td[contains(text(), "GBP")]/../td[4]/text()').extract()[0])
		item['GBP_sell'] = float(hxs.xpath('//div[@class="rzbContentTextNormal"]//table//td[contains(text(), "GBP")]/../td[5]/text()').extract()[0])

		item['CHF_buy'] =  float(hxs.xpath('//div[@class="rzbContentTextNormal"]//table//td[contains(text(), "CHF")]/../td[4]/text()').extract()[0])
		item['CHF_sell'] = float(hxs.xpath('//div[@class="rzbContentTextNormal"]//table//td[contains(text(), "CHF")]/../td[5]/text()').extract()[0])
		
		return [item]
		
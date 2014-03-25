from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from ExchangeRate.items import ExchangerateItem
import re

class CECSpider(BaseSpider):
	name = "CEC"
	allowed_domains = ["www.cec.ro"]
	start_urls = [
		"https://www.cec.ro/curs-valutar.aspx",
	]

	def parse(self, response):
		hxs = Selector(response)
		item = ExchangerateItem()
		
		# EUR & USD are repeated 3 times in the whole page, pick the 2'nd one
		item['EUR_buy'] = float(re.sub("[A-Z]", "", hxs.xpath('//td[contains(text(), "EUR")]/../td[3]/text()').extract()[0]).strip())
		item['EUR_sell'] = float(re.sub("[A-Z]", "", hxs.xpath('//td[contains(text(), "EUR")]/../td[4]/text()').extract()[0]).strip())
		
		item['USD_buy'] = float(re.sub("[A-Z]", "", hxs.xpath('//td[contains(text(), "USD")]/../td[3]/text()').extract()[0]).strip())
		item['USD_sell'] = float(re.sub("[A-Z]", "", hxs.xpath('//td[contains(text(), "USD")]/../td[4]/text()').extract()[0]).strip())
		
		item['GBP_buy'] = float(re.sub("[A-Z]", "", hxs.xpath('//td[contains(text(), "GBP")]/../td[3]/text()').extract()[0]).strip())
		item['GBP_sell'] = float(re.sub("[A-Z]", "", hxs.xpath('//td[contains(text(), "GBP")]/../td[4]/text()').extract()[0]).strip())

		item['CHF_buy'] = float(re.sub("[A-Z]", "", hxs.xpath('//td[contains(text(), "CHF")]/../td[3]/text()').extract()[0]).strip())
		item['CHF_sell'] = float(re.sub("[A-Z]", "", hxs.xpath('//td[contains(text(), "CHF")]/../td[4]/text()').extract()[0]).strip())
		
		return [item]
		
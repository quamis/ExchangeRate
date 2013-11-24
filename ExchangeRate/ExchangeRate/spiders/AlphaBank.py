from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from ExchangeRate.items import ExchangerateItem


class AlphaBankSpider(BaseSpider):
	name = "AlphaBank"
	allowed_domains = ["www.alphabank.ro"]
	start_urls = [
		"https://www.alphabank.ro/ro/rate/rate_si_dobanzi.php",
	]

	def parse(self, response):
		hxs = Selector(response)
		item = ExchangerateItem()
		
		item['EUR_buy'] = float(hxs.xpath('//td[contains(text(), "(EUR)")][1]/..//td[5]/text()').extract()[0])
		item['EUR_sell'] = float(hxs.xpath('//td[contains(text(), "(EUR)")][1]/..//td[6]/text()').extract()[0])
		
		item['USD_buy'] = float(hxs.xpath('//td[contains(text(), "(USD)")][1]/..//td[5]/text()').extract()[0])
		item['USD_sell'] = float(hxs.xpath('//td[contains(text(), "(USD)")][1]/..//td[6]/text()').extract()[0])
		
		item['CHF_buy'] = float(hxs.xpath('//td[contains(text(), "(CHF)")][1]/..//td[5]/text()').extract()[0])
		item['CHF_sell'] = float(hxs.xpath('//td[contains(text(), "(CHF)")][1]/..//td[6]/text()').extract()[0])
		
		item['GBP_buy'] = float(hxs.xpath('//td[contains(text(), "(GBP)")][1]/..//td[5]/text()').extract()[0])
		item['GBP_sell'] = float(hxs.xpath('//td[contains(text(), "(GBP)")][1]/..//td[6]/text()').extract()[0])
		
		return [item]
		
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from ExchangeRate.items import ExchangerateItem


class TransilvaniaSpider(BaseSpider):
	name = "Transilvania"
	allowed_domains = ["bancatransilvania.ro"]
	start_urls = [
		"http://www.bancatransilvania.ro/curs-valutar-spot/",
	]

	def parse(self, response):
		hxs = Selector(response)
		item = ExchangerateItem()
		
		# EUR & USD are repeated 3 times in the whole page, pick the 2'nd one
        
        # //table[@class="cp"]//td/span[contains(text(), "USD")]/../../td[3]/text()
        
		item['EUR_buy'] = 	float(hxs.xpath('//table[@class="cp"]//td/span[contains(text(), "EUR")]/../../td[3]/text()').extract()[0].strip())
		item['EUR_sell'] = 	float(hxs.xpath('//table[@class="cp"]//td/span[contains(text(), "EUR")]/../../td[4]/text()').extract()[0].strip())
		
		item['USD_buy'] = 	float(hxs.xpath('//table[@class="cp"]//td/span[contains(text(), "USD")]/../../td[3]/text()').extract()[0].strip())
		item['USD_sell'] = 	float(hxs.xpath('//table[@class="cp"]//td/span[contains(text(), "USD")]/../../td[4]/text()').extract()[0].strip())
		
		item['GBP_buy'] = 	float(hxs.xpath('//table[@class="cp"]//td/span[contains(text(), "GBP")]/../../td[3]/text()').extract()[0].strip())
		item['GBP_sell'] = 	float(hxs.xpath('//table[@class="cp"]//td/span[contains(text(), "GBP")]/../../td[4]/text()').extract()[0].strip())

		item['CHF_buy'] = 	float(hxs.xpath('//table[@class="cp"]//td/span[contains(text(), "CHF")]/../../td[3]/text()').extract()[0].strip())
		item['CHF_sell'] = 	float(hxs.xpath('//table[@class="cp"]//td/span[contains(text(), "CHF")]/../../td[4]/text()').extract()[0].strip())
		
		return [item]
		
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from ExchangeRate.items import ExchangerateItem

class TransilvaniaSpider(BaseSpider):
	name = "Transilvania"
	allowed_domains = ["bancatransilvania.ro"]
	start_urls = [
		"http://www.bancatransilvania.ro/curs-valutar-spot/",
	]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = ExchangerateItem()
		# EUR & USD are repeated 3 times in the whole page, pick the 2'nd one
		
		item['EUR_buy'] = 	float(hxs.select('//*[@id="content"]//table[@class="cp"]//td[contains(text(), "EUR")]/../td[6]/text()').extract()[0].strip())
		item['EUR_sell'] = 	float(hxs.select('//*[@id="content"]//table[@class="cp"]//td[contains(text(), "EUR")]/../td[7]/text()').extract()[0].strip())
		
		item['USD_buy'] = 	float(hxs.select('//*[@id="content"]//table[@class="cp"]//td[contains(text(), "USD")]/../td[6]/text()').extract()[0].strip())
		item['USD_sell'] = 	float(hxs.select('//*[@id="content"]//table[@class="cp"]//td[contains(text(), "USD")]/../td[7]/text()').extract()[0].strip())
		
		item['GBP_buy'] = 	float(hxs.select('//*[@id="content"]//table[@class="cp"]//td[contains(text(), "GBP")]/../td[6]/text()').extract()[0].strip())
		item['GBP_sell'] = 	float(hxs.select('//*[@id="content"]//table[@class="cp"]//td[contains(text(), "GBP")]/../td[7]/text()').extract()[0].strip())

		item['CHF_buy'] = 	float(hxs.select('//*[@id="content"]//table[@class="cp"]//td[contains(text(), "CHF")]/../td[6]/text()').extract()[0].strip())
		item['CHF_sell'] = 	float(hxs.select('//*[@id="content"]//table[@class="cp"]//td[contains(text(), "CHF")]/../td[7]/text()').extract()[0].strip())
		
		return [item]
		
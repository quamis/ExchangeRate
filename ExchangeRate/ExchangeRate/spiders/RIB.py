from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from ExchangeRate.items import ExchangerateItem


class RIBSpider(BaseSpider):
	name = "RIB"
	allowed_domains = ["www.roib.ro"]
	start_urls = [
		"http://www.roib.ro/valuta.php",
	]

	def parse(self, response):
		hxs = Selector(response)
		item = ExchangerateItem()
		
		# EUR & USD are repeated 3 times in the whole page, pick the 2'nd one
		
		item['EUR_buy'] = float(hxs.xpath('//span[@class="titlu"]/../table//td[contains(text(), "EUR")]/../td[3]/text()').extract()[0].strip())
		item['EUR_sell'] = float(hxs.xpath('//span[@class="titlu"]/../table//td[contains(text(), "EUR")]/../td[5]/text()').extract()[0].strip())
		
		item['USD_buy'] = float(hxs.xpath('//span[@class="titlu"]/../table//td[contains(text(), "USD")]/../td[3]/text()').extract()[0].strip())
		item['USD_sell'] = float(hxs.xpath('//span[@class="titlu"]/../table//td[contains(text(), "USD")]/../td[5]/text()').extract()[0].strip())
		
		item['GBP_buy'] = float(hxs.xpath('//span[@class="titlu"]/../table//td[contains(text(), "GBP")]/../td[3]/text()').extract()[0].strip())
		item['GBP_sell'] = float(hxs.xpath('//span[@class="titlu"]/../table//td[contains(text(), "GBP")]/../td[5]/text()').extract()[0].strip())

		# CHF are repeated 3 times in the whole page, pick the 2'nd one
		item['CHF_buy'] = float(hxs.xpath('//span[@class="titlu"]/../table//td[contains(text(), "CHF")]/../td[3]/text()').extract()[0].strip())
		item['CHF_sell'] = float(hxs.xpath('//span[@class="titlu"]/../table//td[contains(text(), "CHF")]/../td[5]/text()').extract()[0].strip())
		
		return [item]
		
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from ExchangeRate.items import ExchangerateItem

class RIBSpider(BaseSpider):
	name = "RIB"
	allowed_domains = ["www.roib.ro"]
	start_urls = [
		"http://www.roib.ro/valuta.php",
	]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = ExchangerateItem()
		# EUR & USD are repeated 3 times in the whole page, pick the 2'nd one
		item['EUR_buy'] = float(hxs.select('//td[contains(text(), "EUR")][5]/../td[3]/text()').extract()[0].strip())
		item['EUR_sell'] = float(hxs.select('//td[contains(text(), "EUR")][5]/../td[5]/text()').extract()[0].strip())
		
		item['USD_buy'] = float(hxs.select('//td[contains(text(), "USD")][5]/../td[3]/text()').extract()[0].strip())
		item['USD_sell'] = float(hxs.select('//td[contains(text(), "USD")][5]/../td[5]/text()').extract()[0].strip())
		
		item['GBP_buy'] = float(hxs.select('//td[contains(text(), "GBP")][5]/../td[3]/text()').extract()[0].strip())
		item['GBP_sell'] = float(hxs.select('//td[contains(text(), "GBP")][5]/../td[5]/text()').extract()[0].strip())

		# CHF are repeated 3 times in the whole page, pick the 2'nd one
		item['CHF_buy'] = float(hxs.select('//td[contains(text(), "CHF")][2]/../td[3]/text()').extract()[0].strip())
		item['CHF_sell'] = float(hxs.select('//td[contains(text(), "CHF")][2]/../td[5]/text()').extract()[0].strip())
		
		return [item]
		
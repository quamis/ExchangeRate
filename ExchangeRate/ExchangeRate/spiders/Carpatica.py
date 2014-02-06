from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from ExchangeRate.items import ExchangerateItem
import re

class CarpaticaSpider(BaseSpider):
	name = "Carpatica"
	allowed_domains = ["www.carpatica.ro"]
	start_urls = [
		"http://www.carpatica.ro/index.php?option=com_content&view=article&id=291&Itemid=366&lang=ro",
	]

	def parse(self, response):
		hxs = Selector(response)
		item = ExchangerateItem()
		
		item['EUR_buy'] = float(re.sub(",", ".", hxs.xpath('//*[@id="s5_bodygradientnoin"]//td/span[contains(text(), "EURO")]/../../td[5]/text()').extract()[0]).strip())
		item['EUR_sell'] = float(re.sub(",", ".", hxs.xpath('//*[@id="s5_bodygradientnoin"]//td/span[contains(text(), "EURO")]/../../td[4]/text()').extract()[0]).strip())
		
		item['USD_buy'] = float(re.sub(",", ".", hxs.xpath('//*[@id="s5_bodygradientnoin"]//td/span[contains(text(), "USD")]/../../td[5]/text()').extract()[0]).strip())
		item['USD_sell'] = float(re.sub(",", ".", hxs.xpath('//*[@id="s5_bodygradientnoin"]//td/span[contains(text(), "USD")]/../../td[4]/text()').extract()[0]).strip())
		
		item['GBP_buy'] = float(re.sub(",", ".", hxs.xpath('//*[@id="s5_bodygradientnoin"]//td/span[contains(text(), "GBP")]/../../td[5]/text()').extract()[0]).strip())
		item['GBP_sell'] = float(re.sub(",", ".", hxs.xpath('//*[@id="s5_bodygradientnoin"]//td/span[contains(text(), "GBP")]/../../td[4]/text()').extract()[0]).strip())

		item['CHF_buy'] = float(re.sub(",", ".", hxs.xpath('//*[@id="s5_bodygradientnoin"]//td/span[contains(text(), "CHF")]/../../td[5]/text()').extract()[0]).strip())
		item['CHF_sell'] = float(re.sub(",", ".", hxs.xpath('//*[@id="s5_bodygradientnoin"]//td/span[contains(text(), "CHF")]/../../td[4]/text()').extract()[0]).strip())
		
		return [item]
		
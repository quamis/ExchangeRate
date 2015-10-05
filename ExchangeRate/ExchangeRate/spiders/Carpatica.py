from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from ExchangeRate.items import ExchangerateItem
import re

class CarpaticaSpider(BaseSpider):
	name = "Carpatica"
	allowed_domains = ["www.carpatica.ro"]
	start_urls = [
		"https://www.carpatica.ro/curs-valutar/",
	]

	def parse(self, response):
		hxs = Selector(response)
		item = ExchangerateItem()
        # //table[contains(@class, "table_custom_carp")]//td[contains(text(), "1 EUR")]/../td[3]/text()
		item['EUR_buy'] = float(re.sub(",", ".", hxs.xpath('//table[contains(@class, "table_custom_carp")]//td[contains(text(), "1 EUR")]/../td[3]/text()').extract()[0]).strip())
		item['EUR_sell'] = float(re.sub(",", ".", hxs.xpath('//table[contains(@class, "table_custom_carp")]//td[contains(text(), "1 EUR")]/../td[4]/text()').extract()[0]).strip())
		
		item['USD_buy'] = float(re.sub(",", ".", hxs.xpath('//table[contains(@class, "table_custom_carp")]//td[contains(text(), "1 USD")]/../td[3]/text()').extract()[0]).strip())
		item['USD_sell'] = float(re.sub(",", ".", hxs.xpath('//table[contains(@class, "table_custom_carp")]//td[contains(text(), "1 USD")]/../td[4]/text()').extract()[0]).strip())
		
		item['GBP_buy'] = float(re.sub(",", ".", hxs.xpath('//table[contains(@class, "table_custom_carp")]//td[contains(text(), "1 GBP")]/../td[3]/text()').extract()[0]).strip())
		item['GBP_sell'] = float(re.sub(",", ".", hxs.xpath('//table[contains(@class, "table_custom_carp")]//td[contains(text(), "1 GBP")]/../td[4]/text()').extract()[0]).strip())

		item['CHF_buy'] = float(re.sub(",", ".", hxs.xpath('//table[contains(@class, "table_custom_carp")]//td[contains(text(), "1 CHF")]/../td[3]/text()').extract()[0]).strip())
		item['CHF_sell'] = float(re.sub(",", ".", hxs.xpath('//table[contains(@class, "table_custom_carp")]//td[contains(text(), "1 CHF")]/../td[4]/text()').extract()[0]).strip())
		
		return [item]
		
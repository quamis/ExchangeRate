from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from ExchangeRate.items import ExchangerateItem
import re

class OTPSpider(BaseSpider):
	name = "OTP"
	allowed_domains = ["www.otpbank.ro"]
	start_urls = [
		"https://persoanefizice.otpbank.ro/ro/curs-valutar",
	]

	def parse(self, response):
		hxs = Selector(response)
		item = ExchangerateItem()
		
		# //table[@id="tabelcurs"]//td[contains(text(), "EUR")][1]/../td[4]/text()
		item['EUR_buy'] =  float(hxs.xpath('//table[@id="tabelcurs"]//td[contains(text(), "EUR")][1]/../td[3]/text()').extract()[0])
		item['EUR_sell'] = float(hxs.xpath('//table[@id="tabelcurs"]//td[contains(text(), "EUR")][1]/../td[4]/text()').extract()[0])
		
		item['USD_buy'] =  float(hxs.xpath('//table[@id="tabelcurs"]//td[contains(text(), "USD")][1]/../td[3]/text()').extract()[0])
		item['USD_sell'] = float(hxs.xpath('//table[@id="tabelcurs"]//td[contains(text(), "USD")][1]/../td[4]/text()').extract()[0])
		
		item['GBP_buy'] =  float(hxs.xpath('//table[@id="tabelcurs"]//td[contains(text(), "GBP")][1]/../td[3]/text()').extract()[0])
		item['GBP_sell'] = float(hxs.xpath('//table[@id="tabelcurs"]//td[contains(text(), "GBP")][1]/../td[4]/text()').extract()[0])

		item['CHF_buy'] =  float(hxs.xpath('//table[@id="tabelcurs"]//td[contains(text(), "CHF")][1]/../td[3]/text()').extract()[0])
		item['CHF_sell'] = float(hxs.xpath('//table[@id="tabelcurs"]//td[contains(text(), "CHF")][1]/../td[4]/text()').extract()[0])
		
		return [item]
		
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from ExchangeRate.items import ExchangerateItem
import re

class OTPSpider(BaseSpider):
	name = "OTP"
	allowed_domains = ["www.otpbank.ro"]
	start_urls = [
		"http://www.otpbank.ro/ro/curs-valutar.html",
	]

	def parse(self, response):
		hxs = Selector(response)
		item = ExchangerateItem()
		
		# EUR & USD are repeated 3 times in the whole page, pick the 2'nd one
		item['EUR_buy'] =  float(hxs.xpath('//table[@class="data-default"]//td/strong[contains(text(), "EUR")]/../../td[2]/strong/text()').extract()[0])
		item['EUR_sell'] = float(hxs.xpath('//table[@class="data-default"]//td/strong[contains(text(), "EUR")]/../../td[3]/strong/text()').extract()[0])
		
		#                                  //table[@class="data-default"]//td/strong[contains(text(), "USD")]
		item['USD_buy'] =  float(hxs.xpath('//table[@class="data-default"]//td/strong[contains(text(), "USD")]/../../td[2]/strong/text()').extract()[0])
		item['USD_sell'] = float(hxs.xpath('//table[@class="data-default"]//td/strong[contains(text(), "USD")]/../../td[3]/strong/text()').extract()[0])
		
		item['GBP_buy'] =  float(hxs.xpath('//table[@class="data-default"]//td/strong[contains(text(), "GBP")]/../../td[2]/strong/text()').extract()[0])
		item['GBP_sell'] = float(hxs.xpath('//table[@class="data-default"]//td/strong[contains(text(), "GBP")]/../../td[3]/strong/text()').extract()[0])

		item['CHF_buy'] =  float(hxs.xpath('//table[@class="data-default"]//td/strong[contains(text(), "CHF")]/../../td[2]/strong/text()').extract()[0])
		item['CHF_sell'] = float(hxs.xpath('//table[@class="data-default"]//td/strong[contains(text(), "CHF")]/../../td[3]/strong/text()').extract()[0])
		
		return [item]
		
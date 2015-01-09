from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from ExchangeRate.items import ExchangerateItem


class INGSpider(BaseSpider):
	name = "ING"
	allowed_domains = ["www.ing.ro"]
	start_urls = [
		"http://www.ing.ro/ing/curs-valutar.html",
	]

	def parse(self, response):
		hxs = Selector(response)
		item = ExchangerateItem()
		
		# //div[@id="wrapper"]//div[@class="leftsider"][contains(text(), "EUR")]
		# //div[@id="wrapper"]//div[@class="liner"]/div[@class="leftsider"][contains(text(), "EUR")]
		# //div[@id="wrapper"]//div[@class="liner"]//img[contains(@src, "AUD")]
		# //div[@id="wrapper"]//div[@class="liner"]//img[contains(@src, "AUD")]/../../div[2]/text()	  <-- works!!
		
		# //div[@id="wrapper"]//div[contains(@class, "tabbertab")][2]//div[@class="liner"]//img[contains(@src, "/AUD")]/../../div[2]/text()
		
		item['EUR_buy'] = float(hxs.xpath('//div[@id="wrapper"]//div[contains(@class, "tabbertab")][2]//div[@class="liner"]//img[contains(@src, "/EUR")]/../../div[2]/text()').extract()[0].strip())
		item['EUR_sell'] = float(hxs.xpath('//div[@id="wrapper"]//div[contains(@class, "tabbertab")][1]//div[@class="liner"]//img[contains(@src, "/EUR")]/../../div[2]/text()').extract()[0].strip())
		
		item['USD_buy'] = float(hxs.xpath('//div[@id="wrapper"]//div[contains(@class, "tabbertab")][2]//div[@class="liner"]//img[contains(@src, "/USD")]/../../div[2]/text()').extract()[0].strip())
		item['USD_sell'] = float(hxs.xpath('//div[@id="wrapper"]//div[contains(@class, "tabbertab")][1]//div[@class="liner"]//img[contains(@src, "/USD")]/../../div[2]/text()').extract()[0].strip())
		
		item['GBP_buy'] = float(hxs.xpath('//div[@id="wrapper"]//div[contains(@class, "tabbertab")][2]//div[@class="liner"]//img[contains(@src, "/GBP")]/../../div[2]/text()').extract()[0].strip())
		item['GBP_sell'] = float(hxs.xpath('//div[@id="wrapper"]//div[contains(@class, "tabbertab")][1]//div[@class="liner"]//img[contains(@src, "/GBP")]/../../div[2]/text()').extract()[0].strip())
		
		item['CHF_buy'] = float(hxs.xpath('//div[@id="wrapper"]//div[contains(@class, "tabbertab")][2]//div[@class="liner"]//img[contains(@src, "/CHF")]/../../div[2]/text()').extract()[0].strip())
		item['CHF_sell'] = float(hxs.xpath('//div[@id="wrapper"]//div[contains(@class, "tabbertab")][1]//div[@class="liner"]//img[contains(@src, "/CHF")]/../../div[2]/text()').extract()[0].strip())

		return [item]
		
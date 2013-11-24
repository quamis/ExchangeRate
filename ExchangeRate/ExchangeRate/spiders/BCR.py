from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from ExchangeRate.items import ExchangerateItem

class BCRSpider(BaseSpider):
	name = "BCR"
	allowed_domains = ["www.bcr.ro"]
	start_urls = [
		"http://www.bcr.ro/ro/curs-valutar",
	]

	def parse(self, response):
		hxs = Selector(response)
		item = ExchangerateItem()
		
		item['EUR_buy'] = float(hxs.xpath('//div[@id="main0BCRExchange_ratesOverview"]//td[contains(text(), "EURO")]/../td[3]/text()').extract()[0].strip().replace(",", "."))
		item['EUR_sell'] = float(hxs.xpath('//div[@id="main0BCRExchange_ratesOverview"]//td[contains(text(), "EURO")]/../td[4]/text()').extract()[0].strip().replace(",", "."))
		
		item['USD_buy'] = float(hxs.xpath('//div[@id="main0BCRExchange_ratesOverview"]//td[contains(text(), "DOLAR SUA")]/../td[3]/text()').extract()[0].strip().replace(",", "."))
		item['USD_sell'] = float(hxs.xpath('//div[@id="main0BCRExchange_ratesOverview"]//td[contains(text(), "DOLAR SUA")]/../td[4]/text()').extract()[0].strip().replace(",", "."))
		
		item['GBP_buy'] = float(hxs.xpath('//div[@id="main0BCRExchange_ratesOverview"]//td[contains(text(), "LIRA STERLINA")]/../td[3]/text()').extract()[0].strip().replace(",", "."))
		item['GBP_sell'] = float(hxs.xpath('//div[@id="main0BCRExchange_ratesOverview"]//td[contains(text(), "LIRA STERLINA")]/../td[4]/text()').extract()[0].strip().replace(",", "."))
		
		item['CHF_buy'] = float(hxs.xpath('//div[@id="main0BCRExchange_ratesOverview"]//td[contains(text(), "FRANC ELVETIAN")]/../td[3]/text()').extract()[0].strip().replace(",", "."))
		item['CHF_sell'] = float(hxs.xpath('//div[@id="main0BCRExchange_ratesOverview"]//td[contains(text(), "FRANC ELVETIAN")]/../td[4]/text()').extract()[0].strip().replace(",", "."))
		
		return [item]
		
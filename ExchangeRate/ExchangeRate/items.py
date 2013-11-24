# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ExchangerateItem(Item):
    # define the fields for your item here like:
    # name = Field()
	EUR_buy = Field()
	EUR_sell = Field()
	USD_buy = Field()
	USD_sell = Field()
	CHF_buy = Field()
	CHF_sell = Field()
	GBP_buy = Field()
	GBP_sell = Field()

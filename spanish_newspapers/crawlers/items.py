# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class ScrapyEditorialItem(scrapy.Item):
	title = scrapy.Field()
	subtitle = scrapy.Field()
	url = scrapy.Field()
	text = scrapy.Field()
	last_updated = scrapy.Field()
	published = scrapy.Field()
	tags = scrapy.Field()

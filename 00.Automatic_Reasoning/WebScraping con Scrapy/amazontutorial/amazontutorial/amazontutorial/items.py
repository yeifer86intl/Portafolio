# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazontutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_name = scrapy.Field()
    customers_number=scrapy.Field()
    customers_points=scrapy.Field()
    img_link = scrapy.Field()
    product_link = scrapy.Field()
    price_whole = scrapy.Field()
    pass

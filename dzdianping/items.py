# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy import Item, Field


class DzdianpingItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    stars = Field()
    average_score = Field()
    average_price = Field()
    taste_score = Field()
    environment_score = Field()
    service_score = Field()
    address = Field()
    tel = Field()
    glat = Field()
    glng = Field()
    shopId = Field()
    city = Field()



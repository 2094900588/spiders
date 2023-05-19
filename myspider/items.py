# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field() # 标题
    articleId = scrapy.Field() # id
    pubDate = scrapy.Field() #公告时间
    districtName = scrapy.Field() # 地级名称



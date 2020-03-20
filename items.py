# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NaverNews(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    content=scrapy.Field()
    pub_date=scrapy.Field()
    url=scrapy.Field()
    publisher=scrapy.Field()
    
    def __repr__(self):
        p=NaverNews(self)
        if len(p['content'])>100:
                 p['content']=p['content'][:100]+'...'
   
        return super(NaverNews,p).__repr__()
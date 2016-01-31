# -*- coding: utf-8 -*-

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

class LeboncoinItem(Item):
    doc_id = Field()
    doc_url = Field()
    
    title = Field()
    desc = Field()
    c = Field()
    
    img_urls = Field()
    thumb_urls = Field()
    
    user_url = Field()
    user_id = Field()
    user_name = Field()

    upload_date = Field()
    upload_epoch = Field()
    
    check_date = Field()
    check_epoch = Field()

    urgent = Field()

    region = Field()
    addr_locality = Field()
    location = Field()

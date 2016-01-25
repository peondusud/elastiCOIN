# -*- coding: utf-8 -*-

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

class LeboncoinItem(Item):
    doc_id = Field()
    doc_url = Field()
    doc_category = Field()
    title = Field()
    img_urls = Field()
    thumb_urls = Field()
    user_url = Field()
    user_id = Field()
    user_name = Field()
    user_pro = Field()
    user_pro_siren = Field()

    upload_date = Field()
    check_date = Field()

    price_currency = Field()
    price = Field()
    urgent = Field()

    region = Field()
    addr_locality = Field()
    postal_code = Field()
    latitude = Field()
    longitude = Field()
    location = Field()

    criterias = Field()

    desc = Field()

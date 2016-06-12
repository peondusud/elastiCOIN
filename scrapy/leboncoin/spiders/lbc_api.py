#1 -*- coding: utf-8 -*-

import scrapy
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from leboncoin.items import LeboncoinItem
from scrapy.loader.processors import TakeFirst
from urlparse import urlparse, parse_qs
from datetime import date, datetime
from collections import OrderedDict
import logging
import time
import re


class LbcSpider(scrapy.Spider):
    name = "lbc_api"
    allowed_domains = ["leboncoin.fr"]
    DATE_FORMAT = "%Y.%m.%d"
    TIME_FORMAT = "%H:%M:%S"
    EPOCH_FORMAT = "%s"
    DATETIME_FORMAT = u" ".join((DATE_FORMAT, TIME_FORMAT))


    # start_urls = ( )

    def __init__(self, *args, **kwargs):
        super(LbcSpider, self).__init__(*args, **kwargs)
        self._api_key = "d2c84cdd525dddd7cbcc0d0a86609982c2c59e22eb01ee4202245b7b187f49f1546e5f027d48b8d130d9aa918b29e991c029f732f4f8930fc56dbea67c5118ce"
        self._app_id = "leboncoin_android"
        self._user_agent = "fr.leboncoin.android , Genymotion Custom Phone - 4.4.4 - API 19 - 768x1280 , 4.4.4"
        self._body = OrderedDict((('app_id', self._app_id),
                                 ('key', self._api_key) ))
        self._body_urlencoded = self.encode_params(self._body)
        self._headers = {'User-Agent': self._user_agent}
        self._list_url = "https://mobile.leboncoin.fr/templates/api/list.json"
        self._view_url = "https://mobile.leboncoin.fr/templates/api/view.json"
        self._pivot = "0,0,0"
        self._params = OrderedDict((('ca', "12_s"),   # 2_s=bordeaux 12_s = ile de france  13_s=languedoc 16_s = midipyrn
                                  # ('zipcode', ",".join(map(str, [75000]))),
                                  # ('city',  ",".join(['Paris'])),
                                  ('w', 1),     # 1=departementvoisin region  2= 3=toute la france 275=paris 278=yvelines
                                  # ('c', 8),   # 8=immo 9=ventesimmo 14=multimedia 18=maison 24=loisirs 56=matpro
                                  ('f', 'a'),   # a=all c=company p=private
                                  # ('ur', 1),  # urgent flag
                                  ('o', 1),     # page offset
                                  ('q', "boulez"),  # query
                                  ('sp', 0),    # sp = sort, 0 = date, 1 = price
                                  ('pivot', self._pivot)  # paging_last
                                  ))

    
    def start_requests(self):
        url =  self._list_url + "?ca=12_s&w=1&f=a&o=1&q=&sp=0&pivot=0,0,0"
        yield scrapy.Request(url,
                            method="POST",
                            body=self._body_urlencoded,
                            headers=self._headers,
                            callback=self.parse)


    def encode_params(self, params):
        params_str = "&".join("%s=%s" % (k, v) for k, v in params.items() if v is not None)
        return params_str


    def parse(self, response):
        self.logger.debug("response.url", response.url)
        print dir(response)
        #raise CloseSpider('End - Done') #must close spider
        #self.logger.debug("Wait to close spider nb doc left", self.nb_doc)
        yield scrapy.Request(self._view_url,
                            method="POST",
                            body=self._body_urlencoded,
                            headers=self._headers,
                            callback=self.parse_adview)
       
        url = self._list_url + "?" + self.encode_params(self._params)
        yield scrapy.Request(self._list_url,
                            method="POST",
                            body=self._body_urlencoded,
                            headers=self._headers,
                            callback=self.parse)



    def parse_adview(self, response):
        lbc_ad = LeboncoinItem()
        self.logger.debug("page ",  response.url)


        return lbc_ad

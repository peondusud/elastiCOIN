# -*- coding: utf-8 -*-


import re
import time
import json
import logging
import collections
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from scrapy.exceptions import CloseSpider
from leboncoin.items import LeboncoinItem
from urllib.parse import urlparse, parse_qs
from datetime import date, datetime


class LbcSpider(scrapy.Spider):
    name = "lbc"
    allowed_domains = ["leboncoin.fr"]
    DATE_FORMAT = "%Y.%m.%d"
    TIME_FORMAT = "%H:%M:%S"
    EPOCH_FORMAT = "%s"
    DATETIME_FORMAT = u" ".join((DATE_FORMAT, TIME_FORMAT))

    start_urls = (
        'https://www.leboncoin.fr/_multimedia_/offres/ile_de_france/occasions/',
    )

    def __init__(self, *args, **kwargs):
        super(LbcSpider, self).__init__(*args, **kwargs)
        
       
        date_pattern = r'Mise en ligne le (?P<day>\d\d?) (?P<month>[a-zéû]+) . (?P<hour>\d\d?):(?P<minute>\d\d?)'
        self.date_regex = re.compile(date_pattern)
        
        doc_id_pattern = r"^http://www\.leboncoin\.fr/.{0,100}(?P<id>\d{9})\.htm.{0,50}$"
        self.doc_id_regex = re.compile(doc_id_pattern)
        
        uploader_id_pattern = r"^http.{0,50}(?P<id>\d{9,12})$"
        #uploader_id_pattern = r"^\/\/\w+\.leboncoin\.fr\/.{0,100}id=(?P<id>\d+).*?$"
        self.uploader_id_regex = re.compile(uploader_id_pattern)
        
        criteria_pattern = r'^\s*(\w+) : \"([\w\/]+)\",?'
        self.criteria_regex = re.compile(criteria_pattern, re.MULTILINE)
        
        places_pattern = r'var.*?=\s"([^\$]+?)";'
        self.places_regex = re.compile(places_pattern, re.MULTILINE)
        
        thumbs_pattern = r'^background-image: url\(\'(?P<url>[\w/:\.]+)\'\);$'
        self.thumb_regex = re.compile(thumbs_pattern)
        
        images_thumbs__pattern = r'images_thumbs\[\d\].*?=\s\"\/\/(.*?)\";'
        self.images_thumbs_regex = re.compile(images_thumbs__pattern, re.MULTILINE)
        
        images_pattern = r'images\[\d\].*?=\s\"\/\/(.*?)\";'
        self.images_pattern = re.compile(images_pattern, re.MULTILINE)
        
        page_offset_pattern = r"^http:\/\/www\.leboncoin\.fr\/.{0,100}\/\?o=(?P<offset>\d+).+$"
        self.page_offset_regex = re.compile(page_offset_pattern)
        
        self.nb_page = 0
        self.nb_doc = 0
        
        if kwargs.get('url'):
            self.start_urls = [kwargs.get('url')]
        self.logger.info("### Start URL: {}".format(self.start_urls))

    def parse(self, response):
        """
            parse multi 
        """
        self.logger.debug("response.url : {}".format(response.url))
        base = response.xpath('/html/body/section[@id="container"]/main[@id="main"]/section[@class="content-center"]/section[@id="listingAds"]/section[@class="list mainList tabs"]')
        ad_urls = base.xpath('section[@class="tabsContent block-white dontSwitch"]/ul//li/a/@href').extract()
        next_page_url = base.xpath('footer/div/div/a[@id="next"]/@href').extract_first()

        self.logger.debug("list of ad urls: {}".format(ad_urls))
        self.logger.debug("next page url: {}".format(next_page_url))
        while next_page_url is None:
            if self.nb_doc == 0:
                raise CloseSpider('End - Done')  # must close spider
            self.logger.debug("Wait to close spider nb doc left", self.nb_doc)
            time.sleep(1)
        for ad_url in ad_urls:
                self.nb_doc += 1
                yield scrapy.Request("http:" + ad_url, callback=self.parse_ad_page)
        self.nb_page += 1
       
    def parse_ad_page(self, response):
        lbc_ad = LeboncoinItem()
        
        lbc_ad['doc_url'] = response.url
        
        self.logger.debug( "ad_url, nb doc : {}\t\t{}".format( response.url, self.nb_doc))
        self.nb_doc -= 1  # decrement cnt usefull for stop spider
        
        lbc_ad['upload_date'] = "2017.01.20 20:00:00"
        lbc_ad['c'] = {"listid": "019595649745588" }
        
        
        self.logger.debug( "lbc_ad : {}".format(lbc_ad))
        yield lbc_ad
        
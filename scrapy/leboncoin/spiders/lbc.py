# -*- coding: utf-8 -*-


import re
import time
import json
import logging
import collections
import scrapy
import pprint
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
        base_xpath = '/html/body/section[@id="container"]/main[@id="main"]/section[@class="content-center"]/section[@id="listingAds"]/section[@class="list mainList tabs"]'
        base = response.xpath(base_xpath)
        
        ad_urls_xpath = 'section[@class="tabsContent block-white dontSwitch"]/ul//li/a/@href'
        ad_urls = base.xpath(ad_urls_xpath).extract()
        
        next_page_url_xpath = 'footer/div/div/a[@id="next"]/@href'
        next_page_url = base.xpath(next_page_url_xpath).extract_first()

        self.logger.debug("list of ad urls: {}".format(ad_urls))
        self.logger.debug("next page url: {}".format(next_page_url))
        
        while next_page_url is None:
            if self.nb_doc == 0:
                raise CloseSpider('End - Done')  # must close spider
            self.logger.debug("Wait to close spider nb doc left", self.nb_doc)
            time.sleep(0.5)
        for ad_url in ad_urls:
                self.nb_doc += 1
                yield scrapy.Request("https:" + ad_url, callback=self.parse_ad_page)
        
        #req next page
        self.nb_page += 1
        #yield scrapy.Request("http:" + next_page_url, callback=self.parse)
       
    def parse_ad_page(self, response):
        """
            parse ad view page
        """
        ad_base_xpath = '/html/body/section[@id="container"]/main/section[@class="content-center"]/section[@id="adview"]'
        ad_base = response.xpath(ad_base_xpath)
        ad_base2 = ad_base.xpath('section/section/section[@class="properties lineNegative"]')
        
        title = ad_base.xpath('section/header/h1/text()').extract_first()
        utag_data = response.xpath('/html/body/script[4]/text()').extract()
        
        images = ad_base.xpath('section/section/script[2]/text()').extract_first()
        if images is None:
          images = response.xpath('//*[@class="item_image big popin-open trackable"]/@data-popin-content').extract_first()

        places = ad_base.xpath('aside/div/script/text()').extract_first()
        date_str = ad_base2.xpath('p/text()').extract_first()
        
        check_date = datetime.now()
        user_name = ad_base2.xpath('div[@class="line line_pro noborder"]/p/a/text()').extract_first()
        description = ad_base2.xpath('div[@class="line properties_description"]/p[@itemprop="description"]/text()').extract()
        
        is_phonenumber = response.xpath('boolean(count(//button[@class="button-orange large phoneNumber trackable"]))').extract_first()
        
       
        lbc_ad = {}
        lbc_ad['doc_url'] = response.url        
        lbc_ad['title'] = title        
        lbc_ad['description'] = description
        lbc_ad['criterias'] = utag_data
        lbc_ad['images'] = images
        lbc_ad['user_name'] = user_name
        lbc_ad['places'] = places
        lbc_ad['date'] = date_str
        lbc_ad['check_date'] = check_date
        lbc_ad['is_phonenumber'] = is_phonenumber
        

        #pprint.pprint(lbc_ad)
        
        
        
        self.logger.debug( "ad_url, nb doc : {}\t\t{}".format( response.url, self.nb_doc))
        self.nb_doc -= 1  # decrement cnt usefull for stop spider
        
        
        lbc_ad = LeboncoinItem()
        lbc_ad['doc_url'] = response.url 
        lbc_ad['upload_date'] = "2017.01.20 20:00:00"
        lbc_ad['c'] = { "listid": "019595649745588" }
        
        
        self.logger.debug( "lbc_ad : {}".format(lbc_ad))
        yield lbc_ad
        
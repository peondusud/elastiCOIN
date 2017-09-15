# -*- coding: utf-8 -*-

import re
import time
import json
import logging
import collections
import scrapy
import pprint
import locale
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from scrapy.exceptions import CloseSpider
from leboncoin.items import LeboncoinItem
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import dateparser


class LbcAd():
    DATE_FORMAT = "%Y.%m.%d"
    TIME_FORMAT = "%H:%M:%S"
    EPOCH_FORMAT = "%s"
    DATETIME_FORMAT = u" ".join((DATE_FORMAT, TIME_FORMAT))

    def __init__(self, logger):
        self.logger = logger

        uploader_id_pattern = r"^http.{0,50}(?P<id>\d{9,12})$"
        #uploader_id_pattern = r"^\/\/\w+\.leboncoin\.fr\/.{0,100}id=(?P<id>\d+).*?$"
        self.uploader_id_regex = re.compile(uploader_id_pattern)

        criterias_pattern = r'^\s*(\w+) : \"([\w\/]+)\",?'
        self.criterias_regex = re.compile(criterias_pattern, re.MULTILINE)

        places_pattern = r'^\s+var (\w+) = "(.*)";'
        self.places_regex = re.compile(places_pattern, re.MULTILINE)

        img_thumbs_pattern = r'images_thumbs\[\d\].*?=\s\"\/\/(.*?)\";'
        self.img_thumbs_regex = re.compile(img_thumbs_pattern, re.MULTILINE)

        img_large_pattern = r'images\[\d\].*?=\s\"\/\/(.*?)\";'
        self.img_large_regex = re.compile(img_large_pattern , re.MULTILINE)

        # verify on linux : locale -a
        locale.setlocale(locale.LC_ALL, "fr_FR.utf8")


    def proper(self, raw_dic):
        proper_dic = {}
        proper_dic["ad_url"] = self.proper_url(raw_dic["ad_url"])

        proper_dic["title"] = raw_dic["title"].strip()

        proper_dic["description"] = self.proper_description(raw_dic["description"])

        criterias = self.proper_criterias(raw_dic["criterias"])
        proper_dic.update(criterias)

        upload_date = self.get_date(raw_dic["upload_date"])
        #proper_dic["upload_date"]  = upload_date
        proper_dic["upload_date"]  = upload_date.strftime(self.DATETIME_FORMAT)
        proper_dic["upload_epoch"] = upload_date.strftime(self.EPOCH_FORMAT)

        proper_dic["check_date"] = raw_dic["check_date"].strftime(self.DATETIME_FORMAT)
        proper_dic["check_epoch"] = raw_dic["check_date"].strftime(self.EPOCH_FORMAT)

        img_thumbs_urls = self.proper_img_thumbs_urls(raw_dic["images"])
        img_large_urls = self.proper_img_large_urls(raw_dic["images"])


        tmp = dict(re.findall(self.places_regex, raw_dic["places"]))
        proper_dic["location"] = self.get_geopoint(tmp['lng'], tmp['lat'])
        proper_dic["uploader_id"] = tmp['adreplyLink'].split('id=')[1]
        del tmp

        del raw_dic
        self.logger.debug( "proper_dic : {}".format(proper_dic))
        return proper_dic

    def proper_url(self, url):
        """
          remove = "?ca=12_s" frm url
        """
        #return url.split('?')[0]
        return url[:-8]

    def proper_criterias(self, criterias):
        d = dict(re.findall(self.criterias_regex, criterias))
        # environnement key always eq "prod" so useless
        d.pop("environnement", None)
        # ad_search key always eq "ad_search" so useless
        d.pop("previouspage", None)
        return d

    def proper_description(self, desc):
        s = u"\n".join(desc)
        s = s.strip()
        return s

    def get_date(self, raw_date):
        now = datetime.now()
        #print(":".join("{:02x}".format(ord(c)) for c in raw_date))
        s = raw_date.replace('\u00e0', '')
        #s = raw_date.replace('\xe0', '')
        #d = datetime.strptime(s, "Mise en ligne le %d %B  %H:%M")
        d = dateparser.parse(s, date_formats=['Mise en ligne le %d %B  %H:%M'], languages=['fr'])
        d = d.replace(year=now.year)
        # Prevent to have ads in future date
        # Example if parsed in january with ad date in december
        if d > now:
              # set to previous year
             d = d.replace(year=now.year-1)
        return d

    def proper_img_large_urls(self, string):
        if string is None:
            return None
        img_urls = re.findall(self.img_large_regex, string)
        return img_urls

    def proper_img_thumbs_urls(self, string):
        if string is None:
            return None
        thumb_urls = re.findall(self.img_thumbs_regex, string)
        return thumb_urls

    def get_geopoint(self, lng, lat):
        lon = lng.strip()
        lat = lat.strip()
        location = None
        if lon != "":
            location = [float(lon), float(lat)]
        return location


class LbcSpider(scrapy.Spider):
    name = "lbc"
    allowed_domains = ["leboncoin.fr"]
    start_urls = ('https://www.leboncoin.fr/annonces/offres/', )

    def __init__(self, *args, **kwargs):
        super(LbcSpider, self).__init__(*args, **kwargs)

        self.lbcAd = LbcAd(self.logger)

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

        while next_page_url is None and ad_urls is None:
            if self.nb_doc == 0:
                raise CloseSpider('End - Done')  # must close spider
            self.logger.debug("Wait to close spider nb doc left: {}".format(self.nb_doc))
            time.sleep(0.5)
        for ad_url in ad_urls:
                self.nb_doc += 1
                ad_view_url = "https:" + ad_url
                self.logger.info( "ad_view_url : {}".format(ad_view_url))
                yield scrapy.Request(ad_view_url, callback=self.parse_ad_page)
        if next_page_url is not None:
            #req next page
            self.nb_page += 1
            yield scrapy.Request("http:" + next_page_url, callback=self.parse)

    def parse_ad_page(self, response):
        """
            parse ad view page
        """
        ad_base_xpath = '/html/body/section[@id="container"]/main/section[@class="content-center"]/section[@id="adview"]'
        ad_base = response.xpath(ad_base_xpath)
        ad_base2 = ad_base.xpath('section/section/section[@class="properties lineNegative"]')

        title = ad_base.xpath('section/header/h1/text()').extract_first()
        utag_data = response.xpath('/html/body/script[4]/text()').extract_first()

        images = ad_base.xpath('section/section/script[2]/text()').extract_first()
        if images is None:
          images = response.xpath('//*[@class="item_image big popin-open trackable"]/@data-popin-content').extract_first()

        places = ad_base.xpath('aside/div/script/text()').extract_first()
        date_str = ad_base2.xpath('p/text()').extract_first()

        check_date = datetime.now()
        user_name = ad_base2.xpath('div[@class="line line_pro noborder"]/p/a/text()').extract_first()
        description = ad_base2.xpath('div[@class="line properties_description"]/p[@itemprop="description"]/text()').extract()

        is_phonenumber = response.xpath('boolean(count(//button[@class="button-orange large phoneNumber trackable"]))').extract_first()

        #lbc_ad = LeboncoinItem()
        lbc_ad = {}
        lbc_ad['ad_url'] = response.url
        lbc_ad['title'] = title
        lbc_ad['description'] = description
        lbc_ad['criterias'] = utag_data
        lbc_ad['images'] = images
        lbc_ad['user_name'] = user_name
        lbc_ad['places'] = places
        lbc_ad['upload_date'] = date_str
        lbc_ad['check_date'] = check_date
        lbc_ad['is_phonenumber'] = is_phonenumber


        self.logger.debug( "ad_url, nb doc : {}\t\t{}".format( response.url, self.nb_doc))
        self.nb_doc -= 1  # decrement cnt usefull for stop spider


        self.logger.debug( "lbc_ad : {}".format(lbc_ad))
        yield self.lbcAd.proper(lbc_ad)

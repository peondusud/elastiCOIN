# -*- coding: utf-8 -*-

import re
import locale
import dateparser
from datetime import datetime
from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from scrapy.exceptions import CloseSpider


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
        self.img_large_regex = re.compile(img_large_pattern, re.MULTILINE)

        # verify on linux : locale -a
        locale.setlocale(locale.LC_ALL, "fr_FR.utf8")

    def proper(self, raw_dic):
        proper_dic = {}
        proper_dic["ad_url"] = self.proper_url(raw_dic["ad_url"])

        proper_dic["title"] = raw_dic["title"].strip()

        proper_dic["description"] = self.proper_description(
            raw_dic["description"])

        criterias = self.proper_criterias(raw_dic["criterias"])
        proper_dic.update(criterias)

        upload_date = self.get_date(raw_dic["upload_date"])
        #proper_dic["upload_date"]  = upload_date
        proper_dic["upload_date"] = upload_date.strftime(self.DATETIME_FORMAT)
        proper_dic["upload_epoch"] = upload_date.strftime(self.EPOCH_FORMAT)

        proper_dic["check_date"] = raw_dic["check_date"].strftime(
            self.DATETIME_FORMAT)
        proper_dic["check_epoch"] = raw_dic["check_date"].strftime(
            self.EPOCH_FORMAT)

        img_thumbs_urls = self.proper_img_thumbs_urls(raw_dic["images"])
        img_large_urls = self.proper_img_large_urls(raw_dic["images"])

        tmp = dict(re.findall(self.places_regex, raw_dic["places"]))
        proper_dic["location"] = self.get_geopoint(tmp['lng'], tmp['lat'])
        proper_dic["uploader_id"] = tmp['adreplyLink'].split('id=')[1]
        del tmp

        del raw_dic
        self.logger.debug("proper_dic : {}".format(proper_dic))
        return proper_dic

    def proper_url(self, url):
        """
          remove = "?ca=12_s" frm url
        """
        # return url.split('?')[0]
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
        #s = raw_date.replace(u'Mise en ligne le ', '')
        s = raw_date[17:]
        #s = raw_date.replace('\u00e0', '')
        d = dateparser.parse(
            s, date_formats=[u'%d %B à %H:%M'],
            languages=['fr'],
            settings={'PREFER_DATES_FROM': 'past'})
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

class LeboncoinItem(Item):
    ad_id = Field()
    ad_url = Field()

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

    urg = Field()
    premium = Field()


    region = Field()
    addr_locality = Field()
    location = Field()

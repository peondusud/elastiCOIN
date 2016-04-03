#1 -*- coding: utf-8 -*-

import scrapy
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from leboncoin.items import LeboncoinItem
from scrapy.loader.processors import TakeFirst
from urlparse import urlparse, parse_qs
from datetime import date, datetime
import logging
import time
import re


class LbcSpider(scrapy.Spider):
    name = "lbc"
    allowed_domains = ["leboncoin.fr"]
    DATE_FORMAT = "%Y.%m.%d"
    TIME_FORMAT = "%H:%M:%S"
    EPOCH_FORMAT = "%s"
    DATETIME_FORMAT = u" ".join((DATE_FORMAT, TIME_FORMAT))


    start_urls = (
        #'http://www.leboncoin.fr/annonces/offres/ile_de_france/occasions/', #all ads
        #'http://www.leboncoin.fr/voitures/offres/ile_de_france/occasions/',
        #'http://www.leboncoin.fr/ventes_immobilieres/offres/ile_de_france/',
        'http://www.leboncoin.fr/_multimedia_/offres/ile_de_france/occasions/',
        #'http://www.leboncoin.fr/informatique/offres/ile_de_france/occasions/',
        #'http://www.leboncoin.fr/image_son/offres/ile_de_france/occasions/',
        #'http://www.leboncoin.fr/ameublement/offres/ile_de_france/occasions/',
        #'http://www.leboncoin.fr/electromenager/offres/ile_de_france/occasions/',
    )

    def __init__(self, *args, **kwargs):
        self.thumb_pattern = re.compile(ur'^background-image: url\(\'(?P<url>[\w/:\.]+)\'\);$')
        self.date_pattern = re.compile(ur'Mise en ligne le (?P<day>\d\d?) (?P<month>[a-zéû]+) . (?P<hour>\d\d?):(?P<minute>\d\d?)')
        self.doc_id_pattern = re.compile(ur"^http://www\.leboncoin\.fr/.{0,100}(?P<id>\d{9})\.htm.{0,50}$")
        self.uploader_id_pattern = re.compile(ur"^http.{0,50}(?P<id>\d{9,12})$")
        self.uploader_id_regex = re.compile(ur"^\/\/\w+\.leboncoin\.fr\/.{0,100}id=(?P<id>\d+).*?$")
        self.criteria_pattern = re.compile(ur'^\s{2}(?P<key>\w+) : "(?P<val>\w+)",?', re.MULTILINE)
        self.places_pattern = re.compile(ur'var.*?=\s*([^\$]+?);', re.MULTILINE)
        self.images_thumbs_pattern = re.compile(ur'images_thumbs\[\d\].*?=\s*(.*?);')
        self.images_pattern = re.compile(ur'images\[\d\].*?=\s*(.*?);', re.MULTILINE)
        self.page_offset_regex = re.compile(ur"^http:\/\/www\.leboncoin\.fr\/.{0,100}\/\?o=(?P<offset>\d+).+$")
        self.nb_page = 0
        self.nb_doc = 0
        self.takeFirst = TakeFirst()
        super(LbcSpider, self).__init__(*args, **kwargs)


    def parse(self, response):
       self.logger.debug("response.url", response.url)
       base = response.xpath('/html/body/section[@id="container"]/main/section/section[@id="listingAds"]/section[@class="list mainList tabs"]')
       urls = base.xpath('ul//li/a/@href').extract()
       next_page_url = None
       try:
           next_page_url = base.xpath('footer/div/div/a[@id="next"]/@href').extract()[0]
       except IndexError:
           pass

       if next_page_url is None:
           while True:
               if self.nb_doc == 0:
                   raise CloseSpider('End - Done') #must close spider
               self.logger.debug("Wait to close spider nb doc left", self.nb_doc)
               time.sleep(1)
       else:
          for doc_url in urls:
              self.nb_doc += 1
              yield scrapy.Request("http:" + doc_url, callback=self.parse_page)
       self.nb_page += 1
       yield scrapy.Request("http:" + next_page_url, callback=self.parse)


    def proper_url(self, url):
        """
        remove = "?ca=12_s" frm url
        """
        #return url.split('?')[0]
        return url[:-8]

    def offset_url_page_regex(self, url):
        m = re.search(self.page_offset_regex, url)
        if m is not None:
            url_page_offset = m.group('offset')
        else:
            url_page_offset = 1
        return int(url_page_offset)

    def get_url_page_offset_urlparse(self, url):
        url_parsed = urlparse(url)
        query_string = url_parsed.query
        offset_str = parse_qs(query_string).get('o', '1')
        offset = int(offset_str[-1]) #string trick
        return offset

    def offset_url_page_split(self, url):
         offset_str = url.split("?o=")[-1].split('&')
         offset = int(offset_str[0])
         return offset_str

    def get_doc_id(self, url):
        self.logger.debug(url)
        parse_result = urlparse(url)
        tmp = parse_result.path
        tmp = tmp.split("/")[-1]
        id = tmp.split(".htm")[0]
        return int(id)

    def get_id_regex(self, url):
        #pattern = r"(\d{9})"
        m = re.search(self.doc_id_pattern, url)
        if m is not None:
            return int(m.group('id'))
        return None

    def get_uploader_id(self, url):
        parse_result = urlparse(url)
        tmp = parse_result.query
        tmp = tmp.split("id=")[-1]
        return int(tmp)

    def get_uploader_id_regex(self, url):
        #m = re.search(self.uploader_id_pattern, url)
        m = re.search(self.uploader_id_regex, url)
        if m is not None:
            uploader_id = m.group('id')
            return int(uploader_id)
        return url

    def get_date(self, str):
        text = u''.join(str)
        t = re.search(self.date_pattern, text).groupdict()
        monthDict = {   u'janvier': 1,
                        u'février': 2,
                        u'mars': 3 ,
                        u'avril': 4,
                        u'mai': 5,
                        u'juin': 6,
                        u'juillet': 7,
                        u'août': 8,
                        u'septembre': 9,
                        u'octobre': 10,
                        u'novembre': 11,
                        u'décembre': 12  }
        if t is not None:
            for key, val in monthDict.items():
                if key == t['month']:
                    t['month'] = val
            now = date.today()
            year   = now.year
            month  = int(t['month'])
            day    = int(t['day'])
            hour   = int(t['hour'])
            minute = int(t['minute'])

            date_tmp = date(year, month, day)
            #Prevent to have ads in future date
            #Example if parsed in january with an ads date in december
            if date_tmp > now:
                #set previous year
                year -= 1
            d = datetime(year, month, day, hour, minute)
            return d
        return ''


    def find_imgs_urls(self, string):
        imgs_urls = re.findall(self.images_pattern, string)
        return imgs_urls

    def find_thumbs_urls(self, string):
        thumbs_urls = re.findall(self.images_thumbs_pattern, string)
        return thumbs_urls

    def get_geopoint(self, longitude, latitude):
        lon = longitude[1:-1]
        lat = latitude[1:-1]
        try:
            location = [float(lon), float(lat)]
        except ValueError:
            return None
        return location

    def jsVars_2_py(self, place):
        l =  re.findall(self.places_pattern, place)
        return l

    def jsVar_2_pyDic(self, criterias):
        d =  dict(re.findall(self.criteria_pattern,criterias))
        #environnement key always eq "prod" so useless
        d.pop("environnement", None)
        return d

    def proper_description(self, desc):
        str = u"\n".join(desc)
        str = str.strip()
        #str = str.replace("\n","")
        #str = str.replace("  ","")
        return str

    def parse_page(self, response):
       lbc_page = LeboncoinItem()
       self.logger.debug("page nb doc", self.nb_doc, response.url)
       lbc_page['doc_url'] = self.proper_url(response.url)

       base = response.xpath('/html/body/section[@id="container"]/main/section[@class="content-center"]/section[@id="adview"]')
       lbc_page['title'] = self.takeFirst(base.xpath('section/header/h1/text()').extract()).strip()
       #lbc_page['title'] = self.takeFirst(base.xpath('section[@class="adview_main"]/section[@class="carousel"]/div/@data-alt').extract())

       images = self.takeFirst(base.xpath('section/section/script/text()').extract())
       """
        images_thumbs[0] = "//img1.leboncoin.fr/thumbs/1ed/1ed739cec30cdd54a4459308aaf3c28acd7bdf76.jpg";
        images[0] = "//img1.leboncoin.fr/xxl/1ed/1ed739cec30cdd54a4459308aaf3c28acd7bdf76.jpg";
       """
       if images is not None:
           lbc_page['img_urls'] = self.find_imgs_urls(images)
           lbc_page['thumb_urls'] = self.find_thumbs_urls(images)

       #lbc_page['addr_locality'] =
       place_list = self.jsVars_2_py(self.takeFirst(base.xpath('aside/div/script/text()').extract()))
       
       """
         var apiKey = "54bb0281238b45a03f0ee695f73e704f";
         var lat = "48.85766 ";
         var lng = "2.38004 ";
       """
       apiKey = place_list[0]
       lat = place_list[1]
       lng =  place_list[2]
       lbc_page['location'] = self.get_geopoint(lng, lat)

       base2 = base.xpath('section/section/section[@class="properties lineNegative"]')

       date_text = base2.xpath('p/text()').extract()
       upload_date = self.get_date(date_text)
       lbc_page['upload_date'] = upload_date.strftime(self.DATETIME_FORMAT)
       lbc_page['upload_epoch'] = upload_date.strftime(self.EPOCH_FORMAT)
       check_date = datetime.now()
       lbc_page['check_date'] = check_date.strftime(self.DATETIME_FORMAT)
       lbc_page['check_epoch'] = check_date.strftime(self.EPOCH_FORMAT)

       lbc_page['user_name'] = self.takeFirst(base2.xpath('div[@class="line line_pro noborder"]/p/a/text()').extract())

       criterias = self.takeFirst(response.xpath('/html/body/script[1]/text()').extract())
       #lbc_page['c'] = self.jsVar_2_pyDic(criterias)
       lbc_page['c'] = criterias
       #print criterias

       description  = base2.xpath('div[@class="line properties_description"]/p[@itemprop="description"]/text()').extract()
       lbc_page['desc'] = self.proper_description(description)

       #TODO get phone

       self.nb_doc -= 1 #decrement cnt usefull for stop spider
       #print lbc_page
       return lbc_page

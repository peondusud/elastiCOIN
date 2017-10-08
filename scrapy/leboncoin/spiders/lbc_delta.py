# coding: utf-8


import re
import scrapy
import dateparser
from datetime import datetime, timedelta
from scrapy.loader.processors import TakeFirst
from scrapy.exceptions import CloseSpider
from leboncoin.items import LeboncoinItem, LbcAd
from urllib.parse import urlparse, parse_qs


class LbcSpider(scrapy.Spider):
    name = "lbc_delta"
    allowed_domains = ["leboncoin.fr"]
    start_urls = ('https://www.leboncoin.fr/annonces/offres/', )

    def __init__(self, *args, **kwargs):
        super(LbcSpider, self).__init__(*args, **kwargs)
        self.__now = datetime.now()
        self.lbcAd = LbcAd(self.logger)

        self.nb_page = 0
        self.nb_doc = 0

        if kwargs.get('url'):
            self.start_urls = [kwargs.get('url')]

        time_delta = kwargs.get('timedelta', "91d")
        if time_delta[-1:] == 'm':
            self.timedelta = timedelta(minutes=int(time_delta[:-1]))
        elif time_delta[-1:] == 'h':
            self.timedelta = timedelta(hours=int(time_delta[:-1]))
        elif time_delta[-1:] == 'd':
            self.timedelta = timedelta(days=int(time_delta[:-1]))

        self.pricemin = int(kwargs.get('pricemin', '0'))

        self.logger.info("### Start URL: {}".format(self.start_urls))

    def parse(self, response):
        """
            parse multi
        """
        self.logger.debug("response.url : {}".format(response.url))
        base_xpath = '/html/body/section[@id="container"]/main[@id="main"]/section[@class="content-center"]/section[@id="listingAds"]/section[@class="list mainList tabs"]'
        base = response.xpath(base_xpath)

        #ad_urls_xpath = 'section[@class="tabsContent block-white dontSwitch"]/ul//li/a/@href'
        ads_xpath = 'section[@class="tabsContent block-white dontSwitch"]/ul//li/a'
        ads = base.xpath(ads_xpath)

        next_page_url_xpath = 'footer/div/div/a[@id="next"]/@href'
        next_page_url = base.xpath(next_page_url_xpath).extract_first()

        self.logger.debug("list of ads: {}".format(ads))
        self.logger.debug("next page url: {}".format(next_page_url))

        while next_page_url is None and ad_urls is None:
            if self.nb_doc == 0:
                raise CloseSpider('End - Done')  # must close spider
            self.logger.debug(
                "Wait to close spider nb doc left: {}".format(self.nb_doc))
            time.sleep(0.5)

        for ad in ads:
            ad_date = ad.xpath(
                'section/aside/p[@class="item_supp"]/text()').extract()
            self.logger.debug("ad_date: {}".format(ad_date))
            ad_date = "".join(ad_date).strip()
            self.logger.debug("ad_date: {}".format(ad_date))
            ad_price = ad.xpath('section/h3/@content').extract_first()
            if ad_price is None:
                ad_price = 0
            self.logger.debug("ad_price: {}".format(ad_price))
            ad_date_p = dateparser.parse(ad_date,
                                         date_formats=[
                                             u'%d %B, %H:%M', u'%d %B à %H:%M'],
                                         languages=['fr'],
                                         settings={'PREFER_DATES_FROM': 'past'})
            if ad_date_p >= self.__now - self.timedelta and int(ad_price) >= self.pricemin:

                self.nb_doc += 1
                ad_view_url = "https:" + ad.xpath('@href').extract_first()
                self.logger.debug("ad_view_url : {}".format(ad_view_url))
                yield scrapy.Request(ad_view_url, callback=self.parse_ad_page)
        if next_page_url is not None:
            # req next page
            self.nb_page += 1
            yield scrapy.Request("http:" + next_page_url, callback=self.parse)

    def parse_ad_page(self, response):
        """
            parse ad view page
        """
        ad_base_xpath = '/html/body/section[@id="container"]/main/section[@class="content-center"]/section[@id="adview"]'
        ad_base = response.xpath(ad_base_xpath)
        ad_base2 = ad_base.xpath(
            'section/section/section[@class="properties lineNegative"]')

        title = ad_base.xpath('section/header/h1/text()').extract_first()
        utag_data = response.xpath(
            '/html/body/script[4]/text()').extract_first()

        images = ad_base.xpath(
            'section/section/script[2]/text()').extract_first()
        if images is None:
            images = response.xpath(
                '//*[@class="item_image big popin-open trackable"]/@data-popin-content').extract_first()

        places = ad_base.xpath('aside/div/script/text()').extract_first()
        date_str = ad_base2.xpath('p/text()').extract_first()

        check_date = datetime.now()
        user_name = ad_base2.xpath(
            'div[@class="line line_pro noborder"]/p/a/text()').extract_first()
        description = ad_base2.xpath(
            'div[@class="line properties_description"]/p[@itemprop="description"]/text()').extract()

        is_phonenumber = response.xpath(
            'boolean(count(//button[@class="button-orange large phoneNumber trackable"]))').extract_first()

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

        self.logger.debug("ad_url, nb doc : {}\t\t{}".format(
            response.url, self.nb_doc))
        self.nb_doc -= 1  # decrement cnt usefull for stop spider

        self.logger.debug("lbc_ad : {}".format(lbc_ad))
        yield self.lbcAd.proper(lbc_ad)

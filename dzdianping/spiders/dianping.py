# -*- coding: utf-8 -*-
import json

from scrapy import Request, Spider
from dzdianping.items import DzdianpingItem
import re


class DianpingSpider(Spider):
    name = 'dianping'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/']

    request_url = 'http://www.dianping.com/search/category/{city}/10'
    shop_link = 'http://www.dianping.com/ajax/json/shopfood/wizard/BasicHideInfoAjaxFP?&shopId={shop_id}'


    def start_requests(self):
        for i in range(1, 2310):
            yield Request(self.request_url.format(city=i), callback=self.food_url)

    def food_url(self, response):
        try:
            urls = response.xpath('.//div[@id="classfy"]//a//@href').extract()
            for url in urls:
                yield Request(url, self.region_url)
        except NameError:
            self.logger.debug('No Any Shop')


    def region_url(self, response):
        urls = response.xpath('.//div[@id="region-nav"]//a//@href').extract()
        for url in urls:
            yield Request(url, self.url_index)

    def url_index(self, response):
        try:
            urls = response.xpath('.//div[@id="region-nav-sub"]//a//@href').extract()[1:]
            for url in urls:
                yield Request(url, self.shoplist_url)
        except:
            yield Request(response.url, self.shoplist_url)

    def shoplist_url(self, response):
        try:
            page = response.xpath('.//div[@class="page"]//a//text()').extract()[-2]
        except:
            page = 1
        for s in range(int(page)):
            url = response.url + 'p' + str(s)
            yield Request(url, self.shop_url)

    def shop_url(self, response):
        urls = response.xpath('.//a[@data-hippo-type="shop"]').re('href="(.*?)"')
        city = response.xpath('.//a[@class="city J-city"]//span//text()').extract_first()
        for url in urls:
            shop_id = re.search('shop/(\d+)', url).group(1)
            yield Request(self.shop_link.format(shop_id=shop_id), self.parse_index, meta={'city': city})


    def parse_index(self, response):
        results = json.loads(response.text)
        dianping_item = DzdianpingItem()
        if 'msg' in results.keys():
            name = results.get('msg').get('shopInfo').get('shopName')
            stars = results.get('msg').get('shopInfo').get('shopPower')/10
            average_price = results.get('msg').get('shopInfo').get('avgPrice')
            average_score = results.get('msg').get('shopInfo').get('score')
            taste_score = results.get('msg').get('shopInfo').get('score1')
            environment_score = results.get('msg').get('shopInfo').get('score2')
            service_score = results.get('msg').get('shopInfo').get('score3')
            address = results.get('msg').get('shopInfo').get('address')
            city = response.meta['city']
            tel = results.get('msg').get('shopInfo').get('phoneNo')
            glat = results.get('msg').get('shopInfo').get('glat')
            glng = results.get('msg').get('shopInfo').get('glng')
            shopId = results.get('msg').get('shopInfo').get('shopId')
            for field in dianping_item.fields:
                try:
                    dianping_item[field] = eval(field)
                except NameError:
                    self.logger.debug('Field is Not Defined: ' + field)
            yield dianping_item

    # def parse_index(self, response):
    #     name = response.xpath('.//h1[@class="shop-name"]//text()').extract_first().strip()
    #     stars = response.xpath('.//div[@class="brief-info"]//span[1]').re_first('title="(.*?)"')
    #     review_count = response.xpath('.//div[@class="brief-info"]//span[2]//text()').extract_first()
    #     average_price = response.xpath('.//div[@class="brief-info"]//span[3]//text()').re_first('人均:(.*?)元')
    #     taste_score = response.xpath('.//span[@id="comment_score"]//span[1]//text()').extract_first()
    #     environment_score = response.xpath('.//span[@id="comment_score"]//span[2]//text()').extract_first()
    #     service_score = response.xpath('.//span[@id="comment_score"]//span[3]//text()').extract_first()
    #     address = response.xpath('.//div[@itemprop="street-address"]//span[2]//text()').extract_first().strip()
    #     tel = response.xpath('.//p[@class="expand-info tel"]//span[2]//text()').extract_first()
    #     summary = response.xpath('.//*[@id="summaryfilter-wrapper"]/div[1]/div[2]/span[1]/a').extract()
    #     coordinate = response.xpath('//*[@id="map"]/img').extract_first()
    #     print(name, stars, review_count, average_price, taste_score, environment_score, service_score, address,
    #           tel, summary, coordinate)
    #     dianping_item = DzdianpingItem()
    #     for field in dianping_item.fields:
    #         try:
    #             dianping_item[field] = eval(field)
    #         except NameError:
    #             self.logger.debug('Field is Not Defined: ' + field)
    #     yield dianping_item

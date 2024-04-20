import numpy as np
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CrawlSpider_site(CrawlSpider):
    name = 'Worker'
    allowed_domains = ['vnexpress.net']
    start_urls = ['https://vnexpress.net/']
    rules = [Rule(LinkExtractor(allow=['vnexpress.net/.+'],
                                    deny_domains=['shop.vnexpress.net',
                                                'raovat.vnexpress.net']),
                    callback='parse_article', follow=True)]
    def extractor(self, response):
        print('Got a response from {}'.format(response.url))
        content = response.xpath('//body[@data-source="Detail"]')
        if content:
            content.text
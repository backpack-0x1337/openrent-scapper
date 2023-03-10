import datetime
import os

import scrapy
import re

class OpenRentSpider(scrapy.Spider):
    name = 'openrent'
    current_id = 1601200
    total_property = 180000
    max_id = current_id + total_property
    base_url = 'https://www.openrent.co.uk/'
    start_url = base_url + str(current_id)
    start_urls = [start_url]
    handle_httpstatus_list = [404, 429]
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'AUTOTHROTTLE_ENABLED': False,
        'RANDOMIZE_DOWNLOAD_DELAY': False,
        'FEEDS': {
            'openrent-p.csv': {
                'format': 'csv',
                'overwrite': True
            }
        }
    }

    def isLetAgreed(self, response):
        if response.css('div.alert.alert-warning.mt-1') != "":
            return False
        return True

    def parse(self, response):
        #response.css('strong::text').getall()[4],
        try:
            if response.status != 404 and not response.xpath("//div[@class='alert alert-warning mt-1']/p/text()").extract():

                yield {
                    'link': response.url,

                    'title': response.css('h1.property-title::text').get(),
                    "property_id": self.current_id,
                    'postcode-L1': response.css('h1.property-title::text').get().split(' ')[-1],
                    'postcode-L2': response.xpath("///td/a/@href").extract()[0].split('%')[1],
                    'price-monthly': response.css('h3.price-title::text').getall()[0].replace('£', ''),
                    'bed': response.xpath("//td/strong/text()").extract()[0],
                    'bath': response.xpath("//td/strong/text()").extract()[1],
                    'max-tenants': response.xpath("//td/strong/text()").extract()[2],
                    # 'price-per-Occu.': int(response.css('h3.price-title::text').getall()[0].replace('£', '')) / int(response.css('strong::text').getall()[4]),
                    'list-date': datetime.datetime.strptime(response.css('source').attrib['srcset'].split('mobile')[-1][0:8], '%d%m%Y').strftime('%Y%m%d'),
                    'let-agreed': "",
                    'Furnishing': response.xpath("//table[@class='table table-striped']//tr/td/text()").extract()[-2],
                    'EPC Rating': response.xpath("//table[@class='table table-striped']//tr/td/text()").extract()[-1]

                    # 'price-weekly': response.css('h3.price-title::text').getall()[1].replace('£', '')
                }
            elif response.xpath("//div[@class='alert alert-warning mt-1']/p/text()").extract():
                yield {
                    'link': response.url,
                    'title': response.css('h1.property-title::text').get(),
                    "property_id": self.current_id,
                    'postcode-L1': response.css('h1.property-title::text').get().split(' ')[-1],
                    'postcode-L2': response.xpath("///td/a/@href").extract()[0].split('%')[1],
                    'price-monthly': response.css('h3.price-title::text').getall()[0].replace('£', ''),
                    'bed': response.xpath("//td/strong/text()").extract()[0],
                    'bath': response.xpath("//td/strong/text()").extract()[1],
                    'max-tenants': response.xpath("//td/strong/text()").extract()[2],
                    'list-date': datetime.datetime.strptime(response.css('source').attrib['srcset'].split('mobile')[-1][0:8], '%d%m%Y').strftime('%Y%m%d'),
                    'let-agreed': datetime.datetime.strptime((re.search(r'\d{1,2}\s\w+\s\d{4}', response.xpath("//div[@class='alert alert-warning mt-1']/p/text()").extract()[0]).group()), '%d %B %Y').strftime('%Y%m%d'),
                    'Furnishing': response.xpath("//table[@class='table table-striped']//tr/td/text()").extract()[-2],
                    'EPC Rating': response.xpath("//table[@class='table table-striped']//tr/td/text()").extract()[-1]
                }
        except:
            yield {
                'link': 'error',
                'title': 'error',
                "property_id": 'error',
                'postcode': 'error',
                'price-monthly': 'error',
                'bed': 'error',
                'bath': 'error',
                'max-tenants': 'error',
                'list-date': 'error',
                'let-agreed': 'error',
                'Furnishing': 'error',
                'EPC Rating': 'error'
            }


        self.current_id += 1
        next_url = self.base_url + str(self.current_id)

        if self.current_id < self.max_id:
            yield scrapy.Request(next_url, callback=self.parse)

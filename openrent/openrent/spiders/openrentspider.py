import datetime
import os
from time import sleep

import scrapy
import re
import gspread

gc = gspread.service_account(filename='googleApi.json')

sh = gc.open('openrent-p').sheet1


def get_last_property_id():
    return sh.get_all_records()[-1].get('property_id')


class OpenRentSpider(scrapy.Spider):
    name = 'openrent'
    current_id = get_last_property_id() + 1
    total_property = 1800001
    max_id = current_id + total_property
    base_url = 'https://www.openrent.co.uk/'
    start_url = base_url + str(current_id)
    start_urls = [start_url]
    handle_httpstatus_list = [404, 429]

    end_of_deck_counter = 0
    custom_settings = {

        # 'DOWNLOAD_DELAY': 1,
        # 'AUTOTHROTTLE_ENABLED': False,
        # 'RANDOMIZE_DOWNLOAD_DELAY': False,
        'FEEDS': {
            'openrent-p.csv': {
                'format': 'csv',
                'overwrite': False
            }
        }
    }


    def parse(self, response):
        # response.css('strong::text').getall()[4],
        try:

            if response.status == 429:
                sleep(60)
                self.current_id -= 1

            elif response.status != 404 and not response.xpath(
                    "//div[@class='alert alert-warning mt-1']/p/text()").extract():
                self.end_of_deck_counter = 0

                sh.append_row([response.url, response.css('h1.property-title::text').get(), self.current_id,
                               response.css('h1.property-title::text').get().split(' ')[-1],
                               response.xpath("///td/a/@href").extract()[0].split('%')[1],
                               response.css('h3.price-title::text').getall()[0].replace('£', ''),
                               response.xpath("//td/strong/text()").extract()[0],
                               response.xpath("//td/strong/text()").extract()[1],
                               response.xpath("//td/strong/text()").extract()[2],
                               # 'price-per-Occu.': int(response.css('h3.price-title::text').getall()[0].replace('£', '')) / int(response.css('strong::text').getall()[4]),
                               datetime.datetime.strptime(
                                   response.css('source').attrib['srcset'].split('mobile')[-1][0:8], '%d%m%Y').strftime(
                                   '%Y%m%d'),
                               "",
                               response.xpath("//table[@class='table table-striped']//tr/td/text()").extract()[-2],
                               response.xpath("//table[@class='table table-striped']//tr/td/text()").extract()[-1]])
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
                    'list-date': datetime.datetime.strptime(
                        response.css('source').attrib['srcset'].split('mobile')[-1][0:8], '%d%m%Y').strftime('%Y%m%d'),
                    'let-agreed': "",
                    'Furnishing': response.xpath("//table[@class='table table-striped']//tr/td/text()").extract()[-2],
                    'EPC Rating': response.xpath("//table[@class='table table-striped']//tr/td/text()").extract()[-1]

                    # 'price-weekly': response.css('h3.price-title::text').getall()[1].replace('£', '')
                }
            elif response.xpath("//div[@class='alert alert-warning mt-1']/p/text()").extract():
                sh.append_row([response.url, response.css('h1.property-title::text').get(), self.current_id,
                               response.css('h1.property-title::text').get().split(' ')[-1],
                               response.xpath("///td/a/@href").extract()[0].split('%')[1],
                               response.css('h3.price-title::text').getall()[0].replace('£', ''),
                               response.xpath("//td/strong/text()").extract()[0],
                               response.xpath("//td/strong/text()").extract()[1],
                               response.xpath("//td/strong/text()").extract()[2],
                               # 'price-per-Occu.': int(response.css('h3.price-title::text').getall()[0].replace('£', '')) / int(response.css('strong::text').getall()[4]),
                               datetime.datetime.strptime(
                                   response.css('source').attrib['srcset'].split('mobile')[-1][0:8], '%d%m%Y').strftime(
                                   '%Y%m%d'),
                               datetime.datetime.strptime((re.search(r'\d{1,2}\s\w+\s\d{4}', response.xpath(
                                   "//div[@class='alert alert-warning mt-1']/p/text()").extract()[0]).group()),
                                                          '%d %B %Y').strftime('%Y%m%d'),
                               response.xpath("//table[@class='table table-striped']//tr/td/text()").extract()[-2],
                               response.xpath("//table[@class='table table-striped']//tr/td/text()").extract()[-1]])
                self.end_of_deck_counter = 0
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
                    'list-date': datetime.datetime.strptime(
                        response.css('source').attrib['srcset'].split('mobile')[-1][0:8], '%d%m%Y').strftime('%Y%m%d'),
                    'let-agreed': datetime.datetime.strptime((re.search(r'\d{1,2}\s\w+\s\d{4}', response.xpath(
                        "//div[@class='alert alert-warning mt-1']/p/text()").extract()[0]).group()),
                                                             '%d %B %Y').strftime('%Y%m%d'),
                    'Furnishing': response.xpath("//table[@class='table table-striped']//tr/td/text()").extract()[-2],
                    'EPC Rating': response.xpath("//table[@class='table table-striped']//tr/td/text()").extract()[-1]
                }
            elif response.status == 404:
                self.end_of_deck_counter += 1




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

        if self.end_of_deck_counter >= 30:
            rollback_url = self.base_url + str((self.current_id - self.end_of_deck_counter + 1))
            self.end_of_deck_counter = 0
            sleep(60 * 24)
            print('sleeping')
            yield scrapy.Request(rollback_url, callback=self.parse, dont_filter=True)

        elif self.current_id < self.max_id:
            yield scrapy.Request(next_url, callback=self.parse, dont_filter = True)

import datetime
import os
from time import sleep

import scrapy
import re
import gspread

gc = gspread.service_account(filename='googleApi.json')

sh = gc.open('openrent-p').sheet1


def get_update_list():
    todo_list = []
    records = sh.get_all_records()
    # get not rent out list
    for i in range(2, len(records)):
        if records[i]['let-agreed'] == '':
            todo_list.append(records[i])

    return todo_list


class OpenRentUpdateSpider(scrapy.Spider):
    name = 'OpenRentUpdateSpider'
    todo_list = get_update_list()
    start_urls = [todo_list[1]['link']]
    handle_httpstatus_list = [404, 429]
    counter = 1
    custom_settings = {

        # 'DOWNLOAD_DELAY': 1,
        # 'AUTOTHROTTLE_ENABLED': False,
        # 'RANDOMIZE_DOWNLOAD_DELAY': False,
        # 'FEEDS': {
        # 'openrent-p.csv': {
        #     'format': 'csv',
        #     'overwrite': False
        # }
        # }
    }

    def parse(self, response):
        # try:
            if self.counter >= len(self.todo_list) - 1:
                self.todo_list = get_update_list()
                self.counter = 1

            if response.status == 429:
                sleep(60)

            elif response.status != 404 and not response.xpath(
                    "//div[@class='alert alert-warning mt-1']/p/text()").extract():
                # do nothing
                self.counter += 1
                pass

            elif response.xpath("//div[@class='alert alert-warning mt-1']/p/text()").extract():
                # update let agree date
                letdate = datetime.datetime.strptime((re.search(r'\d{1,2}\s\w+\s\d{4}', response.xpath(
                              "//div[@class='alert alert-warning mt-1']/p/text()").extract()[0]).group()),'%d %B %Y').strftime('%Y%m%d')
                row = sh.find(str(self.todo_list[self.counter]['property_id'])).row
                sh.update_cell(row, 11, letdate)
                self.counter += 1

            elif response.status == 404:
                row = sh.find(str(self.todo_list[self.counter]['property_id'])).row
                sh.update_cell(row, 11, 'error')
                self.counter += 1

        # except:
        #     pass

            next_url = self.todo_list[self.counter]['link']
            yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)

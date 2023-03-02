from openrent.openrent.spiders.openrentspider import OpenRentSpider
from openrentupdatespider.openrentupdatespider.spiders.openrentupdatespider import OpenRentUpdateSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    setting = get_project_settings()
    process = CrawlerProcess(setting)
    process.crawl(OpenRentSpider)
    process.crawl(OpenRentUpdateSpider)
    process.start()


if __name__ == '__main__':
    main()

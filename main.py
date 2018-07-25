import scrapy

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scraper.jobbie.spiders.europe_remotely_spider import EuropeRemotelySpider
from scraper.jobbie.spiders.remotelist_io_spider import RemoteListIoSpider

results = []

def main():
    runSpiders()
    
def runSpiders():
    # set up spiders
    europe_remotely_spider = EuropeRemotelySpider()
    remotelis_io_spider = RemoteListIoSpider()

    # set up settings
    settings = get_project_settings()
    settings['ITEM_PIPELINES'] = {'__main__.SpidersPipeline': 1}

    # set up crawlers
    europe_remotely_crawler = Crawler(europe_remotely_spider, settings)
    europe_remotely_crawler.signals.connect(spiderClosed, signal=signals.spider_closed)

    #remotelis_io_crawler = Crawler(remotelis_io_spider, settings)
    #remotelis_io_crawler.signals.connect(spiderClosed, signal=signals.spider_closed)

    # start crawling
    europe_remotely_crawler.crawl()
    #remotelis_io_crawler.crawl()
    reactor.run()

def spiderClosed(spider):
    for result in results:
        print(result)

    reactor.stop()

class SpidersPipeline(object):
    def process_item(self, item, spider):
        results.append(dict(item))

if __name__ == '__main__':
    main()
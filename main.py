import json

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer

import api
import sqs_queue
import rss
from models import JobOffer
from scraper.jobbie.spiders.europe_remotely_spider import EuropeRemotelySpider
from scraper.jobbie.spiders.remotelist_io_spider import RemoteListIoSpider

results = []
SQS_QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/291634056833/job_offers"


def main():
    """ Runs collectors"""
    run_spiders_collector()
    run_apis_collector()
    run_rss_collector()

    print ("heyyyyo")
    for jobOffer in results:
        results_json = json.dumps(jobOffer.__dict__)
        print ("hey")
        sqs_queue.send_sqs_message(SQS_QUEUE_URL, results_json)


def run_apis_collector():
    """ Runs the API collectors and saves the collected job offers in the results object"""
    for item in api.get_from_github():
        results.append(item)

    for item in api.get_from_remote_ok():
        results.append(item)


def run_rss_collector():
    """ Runs the rss collectors and saves the collected job offers in the results object"""
    for item in rss.parse_stackoverflow():
        results.append(item)

    for item in rss.parse_we_work_remotely():
        results.append(item)


def run_spiders_collector():
    """ Runs the spider collectors and saves the collected job offers in the results object"""
    settings = get_project_settings()
    settings['ITEM_PIPELINES'] = {'__main__.SpidersPipeline': 1}
    runner = CrawlerRunner(settings)
    crawl(runner)
    reactor.run()


@defer.inlineCallbacks
def crawl(runner):
    yield runner.crawl(EuropeRemotelySpider)
    yield runner.crawl(RemoteListIoSpider)

    reactor.stop()


def process_item(item, spider):
    job_offer = JobOffer(item['url'], item['position'], "", item['company'], item['date'], item['tags'])
    results.append(job_offer)


if __name__ == '__main__':
    main()

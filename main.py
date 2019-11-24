import logging
import json

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer

import os
import api
import sqs_queue
import rss
from models import JobOffer
from scraper.jobbie.spiders.europe_remotely_spider import EuropeRemotelySpider

results = []
SQS_QUEUE_URL = os.environ['SQS_QUEUE_URL']
LOGGING_FILENAME = os.environ['LOGGING_FILENAME']
LOGGING_LEVEL = os.environ['LOGGING_LEVEL']


def main():
    """ Runs collectors"""
    setup_logging()

    run_spiders_collector()
    run_apis_collector()
    run_rss_collector()

    for job_offer in results:
        job_offer_json = json.dumps(job_offer.__dict__)
        sqs_queue.send_sqs_message(SQS_QUEUE_URL, job_offer_json)


def setup_logging():
    logging.basicConfig(filename=LOGGING_FILENAME, format='%(asctime)s %(levelname)s %(message)s', level=LOGGING_LEVEL)


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

    reactor.stop()


class SpidersPipeline(object):
    """ Pipeline to transform spiders results into JobOffer objects and save them into the results object"""

    @staticmethod
    def process_item(item, spider):
        job_offer = JobOffer(item['url'], item['position'], "", item['company'], item['date'], item['tags'])
        results.append(job_offer)


if __name__ == '__main__':
    main()

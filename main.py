import requests
import scrapy
import json

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scraper.jobbie.spiders.europe_remotely_spider import EuropeRemotelySpider
from scraper.jobbie.spiders.remotelist_io_spider import RemoteListIoSpider
from api import Github
from api import RemoteOk
from rss import Stackoverflow
from rss import WeWorkRemotely
from models import JobOffer

results = []

def main():
    """ Runs collectors"""
    runSpidersCollector()
    runApisCollector()
    runRsssCollector()

    headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
    for jobOffer in results:
        resultsJSON = json.dumps(jobOffer.__dict__)
        requests.post('http://127.0.0.1:5000/jobs', json = resultsJSON, headers = headers)

def runApisCollector():
    """ Runs the API collectors and saves the collected job offers in the results object"""
    github = Github()
    remoteOk = RemoteOk()
    
    for item in github.get():
        results.append(item)

    for item in remoteOk.get():
        results.append(item)

def runRsssCollector():
    """ Runs the rss collectors and saves the collected job offers in the results object"""
    stackOverflow = Stackoverflow()
    weWorkRemotely = WeWorkRemotely()

    for item in stackOverflow.parse():
        results.append(item)

    for item in weWorkRemotely.parse():
        results.append(item)
    
def runSpidersCollector():
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

class SpidersPipeline(object):
    """ Pipeline to transform spiders results into JobOffer objects and save them into the results object"""
    def process_item(self, item, spider):
        jobOffer = JobOffer(item['url'], item['position'], "", item['company'], item['date'], item['tags'])
        results.append(jobOffer)

if __name__ == '__main__':
    main()
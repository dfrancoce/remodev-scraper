import scrapy

from remodev.items import Job

class EuropeRemotelySpider(scrapy.Spider):
    name = "europeRemotely"

    def start_requests(self):
        urls = [
            'https://europeremotely.com/remote-jobs/Programming'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for item in response.css("ul.regular-jobs li"):
            job = Job()
            job["url"] = item.css("div.left a::attr(href)").extract_first()
            job["company"] = item.css("div.left span::text").extract_first()
            job["position"] = item.css("div.left a::text").extract_first()
            job["date"] = item.css("div.right::text").extract_first()
            job["tags"] = item.css("div.right a::text").extract()

            self.log('Job: %s' % job)
import scrapy

from settings import get_config
from ..items import Job


def create_job(url, company, position, date, tags):
    job = Job()

    job["url"] = url
    job["company"] = company
    job["position"] = position
    job["date"] = ''.join(date).strip()
    job["tags"] = tags

    return job


class EuropeRemotelySpider(scrapy.Spider):
    """ This class crawls the remote jobs in europeRemotely """

    name = "europeRemotely"

    def start_requests(self):
        config = get_config()
        url = config.get('spider').get('europeremotely')
        urls = [url]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        jobs = []

        for item in response.css("ul.sponsored-jobs li"):
            jobs.append(
                create_job(
                    item.css("div.job-row__left_column a::attr(href)").extract_first(),
                    item.css("div.job-row__right_column span.job-row__company::text").extract_first(),
                    item.css("div.job-row__left_column a::text").extract_first(),
                    item.css("div.job-row__right_column::text").extract(),
                    item.css("div.job-row__tags a::text").extract()
                )
            )

        for item in response.css("ul.regular-jobs li"):
            if item.css("li.expired").extract_first() is None:
                jobs.append(
                    create_job(
                        item.css("div.job-row__left_column a::attr(href)").extract_first(),
                        item.css("div.job-row__right_column span.job-row__company::text").extract_first(),
                        item.css("div.job-row__left_column a::text").extract_first(),
                        item.css("div.job-row__right_column::text").extract(),
                        item.css("div.job-row__tags a::text").extract()
                    )
                )
        
        return jobs

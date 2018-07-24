import feedparser
from models import JobOffer

class Stackoverflow(object):
    def parse(self):
        url = "https://stackoverflow.com/jobs/feed?l=Remote&u=Km&d=20"
        feed = feedparser.parse(url)

        jobOffers = []
        for entry in feed.entries:
            tags = self.extractTags(entry["tags"])
            jobOffer = JobOffer(entry["link"], entry["title"], entry["description"], entry["author"], entry["updated"], tags)
            jobOffers.append(jobOffer)
        
        return jobOffers

    def extractTags(self, tags):
        extractedTags = []
        for tag in tags:
            extractedTags.append(tag["term"])

        return extractedTags

class WeWorkRemotely(object):
    def parse(self):
        url = "https://weworkremotely.com/categories/remote-programming-jobs.rss"
        feed = feedparser.parse(url)

        jobOffers = []
        for entry in feed.entries:
            jobOffer = JobOffer(entry["link"], entry["title"], entry["summary"], entry["title"].split(":")[0], entry["published"], "")
            jobOffers.append(jobOffer)
        
        return jobOffers
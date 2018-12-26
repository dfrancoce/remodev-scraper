import feedparser
from models import JobOffer

class Stackoverflow(object):
    """ This class parses the response of the search for remote jobs in stackoverflow """
    
    def parse(self):
        """ Parses the results of the stackoverflow remote jobs search into a list of JobOffer objects """
        url = "https://stackoverflow.com/jobs/feed?l=Remote&u=Km&d=20"
        feed = feedparser.parse(url)

        job_offers = []
        for entry in feed.entries:
            if 'tags' in entry:
                tags = self.extractTags(entry["tags"])
                
            job_offer = JobOffer(entry["link"], entry["title"], entry["description"], entry["author"], entry["updated"], tags)
            job_offers.append(job_offer)
        
        return job_offers

    def extractTags(self, tags):
        extracted_tags = []
        for tag in tags:
            extracted_tags.append(tag["term"])

        return extracted_tags

class WeWorkRemotely(object):
    """ This class parses the response of the weworkremotely remote programming jobs rss feed """

    def parse(self):
        """ Parses the results of the weworkremotely remote programming jobs into a list of JobOffer objects """

        url = "https://weworkremotely.com/categories/remote-programming-jobs.rss"
        feed = feedparser.parse(url)

        job_offers = []
        for entry in feed.entries:
            job_offer = JobOffer(entry["link"], entry["title"], entry["summary"], entry["title"].split(":")[0], entry["published"], "")
            job_offers.append(job_offer)
        
        return job_offers
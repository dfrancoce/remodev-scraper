import feedparser
from domain.job_offer import JobOffer

def parse():
    stackoverflow_rss_url = "https://stackoverflow.com/jobs/feed?l=Remote&u=Km&d=20"
    feed = feedparser.parse(stackoverflow_rss_url)

    jobOffers = []
    for entry in feed.entries:
        jobOffer = JobOffer(entry["link"], entry["title"], entry["description"], "", entry["pubDate"], "")
        jobOffers.append(jobOffer)
    
    return jobOffers

def printJobOffers():
    jobOffers = parse()

    for jobOffer in jobOffers:
        print jobOffer.url + "|" + jobOffer.company + "|" + jobOffer.description + "|" + jobOffer.position

printJobOffers()
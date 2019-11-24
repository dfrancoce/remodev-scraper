import feedparser

from settings import get_config
from models import JobOffer


def parse_stackoverflow():
    """ Parses the results of the stackoverflow remote jobs search into a list of JobOffer objects """

    config = get_config()
    url = config.get('rss').get('stackoverflow')
    feed = feedparser.parse(url)

    job_offers = []
    for entry in feed.entries:
        tags = ""
        if 'tags' in entry:
            tags = extract_tags(entry["tags"])

        job_offer = JobOffer(entry["link"], entry["title"], entry["description"], entry["author"], entry["updated"],
                             tags)
        job_offers.append(job_offer)

    return job_offers


def extract_tags(tags):
    extracted_tags = []

    for tag in tags:
        extracted_tags.append(tag["term"])

    return extracted_tags


def parse_we_work_remotely():
    """ Parses the results of the weworkremotely remote programming jobs into a list of JobOffer objects """

    config = get_config()
    url = config.get('rss').get('weworkremotely')
    feed = feedparser.parse(url)

    job_offers = []
    for entry in feed.entries:
        job_offer = JobOffer(entry["link"], entry["title"], entry["summary"], entry["title"].split(":")[0],
                             entry["published"], "")
        job_offers.append(job_offer)

    return job_offers

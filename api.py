import requests
import json
import urllib

from models import JobOffer

class Github(object):
    def get(self):
        url = "https://jobs.github.com/positions.json?location=remote"
        ret = requests.get(url)
        jobOffersJson = json.loads(ret.content)

        jobOffers = []
        for job in jobOffersJson:
            jobOffer = JobOffer(job["url"], job["title"], job["description"], job["company"], job["created_at"], "")
            jobOffers.append(jobOffer)

        return jobOffers
        
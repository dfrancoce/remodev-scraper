import requests
import json
import urllib

from models import JobOffer

class Github(object):
    def get(self):
        url = "https://jobs.github.com/positions.json?location=remote"
        jobOffersJson = getContentAsJson(url)

        jobOffers = []
        for job in jobOffersJson:
            jobOffer = JobOffer(job["url"], job["title"], job["description"], job["company"], job["created_at"], "")
            jobOffers.append(jobOffer)

        return jobOffers

class RemoteOk(object):
    def get(self):
        url = "https://remoteok.io/api"
        jobOffersJson = getContentAsJson(url)

        jobOffers = []
        for job in jobOffersJson:
            if ('legal' in job):
                continue

            jobOffer = JobOffer(job["url"], job["position"], job["description"], job["company"], job["date"], job["tags"])
            jobOffers.append(jobOffer)

        return jobOffers

def getContentAsJson(url):
    ret = requests.get(url)
    return json.loads(ret.content)

import requests
import json
import urllib

from models import JobOffer

class Github(object):
    """ This class parses the response of the search for remote jobs in github """

    def get(self):
        """ Parses the github remote jobs API results into a list of JobOffer objects """
        url = "https://jobs.github.com/positions.json?location=remote"
        job_offers_json = getContentAsJson(url)

        job_offers = []
        for job in job_offers_json:
            job_offer = JobOffer(job["url"], job["title"], job["description"], job["company"], job["created_at"], "")
            job_offers.append(job_offer)

        return job_offers

class RemoteOk(object):
    """ This class parses the response of the search for remote jobs in remoteok """

    def get(self):
        """ Parses the remoteok jobs API results into a list of JobOffer objects """
        url = "https://remoteok.io/api"
        job_offers_json = getContentAsJson(url)

        job_offers = []
        for job in job_offers_json:
            if ('legal' in job):
                continue

            job_offer = JobOffer(job["url"], job["position"], job["description"], job["company"], job["date"], job["tags"])
            job_offers.append(job_offer)

        return job_offers

def getContentAsJson(url):
    ret = requests.get(url)
    return json.loads(ret.content)

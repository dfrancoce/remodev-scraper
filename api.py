import json

import requests

from settings import get_config
from models import JobOffer


def get_from_github():
    """ Parses the github remote jobs API results into a list of JobOffer objects """

    config = get_config()
    url = config.get('api').get('github')
    job_offers_json = get_content_as_json(url)

    job_offers = []
    for job in job_offers_json:
        job_offer = JobOffer(job["url"], job["title"], job["description"], job["company"], job["created_at"], "")
        job_offers.append(job_offer)

    return job_offers


def get_from_remote_ok():
    """ Parses the remoteok jobs API results into a list of JobOffer objects """

    config = get_config()
    url = config.get('api').get('remote_ok')
    job_offers_json = get_content_as_json(url)

    job_offers = []
    for job in job_offers_json:
        if 'legal' in job:
            continue

        job_offer = JobOffer(job["url"], job["position"], job["description"], job["company"], job["date"], job["tags"])
        job_offers.append(job_offer)

    return job_offers


def get_content_as_json(url):
    ret = requests.get(url)
    return json.loads(ret.content)

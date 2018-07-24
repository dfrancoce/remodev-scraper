import pytest
from rss import Stackoverflow, WeWorkRemotely

def test_stackoverflow_rss():
    stackoverflow = Stackoverflow()
    job_offers = stackoverflow.parse()

    assert len(job_offers) > 0

def test_weworkremotely_rss():
    weWorkRemotely = WeWorkRemotely()
    job_offers = weWorkRemotely.parse()

    assert len(job_offers) > 0

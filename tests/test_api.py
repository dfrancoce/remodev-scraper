import api


def test_github_api():
    job_offers = api.get_from_github()

    assert len(job_offers) > 0


def test_remote_ok_api():
    job_offers = api.get_from_remote_ok()

    assert len(job_offers) > 0

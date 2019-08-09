import rss


def test_stackoverflow_rss():
    job_offers = rss.parse_stackoverflow()

    assert len(job_offers) > 0


def test_we_work_remotely_rss():
    job_offers = rss.parse_we_work_remotely()

    assert len(job_offers) > 0

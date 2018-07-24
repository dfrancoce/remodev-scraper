import pytest
from api import Github, RemoteOk

def test_github_api():
    github = Github()
    job_offers = github.get()

    assert len(job_offers) > 0

def test_remoteOk_api():
    remoteOk = RemoteOk()
    job_offers = remoteOk.get()

    assert len(job_offers) > 0

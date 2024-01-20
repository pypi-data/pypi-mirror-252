import os

import pytest

COOKIE_PATH = "/tmp/kakuyomu_cookie"
from kakuyomu.utils.web import Client


def remove_cookie() -> None:
    if os.path.exists(COOKIE_PATH):
        os.remove(COOKIE_PATH)

@pytest.fixture
def login_client() -> Client:
    remove_cookie()
    client = Client(COOKIE_PATH)
    client.login()
    return client

@pytest.fixture
def logout_client() -> Client:
    remove_cookie()
    client = Client(COOKIE_PATH)
    return client

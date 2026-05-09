from http import HTTPStatus
from json import JSONDecodeError

import httpx
import pytest
from starlette.testclient import TestClient

from byparr.app import app
from byparr.schemas import SolveRequest

client = TestClient(app)

TEST_URLS = [
    "https://ext.to/",
    "https://extratorrent.st/",
    "https://speed.cd/login",
    'https://www.yggtorrent.top/engine/search?do=search&order=desc&sort=publish_date&name="UNESCAPED"+"DOUBLEQUOTES"&category=2145',
    "https://1337x.to/home/",
]


@pytest.mark.parametrize("url", TEST_URLS)
def test_challenge_bypass(url: str):
    preflight = httpx.get(url, timeout=10)
    if (
        preflight.status_code >= HTTPStatus.INTERNAL_SERVER_ERROR
        and "Just a moment..." not in preflight.text
    ):
        try:
            error_info = preflight.json()
        except JSONDecodeError:
            error_info = preflight.text
        pytest.skip(f"Skipping {url} - ({preflight.status_code}) {error_info}")

    response = client.post(
        "/v1",
        json=SolveRequest.model_construct(url=url, cmd="request.get").model_dump(),
    )
    if response.status_code == 408:
        pytest.skip(f"Challenge solving timed out for {url}")
    assert response.status_code == HTTPStatus.OK


def test_health_endpoint():
    response = client.get("/health")
    if response.status_code == 408:
        pytest.skip("Health check timed out accessing google.com")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "msg" in data
    assert "version" in data
    assert "userAgent" in data


def test_root_redirects_to_docs():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 301
    assert response.headers["location"] == "/docs"


def test_v1_response_structure():
    response = client.post(
        "/v1",
        json={"url": "https://example.com", "cmd": "request.get", "max_timeout": 60},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["status"] == "ok"
    assert "message" in data
    assert "solution" in data
    assert "startTimestamp" in data
    assert "endTimestamp" in data
    assert "version" in data
    solution = data["solution"]
    assert "url" in solution
    assert "status" in solution
    assert "cookies" in solution
    assert "userAgent" in solution
    assert "headers" in solution
    assert "response" in solution


def test_timeout_on_max_timeout_exceeded():
    response = client.post(
        "/v1",
        json={"url": "https://example.com", "cmd": "request.get", "max_timeout": 1},
    )
    if response.status_code == 408:
        detail = response.json()
        assert "detail" in detail
    else:
        assert response.status_code == HTTPStatus.OK

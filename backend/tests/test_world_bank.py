import pytest
import requests

from backend.world_bank import ResourceNotFoundError, WorldBankClient, WorldBankError


class FakeResponse:
    def __init__(self, payload, status_error=None):
        self.payload = payload
        self.status_error = status_error

    def raise_for_status(self):
        if self.status_error:
            raise self.status_error

    def json(self):
        return self.payload


class FakeSession:
    def __init__(self, response):
        self.response = response
        self.headers = {}
        self.last_timeout = None

    def get(self, _url, *, params, timeout):
        self.last_timeout = timeout
        return self.response


class QueueSession(FakeSession):
    def __init__(self, responses):
        super().__init__(None)
        self.responses = iter(responses)

    def get(self, _url, *, params, timeout):
        self.last_timeout = timeout
        return next(self.responses)


def test_client_uses_configured_timeout():
    session = FakeSession(FakeResponse([{}, []]))
    client = WorldBankClient(timeout=3.5, session=session)
    client.get_countries()
    assert session.last_timeout == 3.5


def test_http_failure_becomes_domain_error():
    response = FakeResponse([], requests.HTTPError("provider detail"))
    client = WorldBankClient(session=FakeSession(response))
    with pytest.raises(WorldBankError, match="unavailable"):
        client.get_countries()


def test_missing_country_has_specific_error():
    client = WorldBankClient(session=FakeSession(FakeResponse([{}, []])))
    with pytest.raises(ResourceNotFoundError):
        client.get_country_summary("ZZZ")


def test_countries_exclude_aggregates_and_are_sorted():
    payload = [
        {},
        [
            {
                "id": "USA",
                "name": "United States",
                "region": {"value": "North America"},
            },
            {"id": "WLD", "name": "World", "region": {"value": "Aggregates"}},
            {"id": "CRI", "name": "Costa Rica", "region": {"value": "Latin America"}},
        ],
    ]
    client = WorldBankClient(session=FakeSession(FakeResponse(payload)))
    assert [country["id"] for country in client.get_countries()] == ["CRI", "USA"]


def test_indicator_returns_latest_non_null_value():
    payload = [{}, [{"date": "2025", "value": None}, {"date": "2024", "value": 42}]]
    client = WorldBankClient(session=FakeSession(FakeResponse(payload)))
    assert client.get_indicator("CRI", "SP.POP.TOTL") == {
        "year": "2024",
        "value": 42,
    }


def test_summary_composes_all_indicators():
    country = FakeResponse([{}, [{"name": "Costa Rica"}]])
    indicator = FakeResponse([{}, [{"date": "2024", "value": 1}]])
    session = QueueSession([country, indicator, indicator, indicator, indicator])
    summary = WorldBankClient(session=session).get_country_summary("CRI")
    assert summary["country"] == "Costa Rica"
    assert set(summary) == {
        "country",
        "population",
        "gdp",
        "gdp_per_capita",
        "life_expectancy",
    }


def test_rejects_non_list_payload():
    client = WorldBankClient(session=FakeSession(FakeResponse({"error": "invalid"})))
    with pytest.raises(WorldBankError, match="unexpected"):
        client.get_countries()

from typing import Any

import pytest

from backend.app import create_app
from backend.services import CountryComparisonService
from backend.world_bank import ResourceNotFoundError, WorldBankError


class FakeGateway:
    def get_countries(self) -> list[dict[str, str]]:
        return [
            {"id": "CRI", "name": "Costa Rica"},
            {"id": "USA", "name": "United States"},
        ]

    def get_country_summary(self, country_code: str) -> dict[str, Any]:
        if country_code == "ZZZ":
            raise ResourceNotFoundError("Country ZZZ was not found")
        return {"country": country_code, "population": {"year": "2024", "value": 1}}


@pytest.fixture()
def client():
    app = create_app(
        {
            "TESTING": True,
        },
        CountryComparisonService(FakeGateway()),
    )
    return app.test_client()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
    assert response.headers["X-Content-Type-Options"] == "nosniff"


def test_lists_countries(client):
    response = client.get("/countries")
    assert response.status_code == 200
    assert response.get_json()[0]["id"] == "CRI"


@pytest.mark.parametrize(
    "query",
    ["", "?country1=CR&country2=USA", "?country1=CRI&country2=CRI"],
)
def test_rejects_invalid_comparisons(client, query):
    assert client.get(f"/compare{query}").status_code == 400


def test_compares_two_countries(client):
    response = client.get("/compare?country1=cri&country2=USA")
    assert response.status_code == 200
    assert response.get_json()["country1"]["country"] == "CRI"


def test_returns_404_for_unknown_country(client):
    response = client.get("/compare?country1=ZZZ&country2=USA")
    assert response.status_code == 404


def test_provider_errors_do_not_leak_details():
    class BrokenGateway(FakeGateway):
        def get_countries(self):
            raise WorldBankError("sensitive upstream details")

    app = create_app(
        {"TESTING": True},
        CountryComparisonService(BrokenGateway()),
    )
    response = app.test_client().get("/countries")
    assert response.status_code == 502
    assert "sensitive" not in response.get_data(as_text=True)

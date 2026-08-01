"""World Bank API adapter.

This module is the infrastructure boundary: application code depends on the
``WorldBankGateway`` protocol and not on ``requests`` directly.
"""

from __future__ import annotations

from typing import Any, Protocol

import requests

BASE_URL = "https://api.worldbank.org/v2"
INDICATORS = {
    "population": "SP.POP.TOTL",
    "gdp": "NY.GDP.MKTP.CD",
    "gdp_per_capita": "NY.GDP.PCAP.CD",
    "life_expectancy": "SP.DYN.LE00.IN",
}


class WorldBankError(RuntimeError):
    """Base exception for failures communicating with the data provider."""


class ResourceNotFoundError(WorldBankError):
    """Raised when a requested country does not exist."""


class WorldBankGateway(Protocol):
    """Port required by the application service."""

    def get_countries(self) -> list[dict[str, str]]: ...

    def get_country_summary(self, country_code: str) -> dict[str, Any]: ...


class WorldBankClient:
    """HTTP implementation of the World Bank gateway."""

    def __init__(
        self,
        base_url: str = BASE_URL,
        timeout: float = 10.0,
        session: requests.Session | None = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._session = session or requests.Session()
        self._session.headers.update({"User-Agent": "global-insights/1.0"})

    def _get_json(self, path: str, params: dict[str, Any]) -> list[Any]:
        try:
            response = self._session.get(
                f"{self._base_url}/{path.lstrip('/')}",
                params=params,
                timeout=self._timeout,
            )
            response.raise_for_status()
            payload = response.json()
        except (requests.RequestException, ValueError) as exc:
            raise WorldBankError("World Bank service is unavailable") from exc

        if not isinstance(payload, list):
            raise WorldBankError("World Bank returned an unexpected response")
        return payload

    def get_countries(self) -> list[dict[str, str]]:
        payload = self._get_json("country", {"format": "json", "per_page": 300})
        if len(payload) < 2 or not isinstance(payload[1], list):
            raise WorldBankError("World Bank returned an unexpected country list")

        countries = [
            {"id": country["id"], "name": country["name"]}
            for country in payload[1]
            if isinstance(country, dict)
            and isinstance(country.get("region"), dict)
            and country["region"].get("value") != "Aggregates"
            and isinstance(country.get("id"), str)
            and isinstance(country.get("name"), str)
        ]
        return sorted(countries, key=lambda country: country["name"])

    def get_indicator(
        self, country_code: str, indicator_code: str
    ) -> dict[str, Any] | None:
        payload = self._get_json(
            f"country/{country_code}/indicator/{indicator_code}",
            {"format": "json", "per_page": 100},
        )
        if len(payload) < 2 or not isinstance(payload[1], list):
            return None

        for record in payload[1]:
            if isinstance(record, dict) and record.get("value") is not None:
                return {"year": record.get("date"), "value": record["value"]}
        return None

    def get_country_summary(self, country_code: str) -> dict[str, Any]:
        payload = self._get_json(
            f"country/{country_code}", {"format": "json"}
        )
        if len(payload) < 2 or not isinstance(payload[1], list) or not payload[1]:
            raise ResourceNotFoundError(f"Country {country_code} was not found")

        country = payload[1][0]
        if not isinstance(country, dict) or not isinstance(country.get("name"), str):
            raise WorldBankError("World Bank returned unexpected country data")

        summary: dict[str, Any] = {"country": country["name"]}
        for name, indicator in INDICATORS.items():
            summary[name] = self.get_indicator(country_code, indicator)
        return summary

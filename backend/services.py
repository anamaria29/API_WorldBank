"""Application use cases, independent from Flask and HTTP libraries."""

from typing import Any

from .world_bank import WorldBankGateway


class CountryComparisonService:
    def __init__(self, gateway: WorldBankGateway) -> None:
        self._gateway = gateway

    def list_countries(self) -> list[dict[str, str]]:
        return self._gateway.get_countries()

    def compare(self, country1: str, country2: str) -> dict[str, dict[str, Any]]:
        return {
            "country1": self._gateway.get_country_summary(country1),
            "country2": self._gateway.get_country_summary(country2),
        }

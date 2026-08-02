"""Flask composition root and HTTP controllers."""

from __future__ import annotations

import logging
import re
from typing import Any
from werkzeug.exceptions import HTTPException

from flask import Flask, jsonify, request

from .config import Config
from .services import CountryComparisonService
from .world_bank import (
    ResourceNotFoundError,
    WorldBankClient,
    WorldBankError,
)

COUNTRY_CODE_PATTERN = re.compile(r"^[A-Z]{3}$")


def create_app(
    config: type[Config] | dict[str, Any] = Config,
    service: CountryComparisonService | None = None,
) -> Flask:
    app = Flask(__name__)
    if isinstance(config, type):
        app.config.from_object(config)
    else:
        app.config.update(config)

    comparison_service = service or CountryComparisonService(
        WorldBankClient(
            base_url=app.config["WORLD_BANK_BASE_URL"],
            timeout=app.config["WORLD_BANK_TIMEOUT"],
        )
    )

    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.get("/")
    def home():
        return jsonify({"message": "Global Insights API funcionando"})

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/countries")
    def countries():
        return jsonify(comparison_service.list_countries())

    @app.get("/compare")
    def compare():
        country1 = _validated_country_code(request.args.get("country1"))
        country2 = _validated_country_code(request.args.get("country2"))
        if country1 == country2:
            return jsonify({"error": "Los países deben ser diferentes"}), 400
        return jsonify(comparison_service.compare(country1, country2))

    @app.errorhandler(ValueError)
    def handle_validation_error(error: ValueError):
        return jsonify({"error": str(error)}), 400

    @app.errorhandler(ResourceNotFoundError)
    def handle_not_found(error: ResourceNotFoundError):
        return jsonify({"error": str(error)}), 404

    @app.errorhandler(WorldBankError)
    def handle_provider_error(error: WorldBankError):
        app.logger.warning("World Bank request failed: %s", error)
        return jsonify({"error": "El proveedor de datos no está disponible"}), 502

    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException):
        return jsonify({"error": error.description}), error.code or 500

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):
        app.logger.exception("Unexpected request failure")
        return jsonify({"error": "Error interno del servidor"}), 500

    return app


def _validated_country_code(value: str | None) -> str:
    if value is None:
        raise ValueError("Debe indicar country1 y country2")
    normalized = value.strip().upper()
    if not COUNTRY_CODE_PATTERN.fullmatch(normalized):
        raise ValueError("Los países deben usar códigos ISO de tres letras")
    return normalized


app = create_app()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host="127.0.0.1", port=5000, debug=False)

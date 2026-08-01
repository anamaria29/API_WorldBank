"""Environment-backed application configuration."""

import os


class Config:
    DEBUG = False
    JSON_SORT_KEYS = False
    WORLD_BANK_BASE_URL = os.getenv(
        "WORLD_BANK_BASE_URL", "https://api.worldbank.org/v2"
    )
    WORLD_BANK_TIMEOUT = float(os.getenv("WORLD_BANK_TIMEOUT", "10"))

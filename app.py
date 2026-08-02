"""Vercel entry point.

Vercel detects this top-level Flask application and runs it as a Python
Function. The implementation remains inside the backend package.
"""

from backend.app import app
from werkzeug.exceptions import HTTPException

__all__ = ["app"]

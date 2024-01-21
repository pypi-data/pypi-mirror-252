"""Fastapp Package

Author: Collin Meyer
Created: 2024-01-18 15:04
"""
from typing import Any

APP_DESC = """
Fastapp is a boilerplate for fastapi projects. 🚀
"""

# pylint: disable=
metadata: dict[str, Any] = {
    "openapi_tags": [
        {
            "name": "Users and Authentication",
            "description": "Manage users and authentication",
        }
    ],
    "description": APP_DESC
}

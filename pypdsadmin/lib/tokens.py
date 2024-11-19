"""Module for handling secure tokens."""

import base64
import secrets


def generate_secure_token(length: int = 24) -> str:
    """Generate a secure token with the specified length."""
    random_bytes = secrets.token_bytes(30)
    token = base64.b64encode(random_bytes).decode("utf-8")
    sanitized_token = token.translate(str.maketrans("", "", "=+/"))
    return sanitized_token[:length]

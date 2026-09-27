from datetime import UTC, datetime

import jwt
import pytest

from app.auth.jwt import JWTService
from app.config.settings import Settings


def create_service() -> JWTService:
    settings = Settings(
        JWT_SECRET_KEY="test-secret",
        JWT_ALGORITHM="HS256",
        JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30,
    )

    return JWTService(settings)


def test_create_access_token():
    service = create_service()

    token = service.create_access_token(
        user_id="user-1",
        username="archit",
        role="user",
    )

    payload = jwt.decode(
        token,
        "test-secret",
        algorithms=["HS256"],
    )

    assert payload["sub"] == "user-1"
    assert payload["username"] == "archit"
    assert payload["role"] == "user"
    assert "exp" in payload


def test_decode_access_token():
    service = create_service()

    token = service.create_access_token(
        user_id="user-1",
        username="archit",
        role="admin",
    )

    payload = service.decode_access_token(token)

    assert payload["sub"] == "user-1"
    assert payload["username"] == "archit"
    assert payload["role"] == "admin"


def test_decode_invalid_token():
    service = create_service()

    with pytest.raises(jwt.InvalidTokenError):
        service.decode_access_token("invalid-token")


def test_expiration_is_present():
    service = create_service()

    token = service.create_access_token(
        user_id="user-1",
        username="archit",
        role="user",
    )

    payload = service.decode_access_token(token)

    expiration = datetime.fromtimestamp(
        payload["exp"],
        tz=UTC,
    )

    assert expiration > datetime.now(UTC)

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from app.auth.dependencies import get_current_user
from app.auth.jwt import JWTService
from app.config.settings import Settings

TEST_SECRET_KEY = "test-secret-key-that-is-at-least-32-bytes-long"


def create_app() -> FastAPI:
    app = FastAPI()

    test_settings = Settings(
        JWT_SECRET_KEY=TEST_SECRET_KEY,
        JWT_ALGORITHM="HS256",
        JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30,
    )

    app.dependency_overrides[Settings] = lambda: test_settings

    @app.get("/protected")
    def protected(user: dict = Depends(get_current_user)):
        return user

    return app


def test_get_current_user_valid_token():
    app = create_app()
    client = TestClient(app)

    settings = Settings(
        JWT_SECRET_KEY=TEST_SECRET_KEY,
        JWT_ALGORITHM="HS256",
        JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30,
    )

    jwt_service = JWTService(settings)

    token = jwt_service.create_access_token(
        user_id="user-1",
        username="archit",
        role="user",
    )

    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["sub"] == "user-1"
    assert response.json()["username"] == "archit"
    assert response.json()["role"] == "user"


def test_get_current_user_invalid_token():
    app = create_app()
    client = TestClient(app)

    response = client.get(
        "/protected",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid authentication credentials",
    }

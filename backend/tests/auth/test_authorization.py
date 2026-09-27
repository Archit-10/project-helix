from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from app.auth.dependencies import require_role
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

    @app.get("/admin")
    def admin_endpoint(
        user: dict = Depends(require_role("admin")),
    ):
        return {"message": "admin access granted"}

    return app


def create_token(role: str) -> str:
    settings = Settings(
        JWT_SECRET_KEY=TEST_SECRET_KEY,
        JWT_ALGORITHM="HS256",
        JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30,
    )

    jwt_service = JWTService(settings)

    return jwt_service.create_access_token(
        user_id="user-1",
        username="archit",
        role=role,
    )


def test_admin_user_can_access_admin_endpoint():
    app = create_app()
    client = TestClient(app)

    token = create_token("admin")

    response = client.get(
        "/admin",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "admin access granted",
    }


def test_regular_user_cannot_access_admin_endpoint():
    app = create_app()
    client = TestClient(app)

    token = create_token("user")

    response = client.get(
        "/admin",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "Insufficient permissions",
    }

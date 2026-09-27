from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError

from app.auth.jwt import JWTService
from app.config.settings import Settings

security = HTTPBearer()


def get_access_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """Extracts the JWT access token from the Authorization header."""

    return credentials.credentials


def get_current_user(
    token: str = Depends(get_access_token),
    settings: Settings = Depends(Settings),
) -> dict:
    """Validates the JWT and returns its payload."""

    jwt_service = JWTService(settings)

    try:
        return jwt_service.decode_access_token(token)
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        ) from exc


def require_role(required_role: str):
    """Creates a dependency that requires a specific user role."""

    def role_checker(
        user: dict = Depends(get_current_user),
    ) -> dict:
        if user.get("role") != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return user

    return role_checker

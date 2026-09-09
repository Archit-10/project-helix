from datetime import UTC, datetime, timedelta

import jwt

from app.config.settings import Settings


class JWTService:
    """Creates and validates JWT access tokens."""

    def __init__(self, settings: Settings) -> None:
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.access_token_expire_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES

    def create_access_token(
        self,
        user_id: str,
        username: str,
        role: str,
    ) -> str:
        expires_at = datetime.now(UTC) + timedelta(
            minutes=self.access_token_expire_minutes,
        )

        payload = {
            "sub": user_id,
            "username": username,
            "role": role,
            "exp": expires_at,
        }

        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )

    def decode_access_token(self, token: str) -> dict:
        return jwt.decode(
            token,
            self.secret_key,
            algorithms=[self.algorithm],
        )

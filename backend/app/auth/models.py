from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    """Represents an authenticated Helix user."""

    user_id: str
    username: str
    password_hash: str
    role: str = "user"
    is_active: bool = True

from app.auth.models import User


class UserRepository:
    """Provides access to Helix users."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def add(self, user: User) -> None:
        self._users[user.username] = user

    def get_by_username(self, username: str) -> User | None:
        return self._users.get(username)

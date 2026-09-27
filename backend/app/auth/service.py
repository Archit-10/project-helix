from app.auth.models import User
from app.auth.password import PasswordHasher
from app.auth.repository import UserRepository


class AuthenticationService:
    """Handles user authentication."""

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    def authenticate(
        self,
        username: str,
        password: str,
    ) -> User | None:
        user = self.user_repository.get_by_username(username)

        if user is None:
            return None

        if not user.is_active:
            return None

        if not self.password_hasher.verify_password(
            password,
            user.password_hash,
        ):
            return None

        return user

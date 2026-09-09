from app.auth.models import User
from app.auth.repository import UserRepository


def test_add_and_get_user():
    repository = UserRepository()

    user = User(
        user_id="user-1",
        username="archit",
        password_hash="hashed-password",
    )

    repository.add(user)

    result = repository.get_by_username("archit")

    assert result == user


def test_get_unknown_user_returns_none():
    repository = UserRepository()

    result = repository.get_by_username("unknown")

    assert result is None

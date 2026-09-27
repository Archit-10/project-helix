from app.auth.models import User
from app.auth.password import PasswordHasher
from app.auth.repository import UserRepository
from app.auth.service import AuthenticationService


def create_service() -> tuple[
    AuthenticationService,
    User,
    str,
]:
    repository = UserRepository()
    hasher = PasswordHasher()

    password = "secure-password"

    user = User(
        user_id="user-1",
        username="archit",
        password_hash=hasher.hash_password(password),
    )

    repository.add(user)

    service = AuthenticationService(
        user_repository=repository,
        password_hasher=hasher,
    )

    return service, user, password


def test_authenticate_valid_user():
    service, user, password = create_service()

    result = service.authenticate(
        username="archit",
        password=password,
    )

    assert result == user


def test_authenticate_unknown_user():
    service, _, password = create_service()

    result = service.authenticate(
        username="unknown",
        password=password,
    )

    assert result is None


def test_authenticate_wrong_password():
    service, _, _ = create_service()

    result = service.authenticate(
        username="archit",
        password="wrong-password",
    )

    assert result is None


def test_authenticate_inactive_user():
    repository = UserRepository()
    hasher = PasswordHasher()

    password = "secure-password"

    user = User(
        user_id="user-1",
        username="archit",
        password_hash=hasher.hash_password(password),
        is_active=False,
    )

    repository.add(user)

    service = AuthenticationService(
        user_repository=repository,
        password_hasher=hasher,
    )

    result = service.authenticate(
        username="archit",
        password=password,
    )

    assert result is None

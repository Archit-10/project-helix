from app.auth.models import User


def test_user_defaults():
    user = User(
        user_id="user-1",
        username="archit",
        password_hash="hashed-password",
    )

    assert user.user_id == "user-1"
    assert user.username == "archit"
    assert user.password_hash == "hashed-password"
    assert user.role == "user"
    assert user.is_active is True

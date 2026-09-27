from app.auth.password import PasswordHasher


def test_hash_password():
    hasher = PasswordHasher()

    password = "secure-password"

    password_hash = hasher.hash_password(password)

    assert password_hash != password
    assert password_hash.startswith("$argon2")


def test_verify_correct_password():
    hasher = PasswordHasher()

    password = "secure-password"
    password_hash = hasher.hash_password(password)

    assert hasher.verify_password(
        password,
        password_hash,
    )


def test_verify_incorrect_password():
    hasher = PasswordHasher()

    password_hash = hasher.hash_password(
        "secure-password",
    )

    assert not hasher.verify_password(
        "wrong-password",
        password_hash,
    )

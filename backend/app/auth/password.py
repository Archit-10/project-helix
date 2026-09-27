from pwdlib import PasswordHash


class PasswordHasher:
    """Handles password hashing and verification."""

    def __init__(self) -> None:
        self._password_hash = PasswordHash.recommended()

    def hash_password(self, password: str) -> str:
        return self._password_hash.hash(password)

    def verify_password(
        self,
        password: str,
        password_hash: str,
    ) -> bool:
        return self._password_hash.verify(
            password,
            password_hash,
        )

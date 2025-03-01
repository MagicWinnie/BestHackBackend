import bcrypt

FORMAT = "utf-8"


class PasswordHandler:
    def __init__(self, plain_password: str):
        self.plain_password = plain_password

    def get_password_hash(self) -> str:
        """Hash a password."""
        return bcrypt.hashpw(self.plain_password.encode(FORMAT), bcrypt.gensalt()).decode(FORMAT)

    def verify_password(self, hashed_password: str) -> bool:
        """Verify if the plain password matches the hashed version."""
        return bcrypt.checkpw(self.plain_password.encode(FORMAT), hashed_password.encode(FORMAT))

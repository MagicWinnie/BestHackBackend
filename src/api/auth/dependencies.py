from fastapi import HTTPException, status

from src.api.auth.schemas import CredentialsSchema
from src.core.auth.password_handler import PasswordHandler
from src.core.models import User
from src.core.repositories import UserRepository


async def validate_credentials(creds: CredentialsSchema) -> User:
    user = await UserRepository.get_user_by_email(email=creds.email)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not active")

    password_handler = PasswordHandler(plain_password=creds.password)
    if not password_handler.verify_password(user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    return user

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

X_API_KEY = APIKeyHeader(name="X-API-Key")


class APIKeyAuth:
    def __init__(self, token: str):
        """
        Takes the X-API-Key header and validates it with the X-API-Key in the environment.

        Args:
            token: Token to check with.
        """
        self.token = token

    def __call__(self, x_api_key: str = Security(X_API_KEY)) -> None:
        """
        Validates the header key.

        Args:
            x_api_key: The X-API-Key.

        Raises:
            HTTPException: Error 401 in case of invalid API key.
        """
        if x_api_key != self.token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API Key. Check 'X-API-Key' header.",
            )

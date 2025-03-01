from datetime import datetime, timezone

from src.core.models import BlacklistJWT


class BlacklistJWTRepository:
    @staticmethod
    async def is_token_blacklisted(token_uuid: str) -> bool:
        token = await BlacklistJWT.find_one({"refresh_token": token_uuid})
        return bool(token)

    @staticmethod
    async def add_token_uuid_to_blacklist(token_uuid: str):
        if await BlacklistJWTRepository.is_token_blacklisted(token_uuid):
            return

        document = BlacklistJWT(refresh_token=token_uuid, created_at=datetime.now(timezone.utc))
        await document.insert()

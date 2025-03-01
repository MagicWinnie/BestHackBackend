from datetime import datetime, timezone

from beanie import Document


class BlacklistJWT(Document):
    refresh_token: str
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "blacklist_jwt"

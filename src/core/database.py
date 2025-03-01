from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config import settings
from src.core.models import BlacklistJWT, Lot, Order, User


async def init_database():
    client = AsyncIOMotorClient(
        f"mongodb://{settings.MONGO_INITDB_ROOT_USERNAME}:{settings.MONGO_INITDB_ROOT_PASSWORD}@{settings.MONGODB_HOST}",
        connectTimeoutMS=5000,
        timeoutms=5000,
    )
    await init_beanie(
        database=client.besthack,
        document_models=[BlacklistJWT, Lot, Order, User],
    )

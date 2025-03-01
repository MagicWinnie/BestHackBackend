import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api import routers
from src.core.config import settings
from src.core.database import init_database

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Initializing database...")
    await init_database()
    logger.info("Database initialized")
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan,
)

for router in routers:
    app.include_router(router)

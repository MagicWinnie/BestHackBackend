from fastapi import FastAPI

from src.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
)


@app.get("/")
def root():
    return {"message": "Hello, World!"}

from typing import Annotated

from fastapi import APIRouter, File, UploadFile

from src.api.lot.service import LotService

router = APIRouter(prefix="/lot", tags=["lot"])


@router.post("/upload", response_model=int)
async def upload_csv(file: Annotated[UploadFile, File(...)]):
    return await LotService.upload_csv(file)

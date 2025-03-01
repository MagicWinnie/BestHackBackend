from typing import Annotated

from fastapi import APIRouter, File, UploadFile

from src.api.lot.schemas import LotUpdateSchema
from src.api.lot.service import LotService
from src.core.models.lot import Lot

router = APIRouter(prefix="/lot", tags=["lot"])


@router.post("/upload", response_model=int)
async def upload_csv(file: Annotated[UploadFile, File(...)]):
    return await LotService.upload_csv(file)


@router.put("/{number}", response_model=Lot)
async def update_lot(number: int, update_lot: LotUpdateSchema):
    return await LotService.update_lot(number, update_lot)


@router.delete("/{number}")
async def delete_lot(number: int):
    await LotService.delete_lot(number)

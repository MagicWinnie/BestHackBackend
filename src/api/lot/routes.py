from typing import Annotated

from fastapi import APIRouter, File, UploadFile

from src.api.lot.schemas import LotCreateSchema, LotUpdateSchema
from src.api.lot.service import LotService
from src.core.models.lot import Lot

router = APIRouter(prefix="/lot", tags=["lot"])


@router.post("/upload", response_model=int)
async def upload_csv(file: Annotated[UploadFile, File(...)]):
    return await LotService.upload_csv(file)


@router.post("/", response_model=Lot)
async def create_lot(lot: LotCreateSchema):
    return await LotService.create_lot(lot)


@router.get("/", response_model=list[Lot])
async def get_lots():
    return await LotService.get_lots()


@router.get("/{number}", response_model=Lot)
async def get_lot(number: int):
    return await LotService.get_lot_by_id(number)


@router.put("/{number}", response_model=Lot)
async def update_lot(number: int, update_lot: LotUpdateSchema):
    return await LotService.update_lot(number, update_lot)


@router.delete("/{number}")
async def delete_lot(number: int):
    await LotService.delete_lot(number)

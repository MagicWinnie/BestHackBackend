from typing import Annotated

from fastapi import APIRouter, Depends, File, Query, UploadFile

from src.api.auth.dependencies import AccessTokenUserGetter
from src.api.lot.schemas import LotCreateSchema, LotUpdateSchema, UploadFtpSchema
from src.api.lot.service import LotService
from src.core.models.lot import Lot

router = APIRouter(prefix="/lot", tags=["lot"], dependencies=[Depends(AccessTokenUserGetter())])


@router.post("/upload", response_model=int)
async def upload_csv(file: Annotated[UploadFile, File(...)]):
    return await LotService.upload_csv(file)


@router.post("/upload/ftp", response_model=int)
async def upload_ftp(body: UploadFtpSchema):
    return await LotService.upload_ftp(body.host, body.username, body.password, body.path)


@router.post("/", response_model=Lot)
async def create_lot(lot: LotCreateSchema):
    return await LotService.create_lot(lot)


@router.get("/", response_model=list[Lot])
async def get_lots(skip: Annotated[int, Query(ge=0)] = 0, limit: Annotated[int, Query(ge=0)] = 0):
    return await LotService.get_lots(skip, limit)


@router.get("/{number}", response_model=Lot)
async def get_lot(number: int):
    return await LotService.get_lot_by_id(number)


@router.put("/{number}", response_model=Lot)
async def update_lot(number: int, update_lot: LotUpdateSchema):
    return await LotService.update_lot(number, update_lot)


@router.delete("/{number}")
async def delete_lot(number: int):
    await LotService.delete_lot(number)

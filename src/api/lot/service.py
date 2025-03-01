import logging
from io import StringIO

import pandas as pd
from fastapi import HTTPException, UploadFile, status
from pydantic import ValidationError

from src.api.lot.schemas import LotCreateSchema, LotUpdateSchema
from src.core.config import settings
from src.core.models.lot import Lot
from src.core.repositories.lot import LotRepository

logger = logging.getLogger(__name__)


class LotService:
    @staticmethod
    async def upload_csv(file: UploadFile) -> int:
        if file.content_type not in ("text/csv", "application/vnd.ms-excel"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File must be a CSV")

        content = await file.read()
        stringio = StringIO(content.decode("utf-8"))
        df = pd.read_csv(stringio)

        if len(df.columns) != len(settings.LOT_COLUMNS):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"CSV file has {len(df.columns)} columns, expected {len(settings.LOT_COLUMNS)}",
            )

        df.columns = settings.LOT_COLUMNS

        new_lot_number = await LotRepository.get_new_lot_number()

        lots_data = df.to_dict(orient="records")
        lots_to_save = []
        for lot_data in lots_data:
            try:
                lot_data["number"] = new_lot_number
                lot = Lot(**lot_data)  # type: ignore
                lots_to_save.append(lot)
                new_lot_number += 1
            except ValidationError as e:
                logger.warning("Validation error: %s", e)
                continue

        result = await Lot.insert_many(lots_to_save)
        return len(result.inserted_ids)

    @staticmethod
    async def get_lot_by_id(number: int) -> Lot:
        lot = await LotRepository.get_lot_by_id(number)
        if lot is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lot not found")
        return lot

    @staticmethod
    async def delete_lot(number: int) -> None:
        lot = await LotService.get_lot_by_id(number)
        await lot.delete()

    @staticmethod
    async def update_lot(number: int, update_lot: LotUpdateSchema) -> Lot:
        lot = await LotRepository.update_lot(number, update_lot)
        if lot is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lot not found")
        return lot

    @staticmethod
    async def get_lots(skip: int, limit: int) -> list[Lot]:
        return await LotRepository.get_lots(skip, limit)

    @staticmethod
    async def create_lot(lot: LotCreateSchema) -> Lot:
        return await LotRepository.create_lot(lot)

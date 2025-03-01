import logging
from io import StringIO

import pandas as pd
from fastapi import HTTPException, UploadFile, status
from pydantic import ValidationError

from src.core.config import settings
from src.core.models.lot import Lot

logger = logging.getLogger(__name__)


class LotService:
    @staticmethod
    async def upload_csv(file: UploadFile) -> int:
        if file.content_type != "text/csv":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File must be a CSV (MIME: text/csv)")

        content = await file.read()
        stringio = StringIO(content.decode("utf-8"))
        df = pd.read_csv(stringio)

        if len(df.columns) != len(settings.LOT_COLUMNS):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"CSV file has {len(df.columns)} columns, expected {len(settings.LOT_COLUMNS)}",
            )

        df.columns = settings.LOT_COLUMNS

        lots_data = df.to_dict(orient="records")
        lots_to_save = []
        for lot_data in lots_data:
            try:
                lot = Lot(**lot_data)  # type: ignore
                lots_to_save.append(lot)
            except ValidationError as e:
                logger.warning("Validation error: %s", e)
                continue

        result = await Lot.insert_many(lots_to_save)
        return len(result.inserted_ids)

import csv
import io
import logging
from datetime import datetime
from decimal import Decimal
from ftplib import FTP
from io import StringIO

from fastapi import HTTPException, UploadFile, status

from src.api.lot.schemas import LotCreateSchema, LotUpdateSchema
from src.core.config import settings
from src.core.models.lot import Lot, LotStatus
from src.core.repositories.lot import LotRepository

logger = logging.getLogger(__name__)


class LotService:
    @staticmethod
    async def upload_csv(file: UploadFile) -> int:
        if file.content_type not in ("text/csv", "application/vnd.ms-excel"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File must be a CSV")

        content = await file.read()
        string_content = content.decode("utf-8")
        string_io = StringIO(string_content)
        reader = csv.reader(string_io)

        new_lot_number = await LotRepository.get_new_lot_number()
        lots, new_lot_number = LotService._parse_lots(reader, new_lot_number)

        if lots:
            await Lot.insert_many(lots)

        return len(lots)

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
        return await LotRepository.get_lots(skip, limit, [LotStatus.CONFIRMED])

    @staticmethod
    async def create_lot(lot: LotCreateSchema) -> Lot:
        return await LotRepository.create_lot(lot)

    @staticmethod
    async def upload_ftp(host: str, username: str, password: str, path: str) -> int:
        try:
            ftp = FTP(host, timeout=settings.FTP_TIMEOUT)
            ftp.login(user=username, passwd=password)
        except Exception as e:
            logger.error("Error connecting to FTP: %s", e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error connecting to FTP") from e

        buffer = io.BytesIO()
        ftp.retrbinary(f"RETR {path}", buffer.write)
        buffer.seek(0)

        text_stream = io.TextIOWrapper(buffer, encoding="utf-8")
        reader = csv.reader(text_stream)

        new_lot_number = await LotRepository.get_new_lot_number()
        lots, new_lot_number = LotService._parse_lots(reader, new_lot_number)

        ftp.quit()

        if lots:
            await Lot.insert_many(lots)

        return len(lots)

    @staticmethod
    def _parse_lots(reader, new_lot_number: int) -> tuple[list[Lot], int]:
        lots = []

        _ = next(reader, None)

        for row in reader:
            if len(row) == 9:
                row = row[1:]
            try:
                lot = Lot(
                    number=new_lot_number,
                    date=datetime.fromisoformat(row[0]),
                    code_nb=int(row[1]),
                    code_fuel=int(row[2]),
                    start_weight=Decimal(row[3]),
                    available_balance=Decimal(row[4]) if row[4].strip() else None,
                    status=LotStatus(row[5]),
                    price=Decimal(row[6]) if row[6].strip() else None,
                    price_per_ton=Decimal(row[7]),
                )
                lots.append(lot)
                new_lot_number += 1
            except Exception as e:
                logger.warning("Error parsing row %s: %s", row, e)
        return lots, new_lot_number

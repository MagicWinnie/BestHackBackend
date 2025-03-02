from datetime import datetime

from beanie import DecimalAnnotation
from pydantic import BaseModel

from src.core.models.lot import LotStatus


class LotUpdateSchema(BaseModel):
    date: datetime | None = None
    code_nb: int | None = None
    code_fuel: int | None = None
    start_weight: DecimalAnnotation | None = None
    available_balance: DecimalAnnotation | None = None
    status: LotStatus | None = None
    price: DecimalAnnotation | None = None
    price_per_ton: DecimalAnnotation | None = None


class LotCreateSchema(BaseModel):
    date: datetime
    code_nb: int
    code_fuel: int
    start_weight: DecimalAnnotation
    available_balance: DecimalAnnotation
    status: LotStatus
    price: DecimalAnnotation
    price_per_ton: DecimalAnnotation


class UploadFtpSchema(BaseModel):
    ip: str
    username: str
    password: str
    path: str

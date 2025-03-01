from uuid import UUID

from beanie import DecimalAnnotation
from pydantic import BaseModel

from src.core.models import OrderDeliveryType


class OrderCreateSchema(BaseModel):
    lot_number: int
    code_nb: int
    code_fuel: int
    volume: DecimalAnnotation
    delivery_type: OrderDeliveryType
    user_id: UUID

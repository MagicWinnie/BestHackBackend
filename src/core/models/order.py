from datetime import datetime
from enum import Enum
from uuid import UUID

from beanie import DecimalAnnotation, Document
from pydantic import ConfigDict


class OrderDeliveryType(str, Enum):
    SELF_DELIVERY = "self_delivery"
    DELIVERY = "delivery"


class Order(Document):
    model_config = ConfigDict(use_attribute_docstrings=True)

    number: int
    """Номер заказа (автоинкремент)"""

    date: datetime
    """Дата заказа"""

    lot_number: int
    """Номер лота"""

    code_nb: int
    """Код КССС НБ"""

    code_fuel: int
    """Код КССС Топлива"""

    volume: DecimalAnnotation
    """Объём заказа"""

    delivery_type: OrderDeliveryType
    """Тип доставки"""

    user_id: UUID
    """Идентификатор пользователя"""

    class Settings:
        name = "orders"

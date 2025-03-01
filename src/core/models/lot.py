from datetime import datetime
from enum import Enum

from beanie import DecimalAnnotation, Document
from pydantic import ConfigDict


class LotStatus(str, Enum):
    CONFIRMED = "Подтвержден"
    SOLD = "Продан"
    INACTIVE = "Неактивен"


class Lot(Document):
    model_config = ConfigDict(use_attribute_docstrings=True)

    number: int
    """Номер (автоинкремент)"""

    date: datetime
    """Дата лота"""

    code_nb: int
    """Код КССС НБ"""

    code_fuel: int
    """Код КССС Топлива"""

    start_weight: DecimalAnnotation
    """Стартовый вес (доступный объём лота в литрах)"""

    available_balance: DecimalAnnotation | None = None
    """Доступный остаток (по умолчанию стартовый вес, уменьшается при оформлении заказа)"""

    status: LotStatus
    """Статус (по умолчанию «Подтвержден», «Продан» при оформлении заказов на весь объём, «Неактивен» при
    оставшимся доступном объёма в лоте при наступлении даты следующий за датой лота)"""

    price: DecimalAnnotation | None = None
    """Цена лота (общая стоимость лота в рублях (цена за 1 тонну * доступный остаток))"""

    price_per_ton: DecimalAnnotation
    """Цена за 1 тонну"""

    def model_post_init(self, __context):
        if self.available_balance is None:
            self.available_balance = self.start_weight
        if self.price is None:
            self.price = self.price_per_ton * self.available_balance

    class Settings:
        name = "lots"

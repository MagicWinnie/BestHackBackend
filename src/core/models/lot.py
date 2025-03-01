from datetime import datetime
from decimal import Decimal
from enum import Enum

from beanie import Document
from pydantic import ConfigDict


class LotStatus(str, Enum):
    CONFIRMED = "Подтвержден"
    SOLD = "Продан"
    INACTIVE = "Неактивен"


class Lot(Document):
    model_config = ConfigDict(use_attribute_docstrings=True)

    number: int
    """Номер (Число, авто инкремент)"""

    date: datetime
    """Дата лота (Дата)"""

    code_nb: int
    """Код КССС НБ (Число)"""

    code_fuel: int
    """Код КССС Топлива (Число)"""

    start_weight: Decimal
    """Стартовой вес (Число, доступный объём лота в литрах)"""

    available_balance: Decimal | None = None
    """Доступный остаток (Число, по умолчанию стартовый вес, уменьшается при оформлении заказа)"""

    status: LotStatus
    """Статус (Строка, по умолчанию «Подтвержден», «Продан» при оформлении заказов на весь объём, «Неактивен» при
    оставшимся доступном объёма в лоте при наступлении даты следующий за датой лота)"""

    price: Decimal | None = None
    """Цена лота (Число, общая стоимость лота в рублях (цена за 1 тонну * доступный остаток))"""

    price_per_ton: Decimal
    """Цена за 1 тонну. (Число)"""

    def model_post_init(self, __context):
        if self.available_balance is None:
            self.available_balance = self.start_weight
        if self.price is None:
            self.price = self.price_per_ton * self.available_balance

    class Settings:
        name = "lots"

from datetime import datetime, timezone

from src.api.order.schemas import OrderCreateSchema
from src.core.models.order import Order


class OrderRepository:
    @staticmethod
    async def get_new_order_number() -> int:
        last_order = await Order.find().sort("-number").limit(1).to_list()
        if not last_order:
            return 1
        return last_order[0].number + 1

    @staticmethod
    async def create_order(create_order: OrderCreateSchema) -> Order:
        order = Order(
            number=await OrderRepository.get_new_order_number(),
            date=datetime.now(timezone.utc),
            lot_number=create_order.lot_number,
            code_nb=create_order.code_nb,
            code_fuel=create_order.code_fuel,
            volume=create_order.volume,
            delivery_type=create_order.delivery_type,
            user_id=create_order.user_id,
        )
        return await order.save()

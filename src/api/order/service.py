from fastapi import HTTPException, status

from src.api.order.schemas import OrderCreateSchema
from src.core.models import Order
from src.core.models.lot import LotStatus
from src.core.repositories import LotRepository
from src.core.repositories.order import OrderRepository


class OrderService:
    @staticmethod
    async def create_order(create_order: OrderCreateSchema) -> Order:
        lot = await LotRepository.get_lot_by_id(create_order.lot_number)
        if lot is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lot not found")
        if lot.available_balance is None:
            lot.available_balance = lot.start_weight
        if lot.available_balance < create_order.volume:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough fuel available in the lot")

        lot.available_balance -= create_order.volume
        if lot.available_balance == 0:
            lot.status = LotStatus.SOLD
        await lot.save()

        return await OrderRepository.create_order(create_order)

from fastapi import APIRouter

from src.api.order.schemas import OrderCreateSchema
from src.api.order.service import OrderService
from src.core.models import Order

router = APIRouter(prefix="/order", tags=["order"])


@router.post("/", response_model=Order)
async def create_order(order: OrderCreateSchema):
    return await OrderService.create_order(order)

from fastapi import APIRouter, Depends

from src.api.auth.dependencies import AccessTokenUserGetter
from src.api.order.schemas import OrderCreateSchema
from src.api.order.service import OrderService
from src.core.models import Order

router = APIRouter(prefix="/order", tags=["order"], dependencies=[Depends(AccessTokenUserGetter())])


@router.post("/", response_model=Order)
async def create_order(order: OrderCreateSchema):
    return await OrderService.create_order(order)

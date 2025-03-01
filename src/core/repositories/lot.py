from src.api.lot.schemas import LotCreateSchema, LotUpdateSchema
from src.core.models import Lot


class LotRepository:
    @staticmethod
    async def get_lot_by_id(number: int) -> Lot | None:
        return await Lot.find_one({"number": number})

    @staticmethod
    async def get_new_lot_number() -> int:
        last_lot = await Lot.find().sort("-number").limit(1).to_list()
        if not last_lot:
            return 1
        return last_lot[0].number + 1

    @staticmethod
    async def update_lot(number: int, update_lot: LotUpdateSchema) -> Lot | None:
        lot = await LotRepository.get_lot_by_id(number)
        if lot is None:
            return None

        if update_lot.date is not None:
            lot.date = update_lot.date
        if update_lot.code_nb is not None:
            lot.code_nb = update_lot.code_nb
        if update_lot.code_fuel is not None:
            lot.code_fuel = update_lot.code_fuel
        if update_lot.start_weight is not None:
            lot.start_weight = update_lot.start_weight
        if update_lot.available_balance is not None:
            lot.available_balance = update_lot.available_balance
        if update_lot.status is not None:
            lot.status = update_lot.status
        if update_lot.price is not None:
            lot.price = update_lot.price
        if update_lot.price_per_ton is not None:
            lot.price_per_ton = update_lot.price_per_ton

        return await lot.save()

    @staticmethod
    async def get_lots() -> list[Lot]:
        return await Lot.find_all().to_list()

    @staticmethod
    async def create_lot(lot: LotCreateSchema) -> Lot:
        return await Lot(**lot.model_dump()).save()

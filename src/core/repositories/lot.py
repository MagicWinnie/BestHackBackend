from src.api.lot.schemas import LotUpdateSchema
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

        lot.date = update_lot.date or lot.date
        lot.code_nb = update_lot.code_nb or lot.code_nb
        lot.code_fuel = update_lot.code_fuel or lot.code_fuel
        lot.start_weight = update_lot.start_weight or lot.start_weight
        lot.available_balance = update_lot.available_balance or lot.available_balance
        lot.status = update_lot.status or lot.status
        lot.price = update_lot.price or lot.price
        lot.price_per_ton = update_lot.price_per_ton or lot.price_per_ton

        return await lot.save()

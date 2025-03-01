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

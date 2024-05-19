import asyncio
from models.methods import get_free_order_by_user


async def check_order_after_delay(user_id: int, delay: int = 20) -> bool | None:
    await asyncio.sleep(delay)
    is_find = get_free_order_by_user(user_id=user_id)
    if is_find:
        return True

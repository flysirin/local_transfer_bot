from aiogram import Bot
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from models.methods import get_driver_usernames_from_db, get_banned_users, get_admins
from config_data.config import ADMIN_IDS


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        admin_ids: list[int] = [int(admin_id) for admin_id in ADMIN_IDS.split(',')]
        admin_usernames: list[str] = get_admins()
        if admin_usernames and message.from_user.username in admin_usernames:
            return True
        elif message.from_user.id in admin_ids:
            return True
        return False


class IsDriver(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        driver_usernames: list = get_driver_usernames_from_db()
        if driver_usernames and message.from_user.username in driver_usernames:
            return True
        return False


class IsNotBannedUser(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        banned_users = get_banned_users()
        if message.from_user.id not in banned_users:
            return True
        return False
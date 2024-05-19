from aiogram import Bot, Router, F
from filters.filters import IsDriver
from lexicon.lexicon import LEXICON_COMMANDS, HOST_LEXICON, DRIVERS_LEXICON
from aiogram.filters import CommandStart, Command, Text
from aiogram.types import Message, CallbackQuery
from keyboards.keyboards import order_inline_kb, end_drive_inline_kb
from models.create_db import OrderStatus
import logging

from models.methods import *

logging.basicConfig(level=logging.INFO)
logger_driver_handler = logging.getLogger(__name__)

driver_router = Router()

driver_router.message.filter(IsDriver())
driver_router.callback_query.filter(IsDriver())


@driver_router.message(CommandStart())
async def start(message: Message):
    driver_id = message.from_user.id
    username = message.from_user.username
    add_driver_id(driver_id=driver_id, username=username)
    await message.answer(text=DRIVERS_LEXICON["activate_driver"])


@driver_router.callback_query(Text(contains="_order_confirm_"))
async def order_confirm(callback: CallbackQuery):
    user_id = callback.data.replace("_order_confirm_", "")
    bot = Bot.get_current()
    text_message = callback.message.text
    await callback.message.edit_text(text=f'{text_message}\n'
                                          f'{DRIVERS_LEXICON["order_confirmed"]}',
                                     reply_markup=end_drive_inline_kb(user_id))
    driver_id = callback.from_user.id
    put_driver_to_order(user_id=int(user_id), status_drive=OrderStatus.DRIVE.value, driver_id=driver_id)
    await bot.send_message(int(user_id), text=HOST_LEXICON["driver_coming"])


@driver_router.callback_query(Text(contains="_reject_"))
async def order_reject(callback: CallbackQuery):
    user_id = callback.data.replace("_reject_", "")
    bot = Bot.get_current()
    await callback.message.delete()
    await bot.send_message(int(user_id), text=HOST_LEXICON["order_rejected"])


@driver_router.callback_query(Text(startswith="_end_drive_"))
async def end_drive(callback: CallbackQuery):
    user_id = callback.data.replace("_end_drive_", "")
    driver_id = callback.from_user.id
    update_order_status(user_id=int(user_id), status_drive=OrderStatus.END.value, driver_id=driver_id)
    await callback.answer(text=DRIVERS_LEXICON["end_drive_alert"], show_alert=True)
    await callback.message.delete()


import asyncio

from aiogram import Bot, Router, F
from filters.filters import IsNotBannedUser
from lexicon.lexicon import LEXICON_COMMANDS, HOST_LEXICON, DRIVERS_LEXICON
from aiogram.filters import CommandStart, Command, Text
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from keyboards.keyboards import order_inline_kb, order_driver_inline_kb
from models.methods import *
import logging

from services.user_services import check_order_after_delay

logging.basicConfig(level=logging.INFO)
logger_user_handler = logging.getLogger(__name__)

router_user = Router()
router_user.message.filter(IsNotBannedUser())
router_user.callback_query.filter(IsNotBannedUser())


@router_user.message(CommandStart())
async def start(message: Message):
    location_id = message.text.split()[-1]
    print(location_id)
    user_id = message.from_user.id
    username = message.from_user.username
    if not location_id.isdigit():
        await message.answer(text=LEXICON_COMMANDS['/start'])
        return
    create_order(user_id=user_id, username=username, location_id=location_id)
    await message.answer(text=HOST_LEXICON["order"], reply_markup=order_inline_kb())


@router_user.message(Command(commands=["help"]))
async def start(message: Message):
    await message.answer(text=LEXICON_COMMANDS["/help"])


@router_user.callback_query(Text("order_now"))
async def start(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(HOST_LEXICON["wait_drivers"])
    await callback.message.delete()

    user_id: int = callback.from_user.id
    username: str = callback.from_user.username
    driver_id: int = get_free_driver_id_from_db()
    if not driver_id:
        await callback.message.answer(text=HOST_LEXICON["no_drivers"], reply_markup=ReplyKeyboardRemove())
        return

    if not callback.from_user.is_bot:
        bot = Bot.get_current()
        location_id = get_location_id_from_user_id(user_id)
        location_name = get_location_name(location_id=location_id)
        if not location_name:
            location_name = f'{DRIVERS_LEXICON["not_set"]}'

        await bot.send_message(driver_id,
                               text=f'{DRIVERS_LEXICON["confirm_order"]}{location_id}\n'
                                    f'{DRIVERS_LEXICON["location_name"]} <b>{location_name}</b>\n'
                                    f'{DRIVERS_LEXICON["user_profile"]}\n'
                                    f'https://t.me/{username}',
                               reply_markup=order_driver_inline_kb(user_id))

    if await check_order_after_delay(user_id, delay=120):
        await callback.message.answer(text=HOST_LEXICON["driver_no_answer"])

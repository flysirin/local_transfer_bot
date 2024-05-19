from aiogram import Bot, Router, F
from filters.filters import IsDriver, IsAdmin
from lexicon.lexicon import LEXICON_COMMANDS, HOST_LEXICON, ADMIN_LEXICON
from aiogram.filters import CommandStart, Command, Text, StateFilter
from aiogram.types import Message, CallbackQuery
from keyboards.keyboards import order_inline_kb, admin_inline_kb, remove_driver_inline_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from models.methods import *
from states.admin_states import FSMAdmin

import logging

logging.basicConfig(level=logging.INFO)
logger_driver_handler = logging.getLogger(__name__)

admin_router = Router()

admin_router.message.filter(IsAdmin())
admin_router.callback_query.filter(IsAdmin())


@admin_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    username = message.from_user.username
    user_id = message.from_user.id
    add_admin_id_to_db(username=username, admin_id=user_id)
    await message.answer(text=ADMIN_LEXICON["chose_option"], reply_markup=admin_inline_kb())
    await state.set_state(FSMAdmin.default_state)


@admin_router.callback_query(Text(text=["add_driver"]), StateFilter(FSMAdmin.default_state))
async def add_driver(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=ADMIN_LEXICON["write_nickname"])
    await state.set_state(FSMAdmin.add_driver)


@admin_router.message(StateFilter(FSMAdmin.add_driver))
async def driver_added(message: Message, state: FSMContext):
    username = message.text
    add_driver_to_db(username=username)
    await message.answer(text=f'{ADMIN_LEXICON["driver_added"]} {username}\n'
                              f'{ADMIN_LEXICON["reminder"]}')
    await message.delete()
    await state.set_state(FSMAdmin.default_state)


@admin_router.callback_query(Text(text=["remove_driver"]), StateFilter(FSMAdmin.default_state))
async def add_driver(callback: CallbackQuery, state: FSMContext):
    drivers_usernames: list[str] = get_driver_usernames_from_db()
    await callback.message.edit_text(text=ADMIN_LEXICON["chose_remove"],
                                     reply_markup=remove_driver_inline_kb(drivers_usernames))
    await state.set_state(FSMAdmin.delete_driver)


@admin_router.callback_query(F.data.regexp(r"_{2}.*_{2}"), StateFilter(FSMAdmin.delete_driver))
async def add_driver(callback: CallbackQuery, state: FSMContext):
    username = callback.data[2:-2]
    delete_driver(username)
    await callback.message.edit_text(text=f'{username} {ADMIN_LEXICON["remove_complete"]}')
    await state.set_state(FSMAdmin.default_state)


@admin_router.callback_query(Text(text=["##cancel##operation##"]))
async def cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=ADMIN_LEXICON["chose_option"], reply_markup=admin_inline_kb())
    await state.set_state(FSMAdmin.default_state)


@admin_router.callback_query(Text(text=["add_admin"]), StateFilter(FSMAdmin.default_state))
async def add_driver(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=ADMIN_LEXICON["write_admin_nickname"])
    await state.set_state(FSMAdmin.add_admin)


@admin_router.message(StateFilter(FSMAdmin.add_admin))
async def admin_added(message: Message, state: FSMContext):
    username = message.text
    add_admin_to_db(username=username)
    await message.answer(text=f'{ADMIN_LEXICON["admin_added"]} {username}\n'
                              f'{ADMIN_LEXICON["reminder"]}')
    await message.delete()
    await state.set_state(FSMAdmin.default_state)


@admin_router.callback_query(Text(text=["remove_admin"]), StateFilter(FSMAdmin.default_state))
async def add_driver(callback: CallbackQuery, state: FSMContext):
    admin_usernames: list[str] = get_admins()
    await callback.message.edit_text(text=ADMIN_LEXICON["chose_remove_admin"],
                                     reply_markup=remove_driver_inline_kb(admin_usernames))
    await state.set_state(FSMAdmin.delete_admin)


@admin_router.callback_query(F.data.regexp(r"_{2}.*_{2}"), StateFilter(FSMAdmin.delete_admin))
async def add_driver(callback: CallbackQuery, state: FSMContext):
    username = callback.data[2:-2]
    remove_admin_from_db(username=username)
    await callback.message.edit_text(text=f'{username} {ADMIN_LEXICON["remove_complete"]}')
    await state.set_state(FSMAdmin.default_state)


@admin_router.callback_query(Text(text=["view_orders"]))
async def view_orders(callback: CallbackQuery):
    orders_stat = stat_orders()
    info_message = (f'{ADMIN_LEXICON["view_orders"]}\n'
                      f'{ADMIN_LEXICON["about_info"]}\n'
                      f'{orders_stat}')
    if len(info_message) < 4000:
        await callback.message.edit_text(text=info_message)
        return
    chucks = info_message.split("\n")
    result = ''
    for chuck in chucks:
        if len(result + chuck + '\n') > 4000:
            await callback.message.edit_text(text=result)
            return
        result += chuck + '\n'

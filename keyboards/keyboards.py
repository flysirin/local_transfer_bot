from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
from lexicon.lexicon import HOST_BUTTONS, ADMIN_BUTTONS
from aiogram.utils.keyboard import InlineKeyboardBuilder


def order_inline_kb() -> InlineKeyboardMarkup:
    order = InlineKeyboardButton(text=HOST_BUTTONS["order_now"], callback_data="order_now")
    reject = InlineKeyboardButton(text=HOST_BUTTONS["reject"], callback_data="reject")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[order],
                                                     [reject],
                                                     ], )
    return keyboard


def order_driver_inline_kb(user_id) -> InlineKeyboardMarkup:
    order_confirm = InlineKeyboardButton(text=HOST_BUTTONS["order_confirm"],
                                         callback_data=f"_order_confirm_{user_id}")
    reject = InlineKeyboardButton(text=HOST_BUTTONS["reject"],
                                  callback_data=f"_reject_{user_id}")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[order_confirm],
                                                     [reject],
                                                     ], )
    return keyboard


def end_drive_inline_kb(user_id) -> InlineKeyboardMarkup:
    end_drive = InlineKeyboardButton(text=HOST_BUTTONS["end_drive"],
                                     callback_data=f"_end_drive_{user_id}")
    # reject = InlineKeyboardButton(text=HOST_BUTTONS["reject"],
    #                               callback_data=f"_reject_{user_id}")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[end_drive],
                                                     # [reject],
                                                     ], )
    return keyboard


def admin_inline_kb() -> InlineKeyboardMarkup:
    add_driver = InlineKeyboardButton(text=ADMIN_BUTTONS["add_driver"],
                                      callback_data=f"add_driver")
    remove_driver = InlineKeyboardButton(text=ADMIN_BUTTONS["remove_driver"],
                                         callback_data=f"remove_driver")
    add_admin = InlineKeyboardButton(text=ADMIN_BUTTONS["add_admin"],
                                     callback_data=f"add_admin")
    view_orders = InlineKeyboardButton(text=ADMIN_BUTTONS["view_orders"],
                                       callback_data=f"view_orders")
    remove_admin = InlineKeyboardButton(text=ADMIN_BUTTONS["remove_admin"],
                                        callback_data="remove_admin")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[add_driver],
                                                     [remove_driver],
                                                     [add_admin],
                                                     [remove_admin],
                                                     [view_orders],
                                                     ], )
    return keyboard


def remove_driver_inline_kb(drivers_names: list, width: int = 1) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if drivers_names:
        for username in drivers_names:
            buttons.append(InlineKeyboardButton(text=f"{username}",
                                                callback_data=f"__{username}__"))
        buttons.append(InlineKeyboardButton(text=ADMIN_BUTTONS["cancel"],
                                            callback_data=f"##cancel##operation##"))

    kb_builder.row(*buttons, width=width)  # unpack button's list to builder by method row with param width

    return kb_builder.as_markup()  # return object inline kb

HOST_LEXICON: dict = {
    'order': "Заказ трансфера",
    "driver_coming": "Водитель в пути",
    "order_rejected": "Заказ отклонен",
    "no_drivers": "Нет водителей на данный момент! Повторите заказ позже.",
    "wait_drivers": "Ожидайте подтверждение от водителя",
    "driver_no_answer": "Водитель не отвечает в данный момент"
}

LEXICON_COMMANDS: dict[str: str] = {
    '/start': 'Привет! Это бот заказа трансфера (тестовый)  на территории '
              'Солнечной Долины. Для заказа сканируй код на остановке и жми '
              '"Заказать сейчас" 🚗',
    '/help': 'Для заказа трансфера "Заказать сейчас"',
}

HOST_BUTTONS: dict[str: str] = {
    'order_now': "Заказать сейчас",
    'reject': "Отмена",
    "order_confirm": "Подтвердить заказ трансфера",
    "end_drive": "Завершить поездку",

}

DRIVERS_LEXICON: dict[str: str] = {
    "confirm_order": "Поездка от места номер: ",
    'reject': "Отмена",
    "activate_driver": "Ваш статус водителя активен",
    "user_profile": "Пользователь: ",
    "order_confirmed": "Вы приняли заказ",
    "end_drive_alert": "Поездка завершена",
    "location_name": "Название: ",
    "not_set": "Не установлено ;(",

}

ADMIN_LEXICON: dict[str: str] = {
    "chose_option": "Выберите опцию:",
    "write_nickname": "Введите никнейм пользователя, которого хотите добавить:",
    "driver_added": "Водитель добавлен: ",
    "reminder": "Для активации отправьте ему ссылку на бота:\n"
                "https://t.me/DolinaTransferBot?start",

    "chose_remove": "Выберите водителя, которого хотите удалить: ",
    "remove_complete": "удален",
    "write_admin_nickname": "Введите никнейм, которому хотите дать права администратора:",
    "admin_added": "Администратор добавлен:",
    "chose_remove_admin": "Выберите админа, которого хотите удалить: ",
    "view_orders": "Статистика заказов",
    "about_info": "Пассажир | Водитель | Время | статус поездки ",

    "available_locations": "Заданные локации:\n",

    "write_location_name": "Введите номер и название локации через пробел\n"
                           "<b>N Хаски центр</b>",

    "wrong_input_location": "🚫Не верно введены данные, пример: \n"
                            "<b>N Хаски центр</b>",
    "update_location_name_to_id": "Данные обновлены: ",

}

ADMIN_BUTTONS: dict[str: str] = {
    "add_driver": "Добавить водителя",
    "remove_driver": "Удалить водителя",
    "add_admin": "Добавить админа",
    "view_orders": "Посмотреть поездки",
    "cancel": "Отмена",
    "remove_admin": "Удалить администратора(!!!)",
    "attach_name_to_id": "Прикрепить название к номеру локации",

}

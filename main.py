import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from config_data.config import BOT_PROXY
from handlers import user_handlers, driver_handlers, admin_handlers
from config_data import config
from keyboards.set_menu import set_main_menu

logger_main_file = logging.getLogger(__name__)

session = None

if BOT_PROXY:
    session = AiohttpSession(proxy=BOT_PROXY)


bot_obj = Bot(token=config.BOT_TOKEN, parse_mode='HTML', session=session)


async def main(bot: Bot):
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    logger_main_file.info("Starting bot")
    dp = Dispatcher()  # storage=storage
    await bot.delete_webhook(drop_pending_updates=True)

    dp.include_router(admin_handlers.admin_router)
    dp.include_router(driver_handlers.driver_router)
    dp.include_router(user_handlers.router_user)

    await set_main_menu(bot)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main(bot=bot_obj))

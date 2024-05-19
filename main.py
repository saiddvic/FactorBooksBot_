import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from bot.handlers import private_handler_router
from config import conf
from db import database, Category




async def on_startup(dispatcher: Dispatcher, bot: Bot):
    await database.create_all()
    commands_list = [
        BotCommand(command='start', description='Botni ishga tushurish'),
        BotCommand(command='help', description='Yordam')
    ]
    await bot.set_my_commands(commands_list)


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    pass


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(private_handler_router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    bot = Bot(token=conf.bot.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
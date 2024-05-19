from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from db import User

keyboard_router = Router()
@keyboard_router.message(CommandStart())
async def command_start_handler(message: Message, bot: Bot) -> None:
    user_data = message.from_user.model_dump(include={'id', 'first_name', 'username'})
    user_id = message.from_user.id
    if not await User.get(message.from_user.id):
        await User.create(**user_data)
    rkm = ReplyKeyboardBuilder()
    rkm.add(
        KeyboardButton(text='📚 Kitoblar'),
        KeyboardButton(text='📃 Mening buyurtmalarim'),
        KeyboardButton(text='🔵 Biz ijtimoiy tarmoqlarda'),
        KeyboardButton(text="📞 Biz bilan bog'lanish"),
    )
    rkm.adjust(1, 1, 2)
    await bot.send_message(chat_id=user_id, text="Assalomu alaykum! Tanlang.", reply_markup=rkm.as_markup(resize_keyboard=True))

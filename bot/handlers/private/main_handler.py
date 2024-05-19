from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

main_router = Router()



@main_router.message(F.text == "📞 Biz bilan bog'lanish")
async def info_handler(message: Message):
    await message.answer(f"Telegram: @glorystorebot\n\n📞 + 998993479727\n\n🤖 Bot Said(@said) tomonidan tayyorlandi.")


@main_router.message(F.text=='📃 Mening buyurtmalarim')
async def order_handler(message: Message):
    await message.answer('🤷‍♂️ Sizda xali buyurtmalar mavjud emas.')

@main_router.message(Command('help'))
async def help_handler(message: Message):
    await message.answer("""Buyruqlar: 
/start - Botni ishga tushirish
/help - Yordam""")


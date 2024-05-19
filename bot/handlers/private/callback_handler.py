import os

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, URLInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db import Product, Category, Order

callback_router = Router()

user_pages = {}


@callback_router.callback_query(F.data.startswith('category_'))
async def category_handler_callback(callback: CallbackQuery):
    category_id = int(callback.data.split('category_')[-1])
    user_pages['category_id'] = category_id
    products = await Product.get_products_by_category_id(category_id)
    ikb = InlineKeyboardBuilder()
    for product in products:

        ikb.add(InlineKeyboardButton(text=product.name, callback_data=f"product_{product.id}"))
    ikb.add(InlineKeyboardButton(text='◀️ Orqaga', callback_data='go_back'))
    ikb.adjust(2, repeat=True)
    await callback.message.edit_text('📚Productni tanlang', reply_markup=ikb.as_markup())

@callback_router.callback_query(F.data.startswith('product_'))
async def poduct_handler_callback(callback: CallbackQuery):
    ikb = InlineKeyboardBuilder()
    real_user_id = callback.from_user.id
    product_id = int(callback.data.split('product_')[-1])

    product = await Product.get(product_id)
    caption = f"""📚Kitob haqida;
    
🔹 Nomi: {product.id}

💸 Narxi: {product.price}
    """
    user_id = callback.message.from_user.id
    user_pages[user_id] = 1
    user_pages['product_id'] = product_id
    user_pages[real_user_id] = real_user_id
    ikb.add(
        InlineKeyboardButton(text='➖', callback_data='page_-1'),
        InlineKeyboardButton(text='1', callback_data='info'),
        InlineKeyboardButton(text='➕', callback_data='page_+1'),
        InlineKeyboardButton(text='◀️ Orqaga', callback_data='go_back'),
        InlineKeyboardButton(text="🛒 Savatga qo'shish", callback_data='add'),
    )
    ikb.adjust(3, 2, repeat=True)
    await callback.message.delete()
    await callback.message.answer_photo(photo=URLInputFile(product.photo.telegra_image_url), caption=caption, reply_markup=ikb.as_markup())
    # await callback.answer(f"{product_id} tanlandi", show_alert=True)

@callback_router.callback_query(F.data.startswith('page_'))
async def callback_handler_callback(callback: CallbackQuery, state: FSMContext):

    page_id = callback.data.split('page_')[-1]
    user_id = callback.message.from_user.id
    await state.set_state(str(user_id))
    current_page = user_pages.get(user_id, 1)
    if page_id == '+1':
        current_page += 1
    elif page_id == '-1' and current_page > 1:
        current_page -= 1

    user_pages[user_id] = current_page

    ikb = InlineKeyboardBuilder()
    ikb.add(
        InlineKeyboardButton(text='➖', callback_data='page_-1'),
        InlineKeyboardButton(text=str(current_page), callback_data=f'current_page_{current_page}'),
        InlineKeyboardButton(text='➕', callback_data='page_+1'),
        InlineKeyboardButton(text='◀️ Orqaga', callback_data='go_back'),
        InlineKeyboardButton(text="🛒 Savatga qo'shish", callback_data='add'),
    )


    ikb.adjust(3, 2, repeat=True)
    await callback.message.edit_reply_markup(reply_markup=ikb.as_markup())

@callback_router.callback_query(F.data == 'go_back')
async def go_back_handler(callback_query: CallbackQuery):
    await callback_query.message.delete()
    categories = await Category.get_all()
    ikb = InlineKeyboardBuilder()
    for category in categories:
        ikb.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))
    ikb.add(InlineKeyboardButton(text='🔍Qidirish', callback_data='search'))
    ikb.adjust(2, repeat=True)
    await callback_query.message.answer('kategoriyani birini tanlang:', reply_markup=ikb.as_markup())


@callback_router.callback_query(F.data == 'add')
async def add_handler(callback_query: CallbackQuery):
    quantity_of_order = 0
    real_user_id = callback_query.from_user.id
    user_id = callback_query.message.from_user.id
    quantity_of_books = user_pages[user_id]
    product_id = user_pages.get('product_id')
    category_id = user_pages.get('category_id')

    if product_id is not None and category_id is not None:
        await Order.create(user_id=real_user_id, category_id=category_id, product_id=product_id, quantity_of_books=quantity_of_books)
        await callback_query.message.delete()
        await callback_query.answer('🛒Savatga qoshildi 😊', show_alert=True)
    else:
        await callback_query.answer('Mahsulot topilmadi ‼️', show_alert=True)


    categories = await Category.get_all()
    ikb = InlineKeyboardBuilder()
    orders = await Order.get_all()
    for order in orders:
        if order.user_id == real_user_id:
            quantity_of_order += 1

    for category in categories:
        ikb.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))
    ikb.add(InlineKeyboardButton(text='🔍Qidirish', callback_data='search'),
            InlineKeyboardButton(text=f'🛒Savat ({quantity_of_order})', callback_data='quantity_of_order'))
    ikb.adjust(2, repeat=True)
    await callback_query.message.answer('kategoriyani birini tanlang:', reply_markup=ikb.as_markup())

@callback_router.callback_query(F.data.startswith('quantity_of_order'))
async def quantity_of_order_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    total_price = 0
    ikb = InlineKeyboardBuilder()
    ikb.add(
        InlineKeyboardButton(text='❌Savatni tozalash', callback_data='order_delete'),
        InlineKeyboardButton(text='✅Buyurtmani tasdiqlash', callback_data='order_create'),
        InlineKeyboardButton(text='◀️ Orqaga', callback_data='go_back'),
    )
    ikb.adjust(1, repeat=True)

    text = """
    🛒 Savat 
    
"""

    orders = await Order.get_all()
    for order in orders:
        if order.user_id == user_id:
            product = await Product.get(order.product_id)
            total_price += product.price
            text += f"{product.name}\n{order.quantity_of_books} x {product.price} = {product.price*order.quantity_of_books}\n"
            text += '\n'
    text += f"Jami:{total_price}"
    user_pages['text'] = text
    await callback.message.answer(text, reply_markup=ikb.as_markup())

@callback_router.callback_query(F.data.startswith('order'))
async def order_handler(callback_query: CallbackQuery, bot: Bot):
    order_info = callback_query.data.split('order_')[-1]
    user_id = callback_query.from_user.id
    orders = await Order.get_all()
    order_ids = []
    for order in orders:
        if order.user_id == user_id:
            order_ids.append(order.id)

    if order_info == 'delete':
        for order_id in order_ids:
            await Order.delete(order_id)

        await callback_query.message.delete()
        await callback_query.answer('🛒 Savat tozalandi', show_alert=True)
    elif order_info == 'create':
        text = user_pages.get('text')
        await bot.send_message(chat_id=ADMIN, text=text)
























import asyncio
import os
from ctypes import LibraryLoader

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

load_dotenv()

print("BOT_TOKEN найден:", os.getenv("BOT_TOKEN") is not None)
print("APPLICATION_CHAT_ID:", os.getenv("APPLICATION_CHAT_ID"))

TOKEN = os.getenv("BOT_TOKEN")
APPLICATION_CHAT_ID = int(os.getenv("APPLICATION_CHAT_ID"))

dp = Dispatcher()

class ConsultationForm(StatesGroup):
    full_name = State()
    phone = State()
    city = State()
    product = State()

#Main menu (returning user here after success application)
def main_menu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="👤 Я клиент",
                callback_data="client"
            )],
            [InlineKeyboardButton(
                text="🤝 Я партнёр",
                callback_data="partner"
            )]
        ]
    )

@dp.message(CommandStart())
async def start_handler(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📄 Читать Политику",
                    url="https://example.com/policy"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📜 Читать Оферту",
                    url="https://example.com/offer"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Я ознакомлен(-а) с Политикой, Офертой и даю полное согласие",
                    callback_data="agree"
                )
            ]
        ]
    )

    await message.answer(
        "Здравствуйте! Официальный интерактивный помощник команды Atomy.\n"
        "Мы помогаем подобрать оригинальную корейскую продукцию напрямую "
        "с заводов Южной Кореи и защищаем от подделок с маркетплейсов.\n\n"
        "Прежде чем мы начнем, пожалуйста, подтвердите ознакомление "
        "с правовыми документами:\n\n"
        "📄 Политика обработки персональных данных (ФЗ-152)\n"
        "📜 Публичная оферта сервиса\n"
        "📬 Согласие на получение информационно-рекламных рассылок (ФЗ-38)",
        reply_markup=keyboard
    )


@dp.callback_query(lambda callback: callback.data == "agree")
async def agree_handler(callback: CallbackQuery):
    await callback.answer()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👤 Я клиент",
                    callback_data="client"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🤝 Я партнёр",
                    callback_data="partner"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        "Отлично! 👋\n\n"
        "Добро пожаловать в Atomy Kvant!\n"
        "Пожалуйста, выберите нужный раздел:",
        reply_markup=keyboard
    )

@dp.callback_query(lambda callback: callback.data == "client")
async def client_handler(callback: CallbackQuery):
    await callback.answer()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🧴 Мунивер / ХемоХИМ",
                    callback_data="muniver"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✨ Набор Absolute",
                    callback_data="absolute"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📞 Получить консультацию / Заказать товар",
                    callback_data="consultation"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌐 Посмотреть полный каталог",
                    callback_data="catalog"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎁 Как покупать по оптовой цене Кореи",
                    callback_data="wholesale"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        "👤 Клиентский раздел\n\n"
        "Здесь вы можете ознакомиться с продукцией "
        "Atomy, посмотреть каталог или получить консультацию.",
        reply_markup=keyboard
    )

@dp.callback_query(lambda callback: callback.data == "muniver")
async def muniver_handler(callback: CallbackQuery):
    await callback.answer()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="client"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        "🧴 Мунивер / ХемоХИМ\n\n"
        "Комплекс продуктов Atomy на основе HemoHIM.\n\n"
        "💰 Стоимость:\n"
        "• Гостевая цена — 2 600 ₽\n"
        "• Клубная цена — 2 000 ₽\n"
        "• 15 000 PV\n\n"
        "Если хотите узнать подробнее или оформить заказ, "
        "вернитесь в клиентский раздел и выберите "
        "«📞 Получить консультацию / Заказать товар».",
        reply_markup=keyboard
    )

@dp.callback_query(lambda callback: callback.data == "absolute")
async def absolute_handler(callback: CallbackQuery):
    await callback.answer()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="client"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        "🧴 Комплект Absolute\n\n"
        "Комплекс продуктов Atomy на основе HemoHIM.\n\n"
        "💰 Стоимость:\n"
        "• Гостевая цена — 18 000 ₽\n"
        "• Клубная цена — 15 000 ₽\n"
        "• 100 000 PV\n\n"
        "Если хотите узнать подробнее или оформить заказ, "
        "вернитесь в клиентский раздел и выберите "
        "«📞 Получить консультацию / Заказать товар».",
        reply_markup=keyboard
    )


@dp.callback_query(lambda callback: callback.data == "consultation")
async def consultation_handler(
    callback: CallbackQuery,
    state: FSMContext
):
    await callback.answer()

    await state.set_state(ConsultationForm.full_name)

    await callback.message.edit_text(
        "📞 Консультация / Заказ товара\n\n"
        "Давайте оформим заявку.\n\n"
        "Пожалуйста, напишите ваше ФИО:"
    )

@dp.message(ConsultationForm.full_name)
async def process_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)

    await state.set_state(ConsultationForm.phone)

    await message.answer(
        "📱 Отлично!\n\n"
        "Теперь отправьте ваш номер телефона."
    )

@dp.message(ConsultationForm.phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)

    await state.set_state(ConsultationForm.city)

    await message.answer(
        "🌍 Супер!\n\n"
        "Теперь напишите ваш город."
    )

@dp.message(ConsultationForm.city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)

    await state.set_state(ConsultationForm.product)

    await message.answer(
        "🛍 Отлично!\n\n"
        "Теперь напишите, какой товар вас интересует "
        "или задайте свой вопрос"
    )

@dp.message(ConsultationForm.product)
async def process_product(message: Message, state: FSMContext):
    await state.update_data(product=message.text)

    data = await state.get_data()

    #Receiving information about telegram-username
    username = message.from_user.username
    username_text = f"@{username}" if username else "не указан"

    #Forming an application
    application_text = (
        "🆕 НОВАЯ ЗАЯВКА\n\n"
        f"👤 ФИО: {data['full_name']}\n"
        f"📱 Телефон: {data['phone']}\n"
        f"🌍 Город: {data['city']}\n"
        f"🛍 Товар / вопрос: {data['product']}\n\n"
        f"🆔 Telegram ID: {message.from_user.id}\n"
        f"👤 Username: {username_text}"
    )

    #Sending application in work group
    await message.bot.send_message(
        chat_id=APPLICATION_CHAT_ID,
        text=application_text
    )

    #Cleaning FSM after success sending
    await state.clear()

    #Returning the user to the main menu
    keyboard = main_menu_keyboard()

    await message.answer(
        "✅ Спасибо! Ваша заявка успешно отправлена\n\n"
        "Мы получили ваши данные и скоро с вами свяжемся\n\n"
        "Вы можете продолжить работу с ботом:",
        reply_markup=keyboard
    )


#test checking
@dp.message()
async def get_chat_id(message: Message):
    print(f"CHAT ID: {message.chat.id}")
    print(f"CHAT TYPE: {message.chat.type}")
    print(f"CHAT TITLE: {message.chat.title}")


async def main():
    bot = Bot(token=TOKEN)
    me = await bot.get_me()

    print(f"Бот подключён: @{me.username}")
    print(f"Имя: {me.first_name}")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())

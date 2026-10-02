import asyncio
import os
from ast import parse
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
print("BOT_VERSION:", os.getenv("BOT_VERSION"))

TOKEN = os.getenv("BOT_TOKEN")
APPLICATION_CHAT_ID = int(os.getenv("APPLICATION_CHAT_ID"))
BOT_VERSION = str(os.getenv("BOT_VERSION", "unknown"))


dp = Dispatcher()

class ConsultationForm(StatesGroup):
    full_name = State()
    phone = State()
    city = State()
    product = State()

class PartnerForm(StatesGroup):
    full_name = State()
    name = State()
    city = State()
    experience = State()

class MarinaQuestionForm(StatesGroup):
    question = State()

#Showing bot-version below
def with_version(text: str) -> str:
    return f"{text}\n\n\n<i>AtomyKvantBot v{BOT_VERSION}</i>"

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
        with_version(
            "Здравствуйте! <b>Вас приветсвует Официальный интерактивный помощник команды Atomy</b>\n"
            "Мы помогаем подобрать оригинальную корейскую продукцию напрямую "
            "с заводов Южной Кореи и защищаем от подделок с маркетплейсов.\n\n"
            "Прежде чем мы начнем, пожалуйста, подтвердите ознакомление "
            "с правовыми документами:\n\n"
            "📄 <i>Политика обработки персональных данных (ФЗ-152)</i>\n"
            "📜 <i>Публичная оферта сервиса</i>\n"
            "📬 <i>Согласие на получение информационно-рекламных рассылок (ФЗ-38)</i>",
           ),
            parse_mode="HTML",
            reply_markup=keyboard

    )


def main_menu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌿 Подобрать уход / Защита от подделок Ozon",
                    callback_data="client"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💰 Узнать про доход и партнерство",
                    callback_data="partner"
                )
            ]
        ]
    )

@dp.callback_query(lambda callback: callback.data == "main_menu")
async def main_menu_handler(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        "Вас вновь приветствует <b>команда Atomy</b>! ✅\n\n"
        "Мы представляем вам качественные и оригинальные товары на любой вкус от корейской компании! 🌐\n\n"
        "Пожалуйста, выберите что вас интересует:",
        parse_mode="HTML",
        reply_markup=main_menu_keyboard()
    )

@dp.callback_query(lambda callback: callback.data == "agree")
async def agree_handler(callback: CallbackQuery):
    await callback.answer()

    keyboard = main_menu_keyboard()

    await callback.message.edit_text(
        "Здравствуйте! 👋\n\n"
        "Вас вновь приветствует <b>команда Atomy</b>! ✅\n\n"
        "Мы представляем вам качественные и оригинальные товары на любой вкус от корейской компании! 🌐\n\n"
        "Пожалуйста, выберите что вас интересует:",
        parse_mode="HTML",
        reply_markup=keyboard
    )


@dp.callback_query(lambda callback: callback.data == "client")
async def client_handler(callback: CallbackQuery):
    await callback.answer()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
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
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="main_menu"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        "🌿 <b>Клиентский раздел</b>\n\n"
        "Здесь вы можете подобрать продукцию Atomy, "
        "узнать цены и получить помощь с заказом.\n\n"

        "🧴 <b>Мунивер / ХемоХИМ</b>\n"
        "Здоровье и суставы\n"
        "💰 <u>2 000 ₽</u>\n"
        "⭐ <u>15 000 PV</u>\n\n"

        "✨ <b>Набор Absolute</b>\n"
        "Омоложение кожи\n"
        "💰 <u>15 000 ₽</u>\n"
        "⭐ <u>100 000 PV</u>\n\n"

        "<b>⚠️ Важно про Ozon</b>\n"
        "На маркетплейсах могут встречаться товары "
        "неофициального происхождения. "
        "Перед покупкой рекомендуем проверить источник продукции.",
        parse_mode="HTML",
        reply_markup=keyboard
    )

@dp.callback_query(lambda callback: callback.data == "catalog")
async def catalog_handler(callback: CallbackQuery):
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
                    text="⬅️ Назад",
                    callback_data="client"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        with_version(
            "🧴 <b>Каталог флагманов</b>\n\n"
            "Выберите интересующий продукт:"
        ),
        parse_mode="HTML",
        reply_markup=keyboard
    )
@dp.callback_query(lambda callback: callback.data == "wholesale")
async def wholesale_handler(callback: CallbackQuery):
    await callback.answer()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📞 Получить консультацию",
                    callback_data="consultation"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="client"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        with_version(
            "🎁 <i>Как покупать по оптовой цене Кореи?</i>\n\n"
            "После бесплатной регистрации в клубе Atomy "
            "вы сможете покупать продукцию по клубной цене.\n\n"
            "Например:\n\n"
            "🧴 <b>Мунивер / ХемоХИМ</b>\n"
            "<u>Гостевая цена — 2 600 ₽</u>\n"
            "<u>Клубная цена — 2 000 ₽</u>\n\n"
            "✨ <b>Absolute</b>\n"
            "<u>Гостевая цена — 18 000 ₽</u>\n"
            "<u>Клубная цена — 15 000 ₽</u>\n\n"
            "Чтобы узнать подробнее о регистрации, "
            "получить консультацию или оформить заказ, "
            "нажмите кнопку ниже."
        ),
        parse_mode="HTML",
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
                    callback_data="catalog"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        "🧴 <b>Мунивер / ХемоХИМ</b>\n\n"
        "Комплекс продуктов Atomy на основе HemoHIM.\n\n"
        "💰 Стоимость:\n"
        "<u>Гостевая цена — 2 600 ₽</u>\n"
        "<u>Клубная цена — 2 000 ₽</u>\n"
        "<u>15 000 PV</u>\n\n"
        "Если хотите узнать подробнее или оформить заказ, "
        "вернитесь в клиентский раздел и выберите "
        "«📞 <b>Получить консультацию / Заказать товар».</b>",
        parse_mode="HTML",
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
                    callback_data="catalog"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        "🧴 <b>Комплект Absolute</b>\n\n"
        "Комплекс продуктов Atomy на основе HemoHIM.\n\n"
        "💰 Стоимость:\n"
        "<u>Гостевая цена — 18 000 ₽</u>\n"
        "<u>Клубная цена — 15 000 ₽</u>\n"
        "<u>100 000 PV</u>\n\n"
        "Если хотите узнать подробнее или оформить заказ, "
        "вернитесь в клиентский раздел и выберите "
        "«📞 <b>Получить консультацию / Заказать товар».</b>",
        parse_mode="HTML",
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
        "📞 <b>Консультация / Заказ товара</b>\n\n"
        "Давайте оформим заявку\n\n"
        "Пожалуйста, напишите <u>ваше ФИО</u>:",
        parse_mode="HTML",
    )

@dp.message(ConsultationForm.full_name)
async def process_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)

    await state.set_state(ConsultationForm.phone)

    await message.answer(
        "📞 <b>Консультация / Заказ товара</b>\n\n"
        "Теперь отправьте <u>ваш номер телефона</u>:",
        parse_mode = "HTML",
    )

@dp.message(ConsultationForm.phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)

    await state.set_state(ConsultationForm.city)

    await message.answer(
        "📞 <b>Консультация / Заказ товара</b>\n\n"
        "Теперь напишите <u>ваш город</u>:",
        parse_mode = "HTML",
    )

@dp.message(ConsultationForm.city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)

    await state.set_state(ConsultationForm.product)

    await message.answer(
        "📞 <b>Консультация / Заказ товара</b>\n\n"
        "Теперь напишите, какой товар вас интересует"
        "или задайте свой вопрос",
        parse_mode = "HTML",
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
        "✅ <b>Спасибо! Ваша заявка успешно отправлена</b>\n\n"
        "Мы получили ваши данные и скоро с вами свяжемся\n\n"
        "Вы можете продолжить работу с ботом:",
        parse_mode="HTML",
        reply_markup=keyboard
    )

@dp.callback_query(lambda callback: callback.data == "partner_application")
async def partner_application_handler(
    callback: CallbackQuery,
    state: FSMContext
):
    await callback.answer()

    await state.set_state(PartnerForm.name)

    await callback.message.edit_text(
        "🚀 <b>Заявка на собеседование</b>\n\n"
        "Для начала напишите <u>ваше имя</u>:",
        parse_mode = "HTML"
    )


@dp.message(PartnerForm.name)
async def process_partner_name(
    message: Message,
    state: FSMContext
):
    await state.update_data(partner_name=message.text)

    await state.set_state(PartnerForm.city)

    await message.answer(
        "🚀 <b>Заявка на собеседование</b>\n\n"
        "Теперь напишите <u>ваш город:</u>",
        parse_mode="HTML"
    )


@dp.message(PartnerForm.city)
async def process_partner_city(
    message: Message,
    state: FSMContext
):
    await state.update_data(partner_city=message.text)

    await state.set_state(PartnerForm.experience)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Да",
                    callback_data="experience_yes"
                ),
                InlineKeyboardButton(
                    text="❌ Нет",
                    callback_data="experience_no"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🟡 Немного",
                    callback_data="experience_some"
                )
            ]
        ]
    )

    await message.answer(
        "🚀 <b>Заявка на собеседование</b>\n\n"
        "Есть ли у вас опыт в продажах, "
        "бьюти-сфере или сетевом бизнесе?",
        parse_mode="HTML",
        reply_markup=keyboard
    )

@dp.callback_query(
    PartnerForm.experience,
    lambda callback: callback.data in {
        "experience_yes",
        "experience_no",
        "experience_some"
    }
)
async def process_partner_experience(
    callback: CallbackQuery,
    state: FSMContext
):
    print("🔥 EXPERIENCE HANDLER ЗАПУЩЕН")
    print("🔥 callback.data:", callback.data)

    await callback.answer()

    experience_map = {
        "experience_yes": "Да",
        "experience_no": "Нет",
        "experience_some": "Немного"
    }

    experience = experience_map[callback.data]

    print("🔥 Выбранный опыт:", experience)

    await state.update_data(experience=experience)

    data = await state.get_data()

    print("🔥 DATA:", data)

    username = callback.from_user.username
    username_text = f"@{username}" if username else "не указан"

    application_text = (
        "🎯 ЗАЯВКА НА ПАРТНЁРСТВО В КОМАНДУ\n\n"
        f"👤 Имя: {data['partner_name']}\n"
        f"🏙 Город: {data['partner_city']}\n"
        f"💼 Опыт: {data['experience']}\n\n"
        f"🆔 Telegram ID: {callback.from_user.id}\n"
        f"👤 Username: {username_text}"
    )

    print("🔥 Заявка сформирована:")
    print(application_text)

    try:
        await callback.bot.send_message(
            chat_id=APPLICATION_CHAT_ID,
            text=application_text
        )

        print("✅ Заявка успешно отправлена в чат")

    except Exception as e:
        print("❌ ОШИБКА ПРИ ОТПРАВКЕ ЗАЯВКИ:")
        print(repr(e))

        await callback.message.answer(
            "❌ Произошла ошибка при отправке заявки."
        )

        return

    await state.clear()

    print("✅ FSM очищен")

    await callback.message.edit_text(
        "✅ <b>Заявка успешно отправлена!</b>\n\n"
        "Марина получила ваши данные и свяжется с вами "
        "для дальнейшего общения\n\n"
        "<u>Спасибо за интерес к команде Atomy!</u>\n\n"
        "Вы можете продолжить работу с ботом:",
        parse_mode = "HTML",
        reply_markup=main_menu_keyboard()
    )

    print("✅ Сообщение пользователю изменено")

#test checking
#@dp.message()
#async def get_chat_id(message: Message):
#    print(f"CHAT ID: {message.chat.id}")
#    print(f"CHAT TYPE: {message.chat.type}")
#    print(f"CHAT TITLE: {message.chat.title}")


@dp.callback_query(lambda callback: callback.data == "partner")
async def partner_handler(callback: CallbackQuery):
    await callback.answer()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➡️ Как именно здесь зарабатывают деньги?",
                    callback_data="partner_income"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="main_menu"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        (
            "💰 <b>Партнёрская программа</b>\n\n"
            "Давайте честно: <u>почему 90% людей боятся слова "
            "«сетевой»?</u>\n\n"
            "Потому что людей часто заставляют каждый месяц "
            "покупать ненужный товар, бегать с каталогами и "
            "впаривать продукцию знакомым.\n\n"
            "В Atomy всё устроено иначе:\n\n"
            "1. <b>НЕТ</b> обязательных ежемесячных закупок.\n"
            "Вы покупаете только то, что действительно нужно.\n\n"
            "2. Ваши личные баллы (PV) <b>НЕ СГОРАЮТ</b>.\n\n"
            "3. Доход формируется от общего товарооборота "
            "двух веток структуры."
        ),
        parse_mode="HTML",
        reply_markup=keyboard
    )


@dp.callback_query(lambda callback: callback.data == "partner_income")
async def partner_income_handler(callback: CallbackQuery):
    await callback.answer()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➡️ Какую поддержку дает наша команда?",
                    callback_data="partner_support"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="partner"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        (
            "💰 <b>Откуда берутся выплаты?</b>\n\n"
            "Вы бесплатно регистрируетесь, пробуете продукцию "
            "и рассказываете о ней друзьям или знакомым.\n\n"
            "Баллы за покупки суммируются в вашей левой "
            "и правой ветке.\n\n"
            "Когда в структуре накапливается необходимый "
            "оборот, формируются выплаты.\n\n"
            "<u>Semi-Master — от 15 000 до 30 000 ₽ в месяц</u>\n"
            "<u>Master — от 60 000 до 120 000 ₽ в месяц</u>\n\n"
            "<i>Логику доставки, склад, сертификацию и разработку "
            "берёт на себя корпорация Atomy.</i>"
        ),
        parse_mode="HTML",
        reply_markup=keyboard
    )

@dp.callback_query(lambda callback: callback.data == "ask_marina")
async def ask_marina_handler(
    callback: CallbackQuery,
    state: FSMContext
):
    print("🔥 ASK MARINA HANDLER ЗАПУЩЕН")

    await callback.answer()

    await state.set_state(MarinaQuestionForm.question)

    print("🔥 STATE УСТАНОВЛЕН:", await state.get_state())

    await callback.message.edit_text(
        "❓ <b>Вопрос Марине</b>\n\n"
        "Напишите ваш вопрос <u>одним сообщением</u>:",
        parse_mode="HTML"
    )

@dp.message(MarinaQuestionForm.question)
async def process_marina_question(
    message: Message,
    state: FSMContext
):
    print("🔥 MARINA QUESTION HANDLER ЗАПУЩЕН")
    print(f"🔥 Текст вопроса: {message.text}")
    print(f"🔥 APPLICATION_CHAT_ID: {APPLICATION_CHAT_ID}")

    username = message.from_user.username
    username_text = f"@{username}" if username else "не указан"

    question_text = (
        "❓ ВОПРОС МАРИНЕ\n\n"
        f"💬 Вопрос:\n{message.text}\n\n"
        f"🆔 Telegram ID: {message.from_user.id}\n"
        f"👤 Username: {username_text}"
    )

    print("🔥 ВОПРОС СФОРМИРОВАН:")
    print(question_text)

    try:
        print("🔥 ПЫТАЕМСЯ ОТПРАВИТЬ В ЧАТ...")

        await message.bot.send_message(
            chat_id=APPLICATION_CHAT_ID,
            text=question_text
        )

        print("✅ ВОПРОС УСПЕШНО ОТПРАВЛЕН В ЧАТ")

    except Exception as e:
        print("❌ ОШИБКА ПРИ ОТПРАВКЕ ВОПРОСА:")
        print(repr(e))

        await message.answer(
            "⚠️ Не удалось отправить вопрос Марине.\n"
            "Попробуйте ещё раз позже."
        )
        return

    await state.clear()

    await message.answer(
        "✅ <b>Ваш вопрос отправлен Марине!</b>\n\n"
        "Она свяжется с вами, когда сможет\n\n"
        "Вы можете продолжить работу с ботом:",
        parse_mode="HTML",
        reply_markup=main_menu_keyboard()
    )

@dp.callback_query(lambda callback: callback.data == "partner_support")
async def partner_support_handler(callback: CallbackQuery):
    await callback.answer()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Хочу пройти собеседование",
                    callback_data="partner_application"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❓ Задать вопрос Марине",
                    callback_data="ask_marina"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="partner_income"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        with_version(
            "🤝 <b>Поддержка нашей команды</b>\n\n"
            "Вам не придётся самостоятельно придумывать, "
            "что писать и где искать людей.\n\n"
            "Наша команда предоставляет:\n\n"
            "1. <i>Готовый Telegram-бот с персональным QR-кодом.</i>\n"
            "2. <i>Банк готового контента.</i>\n"
            "3. <i>Помощь Марины и лидеров команды.</i>\n"
            "4. <i>Обучение работе с бьюти-мастерами "
            "и локальными площадками.</i>"
        ),
        parse_mode="HTML",
        reply_markup=keyboard
    )


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
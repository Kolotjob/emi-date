from aiogram import Router, types, F
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InputMediaPhoto,
    InputMediaVideo,
    ReplyKeyboardRemove
)
from aiogram.fsm.context import FSMContext

import math
import ssl
import certifi
from geopy.geocoders import Nominatim
from tortoise.expressions import Q

from src.models import User as Userdb, Like, Block
from src.utils.state import SearchPeople

router = Router()

# -----------------------------
# Словари переводов
# -----------------------------
INTERESTS = [
    (1, "Спорт", "Sport"), (2, "Музыка", "Music"), (3, "Путешествия", "Travel"), 
    (4, "Кино", "Movies"), (5, "Кулинария", "Cooking"), (6, "Искусство", "Art"), 
    (7, "Танцы", "Dancing"), (8, "Технологии", "Technology"), (9, "Литература", "Literature"), 
    (10, "Фотография", "Photography"), (11, "Игры", "Games"), (12, "Природа", "Nature"), 
    (13, "Автомобили", "Cars"), (14, "Мода", "Fashion"), (15, "Здоровье", "Health"),
    (16, "Йога", "Yoga"), (17, "Фитнес", "Fitness"), (18, "Астрономия", "Astronomy"), 
    (19, "История", "History"), (20, "Наука", "Science"), (21, "Театр", "Theater"), 
    (22, "Видеомонтаж", "Video Editing"), (23, "Рыбалка", "Fishing"), (24, "Охота", "Hunting"), 
    (25, "Гаджеты", "Gadgets"), (26, "Киберспорт", "Esports"), (27, "Комиксы", "Comics"), 
    (28, "Рукоделие", "Handcraft"), (29, "Медицина", "Medicine"), (30, "Животные", "Animals"),
    (31, "Астрология", "Astrology"), (32, "Эзотерика", "Esoterics"), (33, "Психология", "Psychology"), 
    (34, "Планирование", "Planning"), (35, "Волонтёрство", "Volunteering"), (36, "Блогинг", "Blogging"), 
    (37, "Дизайн", "Design"), (38, "Флористика", "Floristry"), (39, "Косплей", "Cosplay"), 
    (40, "Программирование", "Programming"), (41, "Мотоспорт", "Motor Sports"), 
    (42, "Философия", "Philosophy"), (43, "Чтение", "Reading"), (44, "Коллекционирование", "Collecting"),
    (45, "Лыжи", "Skiing"), (46, "Сноуборд", "Snowboarding"), (47, "Дайвинг", "Diving"), 
    (48, "Кемпинг", "Camping"), (49, "Плавание", "Swimming"), (50, "Бег", "Running"), 
    (51, "Туризм", "Hiking"), (52, "Стрельба", "Shooting"), (53, "Гольф", "Golf"), 
    (54, "Шахматы", "Chess"), (55, "Настольные игры", "Board Games"), (56, "Журналистика", "Journalism"), 
    (57, "Инвестирование", "Investing"), (58, "Кулинария", "Cooking"), (59, "Садоводство", "Gardening"), 
    (60, "Языковой обмен", "Language Exchange"),
]

PREFERENCES = {
    "ru": {
        "friendship": "🤝 Дружба",
        "romantic": "❤️ Романтические отношения",
        "partnership": "💼 Партнерство в проектах",
        "emigration": "🌍 Общение на тему эмиграции"
    },
    "en": {
        "friendship": "🤝 Friendship",
        "romantic": "❤️ Romantic relationships",
        "partnership": "💼 Partnership in projects",
        "emigration": "🌍 Discussion about emigration"
    }
}

GENDER = {
    "ru": {"fem": "👩 Женский", "mal": "👨 Мужской", "oth": "🌈 Другое"},
    "en": {"fem": "👩 Female", "mal": "👨 Male", "oth": "🌈 Other"}
}

WHO = {
    "ru": {"fem": "👩 Девушки", "mal": "👨 Парни", "all": "🌍 Все"},
    "en": {"fem": "👩 fem", "mal": "👨 mal", "all": "🌍 Everyone"}
}

ORI = {
    "ru": {
        "hetero": "❤️ Гетеро",
        "gay": "🌈 Гей",
        "bi": "💛 Би",
        "lesbian": "💖 Лесби",
        "gay_lesbian": "🌈 Гей/Лесби",
        "oth": "💫 Другая",
        "skip": "Не указана"
    },
    "en": {
        "hetero": "❤️ Hetero",
        "gay": "🌈 Gay",
        "bi": "💛 Bi",
        "lesbian": "💖 Lesbian",
        "gay_lesbian": "🌈 Gay/Lesbian",
        "oth": "💫 Other",
        "skip": "Not specified"
    }
}

# -----------------------------
# Вспомогательные функции
# -----------------------------
@router.message(F.text.in_(["❤️ Лайк", "💖 Суперлайк", "👎🏻 Дизлайк", "🚫 Заблокировать", "❗ Пожаловаться", "⏹ Остановить поиск",
                             "❤️ Like", "💖 Superlike", "👎🏻 Dislike", "🚫 Block", "❗ Report", "⏹ Stop Search"]))
async def handle_reaction(message: types.Message, state: FSMContext):
    user = await Userdb.get_or_none(user_id=message.from_user.id)
    if not user:
        await message.answer("Профиль не найден.")
        return

    reaction = message.text
    if reaction in ["⏹ Остановить поиск", "⏹ Stop Search"]:
        await state.clear()
        await message.answer("Поиск остановлен.", reply_markup=ReplyKeyboardRemove())
        return

    data = await state.get_data()
    current_candidate_id = data.get("current_candidate_id")
    if not current_candidate_id:
        await message.answer("Нет текущей анкеты для оценки. Попробуйте начать поиск заново.")
        return

    candidate = await Userdb.get_or_none(user_id=current_candidate_id)
    if not candidate:
        await message.answer("Ошибка: кандидат не найден.")
        return

    if reaction in ["❤️ Лайк", "❤️ Like"]:
        await Like.create(from_user=user, to_user=candidate, is_superlike=False)
        # Если у пользователя Free-подписка, уведомляем, что для просмотра полного профиля необходимо оформить подписку.
        if user.subscription.lower() == "free":
            await message.answer("Вы получили лайк! Чтобы увидеть подробности профиля кандидата, необходимо приобрести подписку.")
            # Здесь можно добавить дополнительную логику для перенаправления на страницу покупки подписки.
        else:
            await message.answer("Вы поставили лайк!")
    elif reaction in ["💖 Суперлайк", "💖 Superlike"]:
        if user.subscription.lower() != "free":
            await Like.create(from_user=user, to_user=candidate, is_superlike=True)
            await message.answer("Вы поставили суперлайк!")
        else:
            await message.answer("Суперлайк доступен только при платной подписке.")
    elif reaction in ["👎🏻 Дизлайк", "👎🏻 Dislike"]:
        await message.answer("Вы дизлайкнули кандидата.")
    elif reaction in ["🚫 Заблокировать", "🚫 Block"]:
        await Block.create(from_user=user, to_user=candidate, can_message=False)
        await message.answer("Кандидат заблокирован.")
    elif reaction in ["❗ Пожаловаться", "❗ Report"]:
        # Здесь можно добавить логику обработки жалобы.
        await message.answer("Вы отправили жалобу.")
    else:
        await message.answer("Неверная команда.")

    # После обработки реакции, если реакция не связана с остановкой поиска, показываем следующего кандидата.
    await start_search(user, state, message.bot)

# -----------------------------
# Хендлер для кнопки "Начать поиск"
# -----------------------------
@router.message(F.text.in_(["🚀 Начать поиск", "🚀 Start Search"]))
async def handle_search_start(message: types.Message, state: FSMContext):
    user = await Userdb.get_or_none(user_id=message.from_user.id)
    if not user:
        await message.answer(
            "<b>Профиль не найден.</b> Пожалуйста, зарегистрируйтесь с помощью команды /start."
        )
        return

    lang = user.lang or ("ru" if message.from_user.language_code == "ru" else "en")
    await state.set_state(SearchPeople.search)
    await message.answer(
        "🔎 Поиск начался! Ожидайте…" if lang == "ru" else "🔎 The search has begun! Please wait…"
    )
    await start_search(user, state, message.bot)

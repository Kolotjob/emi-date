from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from src.models import User
from aiogram.types import Message
from typing import Callable, Awaitable, Dict, Any, List
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext, BaseStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from src.utils.state import SearchPeople
from src.utils.add_profile import add_profile
from aiogram.types import ContentType


router = Router()

from tortoise.expressions import Q
from tortoise.query_utils import Prefetch
from typing import List
import math

# Функция для расчета расстояния между двумя точками (в километрах)
def calculate_distance(lat1, lon1, lat2, lon2):
    radius = 6371  # Радиус Земли в километрах
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return radius * c

# Основная функция для поиска ближайших пользователей
async def find_nearby_users(user: User, max_distance: float = 5000.0) -> List[User]:
    if not user.location:
        return []

    user_lat, user_lon = map(float, user.location.split(","))
    
    # Поиск пользователей, соответствующих фильтрам
    potential_users = await User.filter(
        Q(status_block="Active") &
        Q(location__isnull=False) &
        ~Q(id=user.id) &  # Исключаем самого пользователя
        ~Q(received_likes__from_user=user) &  # Исключаем уже лайкнутых
        ~Q(blocked_by__from_user=user)  # Исключаем заблокированных
    ).prefetch_related(
        Prefetch("received_likes"),
        Prefetch("blocked_by")
    )

    filtered_users = []

    for potential_user in potential_users:
        # Проверяем соответствие параметру for_whom
        if user.for_whom == "all" or user.for_whom == potential_user.gender:
            # Проверяем наличие хотя бы одного общего увлечения
            if user.hobbies and potential_user.hobbies:
                common_hobbies = set(user.hobbies) & set(potential_user.hobbies)
                if common_hobbies:
                    # Вычисляем расстояние между пользователями
                    potential_lat, potential_lon = map(float, potential_user.location.split(","))
                    distance = calculate_distance(user_lat, user_lon, potential_lat, potential_lon)

                    if distance <= max_distance:
                        # Добавляем пользователя в результаты
                        filtered_users.append((potential_user, distance))

    # Сортируем пользователей по расстоянию
    filtered_users.sort(key=lambda x: x[1])

    # Возвращаем отсортированный список пользователей
    return [user[0] for user in filtered_users]



@router.message(lambda message: message.text.lower() == ("🚀 Начать поиск" or "🚀 Start Search"))
async def handle_message1(message: types.Message, state: FSMContext, lang: str, user: User = None, user_none: bool = False):
    lang = lang if lang else ("ru" if message.from_user.language_code == "ru" else "en")

    if lang == "ru":
        txt = "🔎 Поиск начался! Используйте кнопки ниже для взаимодействия."
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="❤️ Лайк" if lang=="ru" else "❤️ Like"),
                    KeyboardButton(text="💖 Суперлайк" if lang=="ru" else "💖 Superlike"),
                ],
                [
                    KeyboardButton(text="👎🏻 Дизлайк" if lang=="ru" else "👎🏻 Dislike"),
                    KeyboardButton(text="🚫 Заблокировать" if lang=="ru" else "🚫 Block"),
                ],
                [
                    KeyboardButton(text="❗ Пожаловаться" if lang=="ru" else "❗ Report"),
                    KeyboardButton(text="⏹ Остановить поиск" if lang=="ru" else "⏹ Stop Search"),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    else:
        txt = "🔎 Search started! Use the buttons below to interact."
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="❤️ Like"),
                    KeyboardButton(text="💖 Superlike"),
                ],
                [
                    KeyboardButton(text="👎🏻 Dislike"),
                    KeyboardButton(text="🚫 Block"),
                ],
                [
                    KeyboardButton(text="❗ Report"),
                    KeyboardButton(text="⏹ Stop Search"),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

    await state.set_state(SearchPeople.search)
    await message.answer(txt, reply_markup=keyboard)
    await find_nearby_users(user)
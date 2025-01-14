from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from src.models import User,Like
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

# Словари переводов
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
        (57, "Инвестирование", "Investing"), (58, "Кулинария", "Cooking"), (59, "Садоводство", "Gardening"), (60, "Языковой обмен", "Language Exchange"),
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
    "ru": {
        "fem": "👩 Женский",
        "mal": "👨 Мужской",
        "oth": "🌈 Другое"
    },
    "en": {
        "fem": "👩 Female",
        "mal": "👨 Male",
        "oth": "🌈 Other"
    }
}

WHO = {
    "ru":{"girls":"👩 Девушки",
    "boys":"👨 Парни",
    "all":"🌍 Все"},
    "en":
    {
    "girls":"👩 Girls",
    "boys":"👨 Boys",
    "all":"🌍 Everyone"
    }
}

ORI={
        "ru":{
                "hetero":"❤️ Гетеро",
                "gay":"🌈 Гей",
                "bi":"💛 Би",
                "lesbian":"💖 Лесби",
                "gay_lesbian":"🌈 Гей/Лесби",
                "oth":"💫Другая",
                "skip":"Не указана"


        },
        "en":{
                "hetero":"❤️ Hetero",
                "gay":"🌈 Gay",
                "bi":"💛 Bi",
                "lesbian":"💖 Lesbian",
                "gay_lesbian":"🌈 Gay/Lesbian",
                "oth":"💫Other",
                "skip":"Not specified"
        }

}
MESSAGES = {
    "profile_not_found": {
        "ru": "<b>Профиль не найден.</b>\nПожалуйста, зарегистрируйтесь с помощью команды /start.",
        "en": "<b>Profile not found.</b>\nPlease register using the /start command."
    },
    "action_prompt": {
        "ru": "✏️ <b>Выберите действие:</b>",
        "en": "✏️ <b>Select an action:</b>"
    },
    "edit_name": {
        "ru": "Изменить имя",
        "en": "Edit Name"
    },
    "edit_age": {
        "ru": "Изменить возраст",
        "en": "Edit Age"
    },
    "edit_gender": {
        "ru": "Изменить пол",
        "en": "Edit Gender"
    },
    "reset_profile": {
        "ru": "Заполнить заново",
        "en": "Refill Profile"
    }
}

# Функция для расчета расстояния между двумя точками (в километрах)
def calculate_distance(lat1, lon1, lat2, lon2):
    radius = 6371  # Радиус Земли в километрах
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return radius * c

from geopy.geocoders import Nominatim
import ssl
import certifi
from aiogram.types import InputMediaPhoto, InputMediaVideo

def get_location_by_coordinates(latitude, longitude):
    geolocator = Nominatim(
        user_agent="my_geopy_app",
        timeout=10,
        ssl_context=ssl.create_default_context(cafile=certifi.where())
    )
    try:
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        if location:
            address = location.raw.get('address', {})
            city = address.get('city') or address.get('town') or address.get('village') or address.get('hamlet')
            return city or location.address
        else:
            return "Местоположение не найдено"
    except Exception as e:
        return f"Ошибка при определении местоположения: {e}"

async def find_suitable_profiles(user, lang):
    user_hobbies = set(user.hobbies or [])

    # Фильтрация пользователей
    potential_matches = await User.filter(
        status_block="Active",
        for_whom=user.gender,
    ).exclude(user_id=user.user_id)

    matches = []

    for potential_user in potential_matches:
        # Проверяем, лайкнул ли потенциальный пользователь текущего
        already_liked = await Like.filter(from_user=potential_user, to_user=user).exists()

        # Ищем общие увлечения
        hobbies_match = user_hobbies.intersection(set(potential_user.hobbies or []))

        if hobbies_match:
            # Рассчитываем расстояние
            if user.location and potential_user.location:
                user_lat, user_lon = map(float, user.location.split(","))
                potential_lat, potential_lon = map(float, potential_user.location.split(","))

                # Используем расчет расстояния (заменить на вашу реализацию)
                distance = calculate_distance(user_lat, user_lon, potential_lat, potential_lon)
            else:
                distance = None

            matches.append((potential_user, hobbies_match, already_liked, distance))

    # Сортируем по расстоянию (если расстояние указано)
    matches.sort(key=lambda x: x[3] if x[3] is not None else float('inf'))

    return matches

async def generate_profile_card(user, match, lang):
    hobbies_text = ", ".join([
        (interest[1] if lang == "ru" else interest[2])
        for interest in INTERESTS
        if str(interest[0]) in (match.hobbies or [])
    ])

    location_text = match.location or ("Локация не указана" if lang == "ru" else "Location not provided")
    if "," in location_text:
        latitude, longitude = map(float, location_text.split(","))
        location_text = get_location_by_coordinates(latitude, longitude)
    
    description = (
        f"<b>{match.name}</b> \n"
        f"<b>{'Возраст' if lang == 'ru' else 'Age'}:</b> {match.age}\n"
        f"{GENDER[lang][match.gender]}\n"
        f"<b>{'Ориентация' if lang == 'ru' else 'Orientation'}:</b> {ORI[lang][match.orientation]}\n"
        f"{location_text}\n"
        f"<b>{'Цели' if lang == 'ru' else 'Goals'}:</b> {PREFERENCES[lang][match.preferences]}\n"
        f"<b>{'Увлечения' if lang == 'ru' else 'Hobbies'}:</b> {hobbies_text}\n\n"
        f"{'Пользователь вас лайкнул!' if match.already_liked else ''}\n"
        f"_________________________\n{match.about or ''}\n"
    )

    media = match.medias or []
    if len(media) == 1:
        media_file = media[0]['file_id']
        if media[0]['type'] == 'photo':
            return InputMediaPhoto(media=media_file, caption=description)
        elif media[0]['type'] == 'video':
            return InputMediaVideo(media=media_file, caption=description)
    else:
        files = []
        i = 0
        for media_file in media:
            caption = description if i == 0 else None
            if media_file["type"] == "video":
                files.append(InputMediaVideo(media=media_file['file_id'], caption=caption))
                i += 1
            elif media_file['type'] == 'photo':
                files.append(InputMediaPhoto(media=media_file['file_id'], caption=caption))
                i += 1
        return files

async def start_search(user, state, bot):
    lang = user.lang if user.lang in ["ru", "en"] else "ru"
    matches = await find_suitable_profiles(user, lang)

    if not matches:
        await bot.send_message(user.user_id, "<b>Нет подходящих пользователей.</b>" if lang == "ru" else "<b>No suitable users found.</b>")
        return

    for match, hobbies_match, already_liked, distance in matches:
        profile_card = await generate_profile_card(user, match, lang)

        if isinstance(profile_card, list):
            await bot.send_media_group(user.user_id, profile_card)
        else:
            await bot.send_message(user.user_id, profile_card)


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
    await start_search(user, state, message.bot)
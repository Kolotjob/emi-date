from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMediaVideo
from src.models import User
from aiogram.filters import CommandStart, Command
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from src.models import User
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext, BaseStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from src.utils.state import RegState

router = Router()

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

import ssl
import certifi
from geopy.geocoders import Nominatim

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
    

@router.message(Command("myprofile"))
async def my_profile_handler(message: types.Message,state: FSMContext):
    user = await User.get_or_none(user_id=message.from_user.id)

    if not user:
        lang = "ru"
        await message.answer("<b>Профиль не найден.</b>\nПожалуйста, зарегистрируйтесь с помощью команды /start.")
        return

    lang = user.lang if user.lang in ["ru", "en"] else "ru"
    hobbies_text = ", ".join([
        (interest[1] if lang == "ru" else interest[2])
        for interest in INTERESTS
        if str(interest[0]) in (user.hobbies or [])
    ])

    location_text = user.location or ("Локация не указана" if lang == "ru" else "Location not provided")
    if "," in location_text:
        latitude, longitude = map(float, location_text.split(","))
        location_text = get_location_by_coordinates(latitude, longitude)

    subscription_text = (
        f"<b>{'Подписка' if lang == 'ru' else 'Subscription'}:</b> {user.subscription}\n"
    )
    if user.subscription != "Free":
        subscription_text += (
            f"<b>{'Дата окончания подписки' if lang == 'ru' else 'Subscription end date'}:</b> {user.subscription_end}\n"
        )

    description = (
        f"<b>{'Ваш профиль' if lang == 'ru' else 'Your profile'}:</b>\n\n"
        f"<b>{'Имя' if lang == 'ru' else 'Name'}:</b> {user.name}\n"
        f"<b>{'Возраст' if lang == 'ru' else 'Age'}:</b> {user.age}\n"
        f"<b>{'Пол' if lang == 'ru' else 'Gender'}:</b> {GENDER[lang][user.gender]}\n"
        f"<b>{'Локация' if lang == 'ru' else 'Location'}:</b> {location_text or ('Локация не указана' if lang == 'ru' else 'Location not provided')}\n\n"
        f"{subscription_text}"
        f"<b>{'Ориентация' if lang == 'ru' else 'Orientation'}:</b> {ORI[lang][user.orientation]}\n"
        f"<b>{'Кого показывать' if lang == 'ru' else 'Viewing Preferences'}:</b> {WHO[lang][user.for_whom]}\n"
        f"<b>{'Цели' if lang == 'ru' else 'Goals'}:</b> {PREFERENCES[lang][user.preferences]}\n"
        f"<b>{'Увлечения' if lang == 'ru' else 'Hobbies'}:</b> {hobbies_text}\n\n"
        f"_________________________\n{user.about or ''}\n"
    )



    media = user.medias or []
    if len(media) == 1:
        media_file = media[0]['file_id']
        if media[0]['type'] == 'photo':
            msg= await message.bot.send_photo(message.from_user.id, media_file, caption=description)
        elif media[0]['type'] == 'video':
            msg= await message.bot.send_video(message.from_user.id, media_file, caption=description)
    else:
        files=[]
        i =0
        for media_file in media:
            
            caption=description if i == 0 else None
            
            if media_file["type"] =="video":
                files.append(InputMediaVideo(media=f"{media_file['file_id']}", caption=caption))
                i = i+1
            elif media_file['type'] == 'photo':
                files.append(InputMediaPhoto(media=f"{media_file['file_id']}", caption=caption))
                i = i+1
            else:
                continue
                 

    # Отправка медиа-группы
        msg= await message.bot.send_media_group(chat_id=message.from_user.id, media=files)
        data= await state.get_data()
        data["id_card_profile"]=None
        await state.update_data(data=data)
    lang = user.lang if user and user.lang in ["ru", "en"] else "ru"
    if user.localstatus == "active":
        btn_local = InlineKeyboardButton(
            text="🌍 Скрыть локацию" if lang == "ru" else "🌍 Hide Location",
            callback_data="location_hish"
        )
    else:
        btn_local = InlineKeyboardButton(
            text="🌍 Показать локацию" if lang == "ru" else "🌍 Show Location",
            callback_data="location_hish"
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🖋 Имя" if lang == "ru" else "🖋 Name",
                callback_data="fedit_name"
            ),
            InlineKeyboardButton(
                text="🎂 Возраст" if lang == "ru" else "🎂 Age",
                callback_data="fedit_age"
            )
        ],
        [
            InlineKeyboardButton(
                text="📍 Изменить локацию" if lang == "ru" else "📍 Edit Location",
                callback_data="fedit_location"
            ),
            btn_local
        ],
        [
            InlineKeyboardButton(
                text="⚥ Пол" if lang == "ru" else "⚥ Gender",
                callback_data="fedit_gender"
            ),
            InlineKeyboardButton(
                text="🌈 Ориентация" if lang == "ru" else "🌈 Orientation",
                callback_data="fedit_orientation"
            )
        ],
        [
            InlineKeyboardButton(
                text="👁️‍🗨️ Кого показывать" if lang == "ru" else "👁️‍🗨️ Viewing Preferences",
                callback_data="fedit_pref"
            ),
            InlineKeyboardButton(
                text="🎯 Цели" if lang == "ru" else "🎯 Goals",
                callback_data="fedit_goals"
            )
        ],
        [
            InlineKeyboardButton(
                text="🎨 Увлечения" if lang == "ru" else "🎨 Hobbies",
                callback_data="fedit_hobbies"
            ),
            InlineKeyboardButton(
                text="📝 Описание" if lang == "ru" else "📝 Description",
                callback_data="fedit_descr"
            )
        ],[
    InlineKeyboardButton(
        text="🖼️ Изменить медиа" if lang == "ru" else "🖼️ Edit Media",
        callback_data="fedit_media"
    )
],

        [
            InlineKeyboardButton(
                text="🔄 Заполнить заново" if lang == "ru" else "🔄 Refill Profile",
                callback_data="reset_profile"
            )
        ]
    ])


    await message.answer(
        MESSAGES["action_prompt"][lang], 
        reply_markup=keyboard
    )

from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from src.models import User
from aiogram.types import Message
from typing import Callable, Awaitable, Dict, Any, List
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext, BaseStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from src.utils.state import RegState
from src.utils.add_profile import add_profile
from aiogram.types import ContentType


router = Router()
BAD_WORDS = [
    # Наркотики
    "наркотик", "наркота", "косяк", "травка", "гашиш", "героин", "кокаин", "амфетамин", "экстази",
    "марихуана", "спайс", "лсд", "шишки", "опиум", "план", "кристалл", "мефедрон", "drugs", "drug",
    "weed", "marijuana", "cocaine", "heroin", "ecstasy", "meth", "amphetamine", "hash", "spice",
    "lsd", "crystal", "meph", "opium", "j0int", "dr@g", "tr@vka",

    # CP
    "детская порнография", "детское порно", "запрещенное видео", "нелегальный контент", "порнография с детьми",
    "cp", "child porn", "child pornography", "illegal content", "b@nned video", "ch!ld p0rn",

    # Оружие
    "оружие", "пистолет", "винтовка", "автомат", "пулемет", "граната", "мина", "бомба", "арсенал",
    "ружье", "ствол", "калашников", "ак-47", "глок", "гранатомет", "weapon", "gun", "pistol", "rifle",
    "machine gun", "grenade", "bomb", "landmine", "arsenal", "shotgun", "kalashnikov", "ak47",
    "glock", "rocket launcher", "we@pon", "glock-19", "b0mb",

    # Additional prohibited words
    "explosive", "tnt", "c4", "detonator", "silencer", "sniper", "assault rifle", "pipe bomb",
    "наркот", "герич", "герыч", "доза", "спайсы", "соли", "фен", "скорость",
    "запрещенка", "порно с детьми", "порево", "kill", "murder", "mass shooting", "terrorist", "attack"
]






# ++++++++++++++++ NAME +++++++++++++++

@router.message(RegState.name)
async def set_name(message: types.Message, state: FSMContext, lang: str):
    user = await User.get_or_none(user_id=message.from_user.id)
    global BAD_WORDS
    if user:
        
        if message.text not in BAD_WORDS:
            user.name = message.text.strip()
            await user.save()
            if user.gender is None:
                
                if lang == "ru":
                    txt = """<b>Имя указано! ✅</b>
    Отлично, теперь укажи свой пол! 🌟

    ➡️ Выбери один из вариантов:
    """
                else:
                    txt = """<b>Name provided! ✅</b>
    Great, now specify your gender! 🌟

    ➡️ Choose one of the options:
    """

                inline_keyboard = [
                    [InlineKeyboardButton(text="👩 Женский" if lang == "ru" else "👩 Female", callback_data="gender_fem")],
                    [InlineKeyboardButton(text="👨 Мужской" if lang == "ru" else "👨 Male", callback_data="gender_mal")],
                    [InlineKeyboardButton(text="🌈 Другое" if lang == "ru" else "🌈 Other", callback_data="gender_oth")]
                ]

                keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
                await state.set_state(RegState.gender)
                await message.answer(txt, reply_markup=keyboard)
            else:
                txt="Сохранено ✅\nНажмите /start, чтобы продолжить." if lang == "ru" else "Saved ✅\nClick /start to continue."                
                await state.set_state(state=None)

                
                if not all([
                        user.name,
                        user.age,
                        user.gender,
                        user.orientation,
                        user.for_whom,
                        user.preferences,
                        user.location,
                        user.about,
                        user.hobbies,
                        user.medias]):
                    await add_profile(message=message, state=state , user=user, lang=lang)
                else:
                    await message.answer(txt)

        else:
            txt = """<❌ <b>Ошибка:</b> Ваше имя содержит запрещенные слова. Пожалуйста, выберите другое имя. ✍️""" if lang == "ru" else """<❌ <b>Error:</b> Your name contains prohibited words. Please choose another name. ✍️"""
            await state.set_state(RegState.name)
            await message.answer(txt)
        
# ++++++++++++++++ GENDER +++++++++++++++

@router.callback_query(lambda c: c.data.startswith("gender_"), RegState.gender)
async def set_gender(callback_query: CallbackQuery, user: User, state: FSMContext, lang: str):
    if user:
        user.gender = callback_query.data.split("_")[1]
        await user.save()
        if user.orientation is None:
            if lang == "ru":
                txt = """<b>Пол указан! ✅</b>
    Теперь укажи свою ориентацию! 🌟

    ➡️ Выбери один из вариантов:
    """
            else:
                txt = """<b>Gender saved! ✅</b>
    Now specify your orientation! 🌟

    ➡️ Choose one of the options:
    """
            if user.gender =='mal':

                inline_keyboard = [
                    [InlineKeyboardButton(text="❤️ Гетеро" if lang == "ru" else "❤️ Hetero", callback_data="orientation_hetero")],
                    [InlineKeyboardButton(text="🌈 Гей" if lang == "ru" else "🌈 Gay", callback_data="orientation_gay")],
                    [InlineKeyboardButton(text="💛 Би" if lang == "ru" else "💛 Bi", callback_data="orientation_bi")]
                ]
            elif user.gender =="fem":
                inline_keyboard = [
                    [InlineKeyboardButton(text="❤️ Гетеро" if lang == "ru" else "❤️ Hetero", callback_data="orientation_hetero")],
                    [InlineKeyboardButton(text="💖 Лесби" if lang == "ru" else "💖 Lesbian", callback_data="orientation_lesbian")],
                    [InlineKeyboardButton(text="💛 Би" if lang == "ru" else "💛 Bi", callback_data="orientation_bi")]
                ]
            elif user.gender=="oth":
                inline_keyboard = [
                    [InlineKeyboardButton(text="❤️ Гетеро" if lang == "ru" else "❤️ Hetero", callback_data="orientation_hetero")],
                    [InlineKeyboardButton(text="🌈 Гей/Лесби" if lang == "ru" else "🌈 Gay/Lesbian", callback_data="orientation_gay_lesbian")],
                    [InlineKeyboardButton(text="💛 Би" if lang == "ru" else "💛 Bi", callback_data="orientation_bi")]
                ]

            inline_keyboard.append([InlineKeyboardButton(text="💫Другая" if lang == "ru" else "💫Other", callback_data="orientation_oth")])
            inline_keyboard.append([InlineKeyboardButton(text="Пропустить ➡️" if lang == "ru" else "Skip ➡️", callback_data="orientation_skip")])
            keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
            await state.set_state(RegState.orientation)
            await callback_query.message.edit_text(txt, reply_markup=keyboard)
        else:
            txt="Сохранено ✅\nНажмите /start, чтобы продолжить." if lang == "ru" else "Saved ✅\nClick /start to continue."                
            await state.set_state(state=None)

            
            if not all([
                        user.name,
                        user.age,
                        user.gender,
                        user.orientation,
                        user.for_whom,
                        user.preferences,
                        user.location,
                        user.about,
                        user.hobbies,
                        user.medias]):
                    await add_profile(message=callback_query.message, state=state , user=user, lang=lang)
            else:
                await callback_query.message.edit_text(txt, reply_markup=None)
# ++++++++++++++++ ORIENTATION +++++++++++++++

@router.callback_query(lambda c: c.data.startswith("orientation_"), RegState.orientation)
async def set_orientation(callback_query: CallbackQuery, user: User, state: FSMContext, lang: str):
    if user:
        user.orientation = callback_query.data.split("_")[1]
        await user.save()
        if user.for_whom is None:
            if lang == "ru":
                txt = """<b>Ориентация указана! ✅</b>
    Теперь укажи, кого ты хочешь видеть! 🌟

    ➡️ Выбери один из вариантов:
    """
            else:
                txt = """<b>Orientation saved! ✅</b>
    Now specify who you want to see! 🌟

    ➡️ Choose one of the options:
    """

            inline_keyboard = [
                [InlineKeyboardButton(text="👩 Девушки" if lang == "ru" else "👩 Girls", callback_data="show_fem")],
                [InlineKeyboardButton(text="👨 Парни" if lang == "ru" else "👨 Boys", callback_data="show_mal")],
                [InlineKeyboardButton(text="🌍 Все" if lang == "ru" else "🌍 Everyone", callback_data="show_all")]
            ]

            keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
            await state.set_state(RegState.show)
            await callback_query.message.edit_text(txt, reply_markup=keyboard)
        else:
            txt="Сохранено ✅\nНажмите /start, чтобы продолжить." if lang == "ru" else "Saved ✅\nClick /start to continue."                
            await state.set_state(state=None)

            
            if not all([
                        user.name,
                        user.age,
                        user.gender,
                        user.orientation,
                        user.for_whom,
                        user.preferences,
                        user.location,
                        user.about,
                        user.hobbies,
                        user.medias]):
                    await add_profile(message=callback_query.message, state=state , user=user, lang=lang)
            else:
                await callback_query.message.edit_text(txt, reply_markup=None)

# ++++++++++++++++ SHOW PREFERENCES +++++++++++++++

@router.callback_query(lambda c: c.data.startswith("show_"), RegState.show)
async def set_show_preferences(callback_query: CallbackQuery, user: User, state: FSMContext, lang: str):
    if user:
        user.for_whom = callback_query.data.split("_")[1]
        await user.save()
        if user.age is None:
            if lang == "ru":
                txt = """<b>Параметры просмотра указаны! ✅</b>
    Теперь укажи свой возраст! 🌟

    ➡️ Введите ваш возраст (минимум 16 лет):
    """
            else:
                txt = """<b>Viewing preferences saved! ✅</b>
    Now specify your age! 🌟

    ➡️ Enter your age (minimum 16 years):
    """

            await state.set_state(RegState.age)
            await callback_query.message.edit_text(txt)
        else:
            txt="Сохранено ✅\nНажмите /start, чтобы продолжить." if lang == "ru" else "Saved ✅\nClick /start to continue."                
            await state.set_state(state=None)

            
            if not all([
                        user.name,
                        user.age,
                        user.gender,
                        user.orientation,
                        user.for_whom,
                        user.preferences,
                        user.location,
                        user.about,
                        user.hobbies,
                        user.medias]):
                    await add_profile(message=callback_query.message, state=state , user=user, lang=lang)
            else:
                await callback_query.message.edit_text(txt, reply_markup=None)

# ++++++++++++++++ AGE +++++++++++++++

@router.message(RegState.age)
async def set_age(message: types.Message, user: User, state: FSMContext, lang: str):
    if user:
        if message.text.isdigit():
            age = int(message.text)
            if age >= 16:
                user.age = age
                await user.save()
                if user.preferences is None:
                    if lang == "ru":
                        txt = """<b>Возраст указан! ✅</b>
    Теперь укажи свои цели! 🌟

    ➡️ Выбери цели из предложенных вариантов:
    """
                    else:
                        txt = """<b>Age saved! ✅</b>
    Now specify your goals! 🌟

    ➡️ Choose your goals from the options provided:
    """
                    inline_keyboard=[]
                    if lang =="ru":
                        inline_keyboard.append([InlineKeyboardButton(text="🤝 Дружба", callback_data="interest_friendship")])
                        inline_keyboard.append([InlineKeyboardButton(text="❤️ Романтические отношения", callback_data="interest_romantic")])
                        inline_keyboard.append([InlineKeyboardButton(text="💼 Партнерство в проектах", callback_data="interest_partnership")])
                        inline_keyboard.append([InlineKeyboardButton(text="🌍 Общение на тему эмиграции", callback_data="interest_emigration")])
                    else:
                        inline_keyboard.append([InlineKeyboardButton(text="🤝 Friendship", callback_data="interest_friendship")])
                        inline_keyboard.append([InlineKeyboardButton(text="❤️ Romantic relationships", callback_data="interest_romantic")])
                        inline_keyboard.append([InlineKeyboardButton(text="💼 Partnership in projects", callback_data="interest_partnership")])
                        inline_keyboard.append([InlineKeyboardButton(text="🌍 Discussion about emigration", callback_data="interest_emigration")])


                    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
                    await state.set_state(RegState.preferences)
                    await message.answer(txt, reply_markup=keyboard)
                else:
                    txt="Сохранено ✅\nНажмите /start, чтобы продолжить." if lang == "ru" else "Saved ✅\nClick /start to continue."                
                    await state.set_state(state=None)

                    if not all([
                        user.name,
                        user.age,
                        user.gender,
                        user.orientation,
                        user.for_whom,
                        user.preferences,
                        user.location,
                        user.about,
                        user.hobbies,
                        user.medias]):
                        await add_profile(message=message, state=state , user=user, lang=lang)
                    else:
                        await message.answer(txt)
            else:
                txt = """❌ <b>Ошибка:</b> Возраст должен быть не менее 16 лет. 🔢""" if lang == "ru" else """❌ <b>Error:</b> Age must be at least 16 years. 🔢"""
                await message.answer(txt)
        else:
            txt = """❌ <b>Ошибка:</b> Возраст должен быть числом. Пожалуйста, введите корректное значение. 🔢""" if lang == "ru" else """❌ <b>Error:</b> Age must be a number. Please enter a valid value. 🔢"""
            await message.answer(txt)


# ++++++++++++++++ PREFERENCES +++++++++++++++

@router.callback_query(lambda c: "interest_" in c.data, RegState.preferences)
async def callback_handler(callback_query: CallbackQuery, user: User, state: FSMContext, lang: str):
    
    if user:
        pref = callback_query.data.split("_")[1]
        user.preferences=pref
        await user.save()
        if user.location is None:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[[ KeyboardButton(text="📍 Отправить локацию" if lang == "ru" else "📍 Share Location",request_location=True)]],resize_keyboard=True,one_time_keyboard=True)

            if lang == "ru":
                txt = """<b>Цели поиска указаны! ✅</b>
    Отлично, теперь нам нужно знать вашу локацию, чтобы предложить людей рядом. 🌍

    ⚠️ <b>Не переживайте:</b> никто из пользователей не узнает ваше реальное местоположение. Они будут видеть только <b>приблизительное расстояние</b> до вас. 🛡️

    💡 <b>Обратите внимание:</b> вы можете отправить свою текущую геолокацию, нажав кнопку ниже. 
    Если хотите указать другую точку на карте, выберите её в меню Telegram. Подробная инструкция по смене локации доступна в нашем <a href="https://t.me/your_channel_post">канале</a>. 📍

    ➡️ Пожалуйста, нажмите кнопку ниже, чтобы отправить свою локацию или выберите точку на карте.
    """
            else:
                txt = """<b>Search goals saved! ✅</b>
    Great, now we need your location to suggest people nearby. 🌍

    ⚠️ <b>Don't worry:</b> no one will see your exact location. Users will only see the <b>approximate distance</b> to you. 🛡️

    💡 <b>Note:</b> You can send your current location by pressing the button below. 
    If you’d like to specify another point on the map, select it in the Telegram menu. Detailed instructions for changing the location are available in our <a href="https://t.me/your_channel_post">channel</a>. 📍

    ➡️ Please press the button below to share your location or choose a point on the map.
    """

            await state.set_state(RegState.location)
            await callback_query.bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
            msg= await callback_query.bot.send_message(callback_query.from_user.id, txt, reply_markup=keyboard)
            data = await state.get_data()
            data['idmsg_local']=msg.message_id
            await state.update_data(data)
        else:
            txt="Сохранено ✅\nНажмите /start, чтобы продолжить." if lang == "ru" else "Saved ✅\nClick /start to continue."                
            await state.set_state(state=None)

            
            if not all([
                        user.name,
                        user.age,
                        user.gender,
                        user.orientation,
                        user.for_whom,
                        user.preferences,
                        user.location,
                        user.about,
                        user.hobbies,
                        user.medias]):
                    await add_profile(message=callback_query.message, state=state , user=user, lang=lang)
            else:
                await callback_query.message.edit_text(txt, reply_markup=None)

# ++++++++++++++++ LOCATION +++++++++++++++

@router.message(RegState.location, lambda message: message.content_type == ContentType.LOCATION)
async def set_location(message: types.Message, user: User, state: FSMContext, lang: str):
    
    if user:
        print(f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n{message.location}\n\n\n\n\n\n\n\n\n\n\n\n{message.location.model_config}")
        user.location = f"{message.location.latitude},{message.location.longitude}"
        await user.save()
        if user.about is None:
            if lang == "ru":
                txt = """<b>Локация указана! ✅</b>
    Отлично, теперь расскажи немного о себе. 🌟

    ➡️ Напиши короткое описание о себе: твои интересы, хобби или что-то, что ты хотел бы, чтобы другие знали о тебе.
    """
            else:
                txt = """<b>Location saved! ✅</b>
    Great, now tell us a bit about yourself. 🌟

    ➡️ Write a short description about yourself: your interests, hobbies, or anything you’d like others to know about you.
    """
            await state.set_state(RegState.about)
            data = await state.get_data()
            if "idmsg_local" in data: 
                await message.bot.delete_message(message.from_user.id, data["idmsg_local"])
            data["idmsg_local"]=''
            await state.update_data(data)
            await message.bot.delete_message(message.from_user.id, message.message_id)
            await message.bot.send_message(message.from_user.id, txt)
        else:
            txt="Сохранено ✅\nНажмите /start, чтобы продолжить." if lang == "ru" else "Saved ✅\nClick /start to continue."                
            await state.set_state(state=None)

            
            if not all([
                        user.name,
                        user.age,
                        user.gender,
                        user.orientation,
                        user.for_whom,
                        user.preferences,
                        user.location,
                        user.about,
                        user.hobbies,
                        user.medias]):
                    await add_profile(message=message, state=state , user=user, lang=lang)
            else:
                await message.answer(txt)
# ++++++++++++++++ ABOUT +++++++++++++++

@router.message(RegState.about)
async def set_about(message: types.Message, user: User, state: FSMContext, lang: str):
    global BAD_WORDS
    if user:
        if message.text:
            if message.text not in BAD_WORDS:
                user.about = message.text
                await user.save()
                if user.hobbies is None:
                
                    await state.set_state(RegState.hobbies)
                # Увлечения на двух языках с номерами
                    interests = [
                        (1, "Спорт", "Sport"), (2, "Музыка", "Music"), (3, "Путешествия", "Travel"), 
                        (4, "Кино", "Movies"), (5, "Кулинария", "Cooking"), (6, "Искусство", "Art"), 
                        (7, "Танцы", "Dancing"), (8, "Технологии", "Technology"), (9, "Литература", "Literature"), 
                        (10, "Фотография", "Photography"), (11, "Игры", "Games"), (12, "Природа", "Nature"), 
                        (13, "Автомобили", "Cars"), (14, "Мода", "Fashion"), (15, "Здоровье", "Health")
                    ]
                    inlinekeyboard = []
                    row = []

                    # Формируем кнопки для увлечений, по 3 в ряд
                    for i, (number, interest_ru, interest_en) in enumerate(interests[:10], start=1):
                        row.append(InlineKeyboardButton(
                            text=interest_ru if lang == "ru" else interest_en,
                            callback_data=f"intrs_{number}"
                        ))
                        # Если добавлено 3 кнопки или это последняя кнопка в списке
                        if len(row) == 2 or i == len(interests[:10]):
                            inlinekeyboard.append(row)
                            row = []  # Сбрасываем строку для следующего ряда

                    # Добавляем стрелки навигации в последнюю строку
                    inlinekeyboard.append([
                        InlineKeyboardButton(text="🚫" if lang == "ru" else "🚫", callback_data="intrs_z"),
                        InlineKeyboardButton(text="➡️" if lang == "ru" else "➡️ Next", callback_data="intrs_page_next")
                    ])

                    keyboard = InlineKeyboardMarkup(inline_keyboard=inlinekeyboard)
                    
                    if lang == "ru":
                        txt = """<b>Записали ✅</b>
    Отлично, теперь выбери до 5 увлечений, которые описывают тебя. 🌟

    ➡️ Нажимай на кнопки, чтобы выбрать увлечения. Когда закончишь, нажми "Сохранить✅".
        """
                    else:
                        txt = """<b>Saved ✅</b>
    Great, now select up to 5 hobbies that describe you. 🌟\n\n➡️ Click on the buttons to select your hobbies. Once you're done, click \"<b>Save✅</b>\".
    """


                    await message.answer(txt, reply_markup=keyboard)
                else:
                    txt="Сохранено ✅\nНажмите /start, чтобы продолжить." if lang == "ru" else "Saved ✅\nClick /start to continue."
                    await state.set_state(state=None)

                    
                    if not all([
                        user.name,
                        user.age,
                        user.gender,
                        user.orientation,
                        user.for_whom,
                        user.preferences,
                        user.location,
                        user.about,
                        user.hobbies,
                        user.medias]):
                        await add_profile(message=message, state=state , user=user, lang=lang)
                    else:
                        await message.answer(txt)
            else:
                if lang == "ru":
                    txt = """❌ <b>Ошибка:</b> Описание содержит запрещенные слова. Пожалуйста, введите другое описание и попробуйте снова. ✍️"""
                else:
                    txt = """❌ <b>Error:</b> The description contains prohibited words. Please enter another description and try again. ✍️"""
                await message.answer(txt)
                await state.set_state(RegState.about)
        else:
                if lang == "ru":
                    txt = """❌ <b>Ошибка:</b> Описание долджно содержать текст ✍️"""
                else:
                    
                    txt = """❌ <b>Error:</b> The description must contain text. Please write something ✍️"""
                await message.answer(txt)
                await state.set_state(RegState.about)

# ++++++++++++++++ HOBBIES +++++++++++++++

@router.callback_query(lambda c: "intrs_" in c.data or c.data.startswith("intrs_page") or c.data == "intrs_done", RegState.hobbies)
async def callback_handler(callback_query: CallbackQuery, user: User, state: FSMContext, lang: str):
    # Загружаем список интересов
    interests = [
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

    # Обработка страниц
    state_data = await state.get_data()
    current_page = state_data.get("current_page", 1)
    hobbies = state_data.get("selected_hobbies", [])

    if callback_query.data.startswith("intrs_page"):
        if "next" in callback_query.data:
            current_page += 1
        elif "back" in callback_query.data:
            current_page -= 1
        await state.update_data(current_page=current_page)

    elif callback_query.data.startswith("intrs_") and callback_query.data != "intrs_done":
        interest = callback_query.data.split("_")[1]
        if interest in hobbies:
            hobbies.remove(interest)
        else:
            if len(hobbies) < 5:
                hobbies.append(interest)
            else:
                txt1 = "Выбрано максимальное количество! Уберите один интерес или нажмите 'Сохранить'." if lang == "ru" else "Maximum number selected! Remove one interest or click 'Save'."
                await callback_query.answer(
                    txt1,
                    show_alert=True
                )
                return
        await state.update_data(selected_hobbies=hobbies)

    elif callback_query.data == "intrs_done":
        if len(hobbies) < 5:
            txt2 = "Вы должны выбрать минимум 5 интересов, чтобы продолжить!" if lang == "ru" else "You must select at least 5 interests to continue!"
            await callback_query.answer(
                txt2,
                show_alert=True
            )
            return
        else:
            user.hobbies = hobbies  # Сохраняем в базу данных только при завершении
            await user.save()
            if user.medias is None:
                txt3 = "Интересы сохранены! ✅" if lang == "ru" else "Interests saved! ✅"
                await callback_query.answer(txt3, show_alert=True)

                txt = """🎉 <b>Отлично!</b> Ваши хобби успешно сохранены.  

    Теперь отправьте от <b>1 до 3 медиа</b> (фотографии или видео), чтобы другие могли узнать вас лучше.  
    Или нажмите "Пропустить", чтобы продолжить. ⏩""" if lang == "ru" else """🎉 <b>Great!</b> Your hobbies have been successfully saved.  

    Now, please send <b>1 to 3 media</b> (photos or videos) so others can get to know you better.  
    Or press "Skip" to continue. ⏩"""

                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Пропустить 🔄" if lang == "ru" else "Skip 🔄", callback_data="skip_album")]
                ])
                data = await state.get_data()
                msg =await callback_query.message.edit_text(txt, reply_markup=keyboard)
                data['idmsg_media']=msg.message_id
                await state.update_data(data)
                await state.set_state(RegState.media)
                return
            else:
                txt="Сохранено ✅\nНажмите /start, чтобы продолжить." if lang == "ru" else "Saved ✅\nClick /start to continue."
                await state.set_state(state=None)
                await callback_query.answer(txt, show_alert=True)

                if not all([
                        user.name,
                        user.age,
                        user.gender,
                        user.orientation,
                        user.for_whom,
                        user.preferences,
                        user.location,
                        user.about,
                        user.hobbies,
                        user.medias]):
                    await add_profile(message=callback_query.message, state=state , user=user, lang=lang)
                else:
                    await callback_query.message.edit_text(txt, reply_markup=None)
                return

    # Генерация кнопок для текущей страницы
    page_size = 10
    start_index = (current_page - 1) * page_size
    end_index = start_index + page_size
    inlinekeyboard = []
    row = []

    for i, (number, interest_ru, interest_en) in enumerate(interests[start_index:end_index], start=1):
        text = ("🔹" if str(number) in hobbies else "") + (interest_ru if lang == "ru" else interest_en)
        row.append(InlineKeyboardButton(
            text=text,
            callback_data=f"intrs_{number}"
        ))
        if len(row) == 2 or i == len(interests[start_index:end_index]):
            inlinekeyboard.append(row)
            row = []

    navigation_buttons = []
    if current_page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️" if lang == "ru" else "⬅️ Back", callback_data="intrs_page_back"))
    if end_index < len(interests):
        navigation_buttons.append(InlineKeyboardButton(text="➡️" if lang == "ru" else "➡️ Next", callback_data="intrs_page_next"))
    if navigation_buttons:
        inlinekeyboard.append(navigation_buttons)

    if len(hobbies) == 5:
        inlinekeyboard.append(
            [InlineKeyboardButton(text=f"Сохранить ({len(hobbies)}/5) ✅" if lang == "ru" else f"Save ({len(hobbies)}/5) ✅", callback_data="intrs_done")]
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=inlinekeyboard)
    txt = (f"<b>Выбрано {len(hobbies)}/5 увлечений ✅</b>\n" if lang == "ru" else f"<b>Selected {len(hobbies)}/5 hobbies ✅</b>\n")
    txt += "Отлично, выбери до 5 увлечений, которые описывают тебя. 🌟\n\n➡️ Нажимай на кнопки, чтобы выбрать увлечения. Когда закончишь, нажми 'Сохранить'." if lang == "ru" else "Great, select up to 5 hobbies that describe you. 🌟\n\n➡️ Click on the buttons to select your hobbies. Once you're done, click 'Save'."

    await callback_query.message.edit_text(txt, reply_markup=keyboard)
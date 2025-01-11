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
            user.name = message.text # Убираем лишние пробелы
            await user.save()
            
            await state.clear()  # Очищаем текущее состояние
            if lang == "ru":
                txt = """<b>Имя указано! ✅</b>
Отлично, давай продолжим настройку твоего профиля. 🌟

➡️ Пожалуйста, укажи свой возраст, чтобы мы могли предложить подходящих людей!
"""
            else:
                txt = """<b>Name provided! ✅</b>
Great, let’s continue setting up your profile. 🌟

➡️ Please provide your age so we can suggest suitable matches!
"""
            await state.set_state(RegState.age)
           
        else:
            if lang == "ru":
                txt = """<❌ <b>Ошибка:</b> Ваше имя содержит запрещенные слова.  
🙅‍♂️ Пожалуйста, выберите другое имя и попробуйте снова. ✍️
"""
            else:
                txt = """<❌ <b>Error:</b> Your name contains prohibited words.  
🙅‍♂️ Please choose another name and try again. ✍️
"""
     # Переходим к следующе
            await state.set_state(RegState.name) 
        await message.answer(txt)


# ++++++++++++++++ AGE +++++++++++++++

@router.message(RegState.age)
async def set_name(message: types.Message, user: User, state: FSMContext, lang: str):
    
    
    
    if user:
        
        if message.text.isdigit():
    
            user.age = int(message.text) 
            await user.save()
            
             # Очищаем текущее состояние
            if lang == "ru":
                txt = f"""<b>{user.name}, возраст указан! ✅</b>
Отлично, теперь укажи свой пол, чтобы мы могли сделать рекомендации ещё точнее. 🌟

➡️ Выбери один из вариантов:

""" 
                inline_keyboard=[]
                inline_keyboard.append([InlineKeyboardButton(text="👩 Женский", callback_data="gender_fem")])
                inline_keyboard.append([InlineKeyboardButton(text="👨 Мужской", callback_data="gender_mal")])
                inline_keyboard.append([InlineKeyboardButton(text="🌈 Другое", callback_data="gender_oth")])

                keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
            else:
                txt = f"""<b>{user.name}, age provided! ✅</b>
Great, now let’s specify your gender to make our suggestions even more accurate. 🌟

➡️ Please choose one of the options:

"""     
                inline_keyboard=[]
                inline_keyboard.append([InlineKeyboardButton(text="👩 Female", callback_data="gender_fem")])
                inline_keyboard.append([InlineKeyboardButton(text="👨 Male", callback_data="gender_mal")])
                inline_keyboard.append([InlineKeyboardButton(text="🌈 Other", callback_data="gender_oth")])

                keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        # Переходим к следующе
            await state.set_state(RegState.gender) 
            await message.answer(txt, reply_markup=keyboard)
        else:
            if lang == "ru":
                txt = """❌ <b>Ошибка:</b> Возраст должен быть числом. Пожалуйста, введите корректное значение. 🔢"""
            else:
                txt = """❌ <b>Error:</b> Age must be a number. Please enter a correct value. 🔢"""
            await message.answer(txt)
            await state.set_state(RegState.age)


# +++++++++ GENDER +++++++++++++++
@router.callback_query(lambda c: "gender_" in c.data, RegState.gender)
async def callback_handler(callback_query: CallbackQuery, user: User, state: FSMContext, lang: str):

    
    if user:
        gender = callback_query.data.split("_")[1]
        user.gender=gender
        await user.save()
        inline_keyboard=[]
        if lang == "ru":
            inline_keyboard.append([InlineKeyboardButton(text="🤝 Дружба", callback_data="interest_friendship")])
            inline_keyboard.append([InlineKeyboardButton(text="❤️ Романтические отношения", callback_data="interest_romantic")])
            inline_keyboard.append([InlineKeyboardButton(text="💼 Партнерство в проектах", callback_data="interest_partnership")])
            inline_keyboard.append([InlineKeyboardButton(text="🌍 Общение на тему эмиграции", callback_data="interest_emigration")])

            txt = """<b>Пол указан! ✅</b>
Отлично, теперь расскажи, что ты ищешь. 🌟

➡️ Выбери цели знакомства:
    """
        else:
            inline_keyboard.append([InlineKeyboardButton(text="🤝 Friendship", callback_data="interest_friendship")])
            inline_keyboard.append([InlineKeyboardButton(text="❤️ Romantic relationships", callback_data="interest_romantic")])
            inline_keyboard.append([InlineKeyboardButton(text="💼 Partnership in projects", callback_data="interest_partnership")])
            inline_keyboard.append([InlineKeyboardButton(text="🌍 Discussion about emigration", callback_data="interest_emigration")])

            txt = """<b>Gender specified! ✅</b>
Great, now tell us what you are looking for. 🌟

➡️ Choose your goals for connecting:
    """
        await state.set_state(RegState.preferences)
        keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        await callback_query.message.edit_text(text=txt, reply_markup=keyboard)

# ++++++++++++++++ PREFERENCES +++++++++++++++

@router.callback_query(lambda c: "interest_" in c.data, RegState.preferences)
async def callback_handler(callback_query: CallbackQuery, user: User, state: FSMContext, lang: str):
    
    if user:
        pref = callback_query.data.split("_")[1]
        user.preferences=pref
        await user.save()
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text="📍 Отправить локацию" if lang == "ru" else "📍 Share Location",
                        request_location=True
                    )
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

        if lang == "ru":
            txt = """<b>Цели поиска указаны! ✅</b>
Отлично, теперь нам нужно знать твою локацию, чтобы предложить людей рядом. 🌍

⚠️ <b>Не переживайте:</b> никто из пользователей не узнает ваше реальное местоположение. Они будут видеть только <b>приблизительное расстояние</b> до вас. 🛡️

➡️ Пожалуйста, нажмите кнопку ниже, чтобы отправить свою локацию.
"""
        else:
            txt = """<b>Search goals saved! ✅</b>
Great, now we need your location to suggest people nearby. 🌍

⚠️ <b>Don't worry:</b> no one will see your exact location. Users will only see the <b>approximate distance</b> to you. 🛡️

➡️ Please press the button below to share your location.
"""
        await state.set_state(RegState.location)
        await callback_query.bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        msg= await callback_query.bot.send_message(callback_query.from_user.id, txt, reply_markup=keyboard)
        data = await state.get_data()
        data['idmsg_local']=msg.message_id
        await state.update_data(data)

# ++++++++++++++++ LOCATION +++++++++++++++

@router.message(RegState.location, lambda message: message.content_type == ContentType.LOCATION)
async def set_location(message: types.Message, user: User, state: FSMContext, lang: str):
    
    if user:
        user.location = f"{message.location.latitude},{message.location.longitude}"
        await user.save()
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

# ++++++++++++++++ ABOUT +++++++++++++++

@router.message(RegState.about)
async def set_about(message: types.Message, user: User, state: FSMContext, lang: str):
    global BAD_WORDS
    if user:
        if message.text:
            if message.text not in BAD_WORDS:
                user.about = message.text
                await user.save()
                
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
                for i, (number, interest_ru, interest_en) in enumerate(interests[:15], start=1):
                    row.append(InlineKeyboardButton(
                        text=interest_ru if lang == "ru" else interest_en,
                        callback_data=f"intrs_{number}"
                    ))
                    # Если добавлено 3 кнопки или это последняя кнопка в списке
                    if len(row) == 3 or i == len(interests[:15]):
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

    ➡️ Нажимай на кнопки, чтобы выбрать увлечения. Когда закончишь, нажми "Далее".
        """
                else:
                    txt = """<b>Saved ✅</b>
    Great, now select up to 5 hobbies that describe you. 🌟

    ➡️ Click on the buttons to select your hobbies. Once you're done, click "Next".
    """


                await message.answer(txt, reply_markup=keyboard)
                
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
    hobbies = user.hobbies or []

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
        user.hobbies = hobbies
        await user.save()

    elif callback_query.data == "intrs_done":
        if len(hobbies) < 5:
            txt2 = "Вы должны выбрать минимум 5 интересов, чтобы продолжить!" if lang == "ru" else "You must select at least 5 interests to continue!"
            await callback_query.answer(
                txt2,
                show_alert=True
            )
            return
        else:
            txt3 = "Интересы сохранены! ✅" if lang == "ru" else "Interests saved! ✅"
            await callback_query.answer(txt3, show_alert=True)
            # Переход к следующему шагу (пример)
            txt ="""🎉 <b>Отлично!</b> Ваши хобби успешно сохранены.  

Теперь отправьте от <b>1 до 3 медиа</b> (фотографии или видео), чтобы другие могли узнать вас лучше.  
Или нажмите "Пропустить", чтобы продолжить. ⏩""" if lang == "ru" else """🎉 <b>Great!</b> Your hobbies have been successfully saved.  

Now, please send <b>1 to 3 media</b> (photos or videos) so others can get to know you better.  
Or press "Skip" to continue. ⏩"""

            await state.set_state(RegState.media)
            data = await state.get_data()
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Пропустить 🔄" if lang == "ru" else "Skip 🔄", callback_data="skip_album")]
            ])
            data = await state.get_data()
            
            msg = await callback_query.message.edit_text(txt, reply_markup=keyboard)
            data["idmsg_media"]=msg.message_id
            await state.update_data(data=data)

            await state.set_state(RegState.media)

            return

    # Генерация кнопок для текущей страницы
    page_size = 15
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
        if len(row) == 3 or i == len(interests[start_index:end_index]):
            inlinekeyboard.append(row)
            row = []

    navigation_buttons = []
    if current_page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️" if lang == "ru" else "⬅️ Back", callback_data="intrs_page_back"))
    if end_index < len(interests):
        navigation_buttons.append(InlineKeyboardButton(text="➡️" if lang == "ru" else "➡️ Next", callback_data="intrs_page_next"))
    if navigation_buttons:
        inlinekeyboard.append(navigation_buttons)

    inlinekeyboard.append(
        [InlineKeyboardButton(text=f"Сохранить ({len(hobbies)}/5) ✅" if lang == "ru" else f"Save ({len(hobbies)}/5) ✅", callback_data="intrs_done")]
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=inlinekeyboard)
    txt = (f"<b>Выбрано {len(hobbies)}/5 увлечений ✅</b>\n" if lang == "ru" else f"<b>Selected {len(hobbies)}/5 hobbies ✅</b>\n")
    txt += "Отлично, выбери до 5 увлечений, которые описывают тебя. 🌟\n\n➡️ Нажимай на кнопки, чтобы выбрать увлечения. Когда закончишь, нажми 'Сохранить'." if lang == "ru" else "Great, select up to 5 hobbies that describe you. 🌟\n\n➡️ Click on the buttons to select your hobbies. Once you're done, click 'Save'."

    await callback_query.message.edit_text(txt, reply_markup=keyboard)





from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from src.models import User
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext, BaseStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from src.utils.state import RegState
from src.utils.comands import set_user_specific_commands, delete_user_specific_commands


router = Router()

@router.message(CommandStart())
async def handle_message1(message: types.Message, state: FSMContext, lang: str, user: User = None, user_none: bool = False):
    if user:
        # Если имя не указано
        if user.name is None:
            txt = (
                "<b>🎉</b>\nТеперь давай настроим твой профиль, чтобы ты мог(ла) быстрее найти интересных людей. 🌟\n\n➡️ Укажи свое имя, чтобы мы могли начать!"
                if lang == "ru" else
                "<b>🎉</b>\nNow let’s set up your profile so you can start meeting interesting people faster. 🌟\n\n➡️ Please provide your name to get started!"
            )
            await state.set_state(RegState.name)
            await message.answer(txt)

        # Если имя указано, но пол не выбран
        elif user.name is not None and user.gender is None:
            txt = (
                f"<b>{user.name}, имя указано! ✅</b>\nОтлично, теперь укажи свой пол! 🌟\n\n➡️ Выбери один из вариантов:"
                if lang == "ru" else
                f"<b>{user.name}, name provided! ✅</b>\nGreat, now specify your gender! 🌟\n\n➡️ Choose one of the options:"
            )
            inline_keyboard = [
                [InlineKeyboardButton(text="👩 Женский" if lang == "ru" else "👩 Female", callback_data="gender_fem")],
                [InlineKeyboardButton(text="👨 Мужской" if lang == "ru" else "👨 Male", callback_data="gender_mal")],
                [InlineKeyboardButton(text="🌈 Другой" if lang == "ru" else "🌈 Other", callback_data="gender_oth")]
            ]
            keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
            await state.set_state(RegState.gender)
            await message.answer(txt, reply_markup=keyboard)

        # Если пол указан, но ориентация не выбрана
        elif user.name is not None and user.gender is not None and user.orientation is None:
            txt = (
                "<b>Пол указан! ✅</b>\nТеперь укажи свою ориентацию! 🌟\n\n➡️ Выбери один из вариантов:"
                if lang == "ru" else
                "<b>Gender saved! ✅</b>\nNow specify your orientation! 🌟\n\n➡️ Choose one of the options:"
            )
            if user.gender == 'mal':
                inline_keyboard = [
                    [InlineKeyboardButton(text="❤️ Гетеро" if lang == "ru" else "❤️ Hetero", callback_data="orientation_hetero")],
                    [InlineKeyboardButton(text="🌈 Гей" if lang == "ru" else "🌈 Gay", callback_data="orientation_gay")],
                    [InlineKeyboardButton(text="💛 Би" if lang == "ru" else "💛 Bi", callback_data="orientation_bi")]
                ]
            elif user.gender == 'fem':
                inline_keyboard = [
                    [InlineKeyboardButton(text="❤️ Гетеро" if lang == "ru" else "❤️ Hetero", callback_data="orientation_hetero")],
                    [InlineKeyboardButton(text="💖 Лесби" if lang == "ru" else "💖 Lesbian", callback_data="orientation_lesbian")],
                    [InlineKeyboardButton(text="💛 Би" if lang == "ru" else "💛 Bi", callback_data="orientation_bi")]
                ]
            elif user.gender == 'oth':
                inline_keyboard = [
                    [InlineKeyboardButton(text="❤️ Гетеро" if lang == "ru" else "❤️ Hetero", callback_data="orientation_hetero")],
                    [InlineKeyboardButton(text="🌈 Гей/Лесби" if lang == "ru" else "🌈 Gay/Lesbian", callback_data="orientation_gay_lesbian")],
                    [InlineKeyboardButton(text="💛 Би" if lang == "ru" else "💛 Bi", callback_data="orientation_bi")]
                ]
            keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
            await state.set_state(RegState.orientation)
            await message.answer(txt, reply_markup=keyboard)

        # Если ориентация указана, но не указаны предпочтения для просмотра
        elif user.name is not None and user.gender is not None and  user.orientation is not None and user.for_whom is None:
            txt = (
                "<b>Ориентация указана! ✅</b>\nТеперь укажи, кого ты хочешь видеть! 🌟\n\n➡️ Выбери один из вариантов:"
                if lang == "ru" else
                "<b>Orientation saved! ✅</b>\nNow specify who you want to see! 🌟\n\n➡️ Choose one of the options:"
            )
            inline_keyboard = [
                [InlineKeyboardButton(text="👩 Девушки" if lang == "ru" else "👩 Girls", callback_data="show_girls")],
                [InlineKeyboardButton(text="👨 Парни" if lang == "ru" else "👨 Boys", callback_data="show_boys")],
                [InlineKeyboardButton(text="🌍 Все" if lang == "ru" else "🌍 Everyone", callback_data="show_everyone")]
            ]
            keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
            await state.set_state(RegState.show)
            await message.answer(txt, reply_markup=keyboard)

        # Если предпочтения для просмотра указаны, но возраст не указан
        elif user.name is not None and user.gender is not None and  user.orientation is not None and user.for_whom is not None and user.age is None:
            txt = (
                "<b>Параметры просмотра указаны! ✅</b>\nТеперь укажи свой возраст! 🌟\n\n➡️ Введите ваш возраст (минимум 16 лет):"
                if lang == "ru" else
                "<b>Viewing preferences saved! ✅</b>\nNow specify your age! 🌟\n\n➡️ Enter your age (minimum 16 years):"
            )
            await state.set_state(RegState.age)
            await message.answer(txt)

        # Если все данные собраны, переходим к следующему шагу
        elif user.name is not None and user.gender is not None and  user.orientation is not None and user.for_whom is not None and user.age is not None and user.preferences is None:
            txt = (
                "<b>Возраст указан! ✅</b>\nТеперь укажи свои цели! 🌟\n\n➡️ Выбери цели из предложенных вариантов:"
                if lang == "ru" else
                "<b>Age saved! ✅</b>\nNow specify your goals! 🌟\n\n➡️ Choose your goals from the options provided:"
            )
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
        elif user.name is not None and user.age is not None and user.gender is not None and  user.orientation is not None and user.for_whom is not None and user.preferences is not None and user.location is None:

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

➡️ Пожалуйста, нажми кнопку ниже, чтобы отправить свою локацию. Не переживай, мы увидим только <b>приблизительное местоположение</b>.
"""
            else:
                txt = """<b>Search goals saved! ✅</b>
Great, now we need your location to suggest people nearby. 🌍

➡️ Please press the button below to share your location. Don’t worry, we will only see your <b>approximate location</b>.
"""
            await state.set_state(RegState.location)
            await message.bot.send_message(message.from_user.id ,text=txt, reply_markup=keyboard)

        elif user.name is not None and user.age is not None and user.gender is not None and  user.orientation is not None and user.for_whom is not None and user.preferences is not None and user.location is not None and user.about is None:
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
            await message.bot.send_message(message.from_user.id, txt)
        elif user.name is not None and user.age is not None and user.gender is not None and user.orientation is not None and user.for_whom is not None and user.preferences is not None and user.location is not None and user.about is not None and user.hobbies is None:
            state_data = await state.get_data()
            current_page = state_data.get("current_page", 1)
            hobbies = state_data.get("selected_hobbies", [])  # Загружаем хобби из состояния или базы

            if len(hobbies) < 5:
                await state.set_state(RegState.hobbies)

                # Увлечения на двух языках с номерами
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
                page_size = 10
                start_index = (current_page - 1) * page_size
                end_index = start_index + page_size

                # Генерация кнопок для текущей страницы
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

                # Добавляем кнопки навигации
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

                if lang == "ru":
                    if hobbies:
                        txt = f"<b>У вас уже выбрано {len(hobbies)}/5 увлечений ✅</b>\n"
                    else:
                        txt = ""
                    txt += "Отлично, теперь выбери до 5 увлечений, которые описывают тебя. 🌟\n\n➡️ Нажимай на кнопки, чтобы выбрать увлечения. Когда закончишь, нажми \"<b>Сохранить✅</b>\"."
                else:
                    if hobbies:
                        txt = f"<b>You have already selected {len(hobbies)}/5 hobbies ✅</b>\n"
                    else:
                        txt = ""
                    txt += "Great, now select up to 5 hobbies that describe you. 🌟\n\n➡️ Click on the buttons to select your hobbies. Once you're done, click \"<b>Save✅</b>\"."

                await state.update_data(current_page=current_page, hobbies=hobbies)  # Сохраняем данные в состояние
                await message.answer(txt, reply_markup=keyboard)


            elif len(hobbies) == 5:
                txt = """

        Теперь отправьте от <b>1 до 3 медиа</b> (фотографии или видео), чтобы другие могли узнать вас лучше.  
        Или нажмите "Пропустить", чтобы продолжить. ⏩""" if lang == "ru" else """

        Now, please send <b>1 to 3 media</b> (photos or videos) so others can get to know you better.  
        Or press "Skip" to continue. ⏩"""
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Пропустить 🔄" if lang == "ru" else "Skip 🔄", callback_data="skip_album")]
                ])
                await state.set_state(RegState.media)
                data = await state.get_data()

                msg = await message.bot.send_message(chat_id=message.from_user.id, text=txt, reply_markup=keyboard)
                data["idmsg_media"] = msg.message_id
                await state.update_data(data=data)

        else:
            
            if lang == "ru":
                button_text = "🚀 Начать поиск"
            else:
                button_text = "🚀 Start Search"

            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text=button_text)]
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )
            await set_user_specific_commands(message.bot, message.from_user.id, lang )
            response = (
        "ℹ️ Воспользуйтесь боковым меню ↙️\nчтобы открыть детали подписки или посмотреть профиль." 
        if lang == "ru" 
        else "ℹ️ Use the side menu ↙️\nto access subscription details or view your profile."
    )
            await message.answer(response, reply_markup=keyboard)

            
        









@router.message(Command("block"))
async def handle_message(message: types.Message, user: User = None, user_none: bool = False):
    user= await User.get_or_none(user_id=message.from_user.id)
    # if user:
    #     user.status_block="Deactive"
    #     await user.save()
    await delete_user_specific_commands(message.bot, message.from_user.id)

    

@router.message(Command("del"))
async def handle_message(message: types.Message, state: FSMContext, user: User = None, user_none: bool = False):
    user= await User.get_or_none(user_id=message.from_user.id)
    
    if user:
        await user.delete()
        # await user.save()

        
async def choise_lang(message: types.Message, lang: str):
    if lang['lang']=="ru":
    
        txt="""<b>Привет! 👋</b>
На связи <b>💖Emi-Date💖</b> — твой помощник в мире знакомств для людей в эмиграции. 🌍✨

Чтобы начать, пожалуйста, выбери язык, который тебе удобен:
"""
    else:
        txt="""<b>Hi there! 👋</b>
Welcome to <b>💖Emi-Date💖</b> — your go-to bot for connecting with people in emigration. 🌍✨

To get started, please select your preferred language:
"""
    
    # Кнопки для выбора языка
    
    inline_keyboard=[]
    inline_keyboard.append([InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")])
    inline_keyboard.append([InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await message.answer(text=txt, reply_markup=keyboard)

















@router.callback_query(lambda c: "lang_" in c.data)
async def callback_handler(callback_query: CallbackQuery, state: FSMContext, lang: str):
    lang = (callback_query.data.split("_"))[1]
    user_id = callback_query.from_user.id
    user= await User.get_or_none(user_id=user_id)
    if user:
        user.lang=lang
        await user.save()
    if user.name==None:
        keyboard = None
        if lang == "ru":
            txt = """<b>Отлично! 🎉</b>
Нажми /start, чтобы быстрее найти интересных людей. 🌟

"""
        else:
            txt = """<b>Great! 🎉</b
Tap /start to quickly find interesting people. 🌟
    """
        await callback_query.bot.edit_message_text(text=txt, chat_id=user_id, message_id=callback_query.message.message_id, reply_markup=None)
        
       


  






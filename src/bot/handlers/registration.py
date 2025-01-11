from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from src.models import User
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext, BaseStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from src.utils.state import RegState


router = Router()

@router.message(CommandStart())
async def handle_message(message: types.Message,state: FSMContext, lang:str, user: User = None, user_none: bool = False):
    if user:
        if user.name is None:
            if lang == "ru":
                txt = """<b>🎉</b>
Теперь давай настроим твой профиль, чтобы ты мог(ла) быстрее найти интересных людей. 🌟

➡️ Укажи свое имя, чтобы мы могли начать!
"""
            else:
                txt = """<b>🎉</b>
Now let’s set up your profile so you can start meeting interesting people faster. 🌟

➡️ Please provide your name to get started!
    """
            await state.set_state(RegState.name)
            await message.answer(txt)
        elif user.name is not None and user.age ==None:
            if lang == "ru":
                txt = f"""<b>{user.name}, имя указано! ✅</b>
Отлично, давай продолжим настройку твоего профиля. 🌟

➡️ Пожалуйста, укажи свой возраст, чтобы мы могли предложить подходящих людей!
"""
            else:
                txt = f"""<b>{user.name}, name provided! ✅</b>
Great, let’s continue setting up your profile. 🌟

➡️ Please provide your age so we can suggest suitable matches!
"""
            await state.set_state(RegState.age)
            await message.answer(txt)
        elif user.name is not  None and user.age is not None and user.gender is None:
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
        elif user.name is not  None and user.age is not None and user.gender is not None and user.preferences ==None:
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
            await message.bot.send_message(message.from_user.id ,text=txt, reply_markup=keyboard)
        elif user.name is not None and user.age is not None and user.gender is not None and user.preferences is not None and user.location is None:

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

        elif user.name is not None and user.age is not None and user.gender is not None and user.preferences is not None and user.location is not None and user.about is None:
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
        elif user.name is not None and user.age is not None and user.gender is not None and user.preferences is not None and user.location is not None and user.about is not None and (user.hobbies is None or len(user.hobbies) < 5):
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
            hobbies = user.hobbies or []  # Получаем текущие увлечения пользователя

            # Формируем кнопки для увлечений, по 3 в ряд
            for i, (number, interest_ru, interest_en) in enumerate(interests[:15], start=1):
                text = ("🔹" if str(number) in hobbies else "") + (interest_ru if lang == "ru" else interest_en)
                row.append(InlineKeyboardButton(
                    text=text,
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
                if hobbies:
                    txt = f"<b>У вас уже выбрано {len(hobbies)}/5 увлечений ✅</b>\n"
                else:
                    txt = "<b>Записали ✅</b>\n"
                txt += "Отлично, теперь выбери до 5 увлечений, которые описывают тебя. 🌟\n\n➡️ Нажимай на кнопки, чтобы выбрать увлечения. Когда закончишь, нажми \"<b>Сохранить✅</b>\"."
            else:
                if hobbies:
                    txt = f"<b>You have already selected {len(hobbies)}/5 hobbies ✅</b>\n"
                else:
                    txt = "<b>Saved ✅</b>\n"
                txt += "Great, now select up to 5 hobbies that describe you. 🌟\n\n➡️ Click on the buttons to select your hobbies. Once you're done, click \"<b>Save✅</b>\"."

            await message.answer(txt, reply_markup=keyboard)
        elif user.name is not None and user.age is not None and user.gender is not None and user.preferences is not None and user.location is not None and user.about is not None and user.hobbies is not None and user.medias is None:
            txt ="""

Теперь отправьте от <b>1 до 3 медиа</b> (фотографии или видео), чтобы другие могли узнать вас лучше.  
Или нажмите "Пропустить", чтобы продолжить. ⏩""" if lang == "ru" else """

Now, please send <b>1 to 3 media</b> (photos or videos) so others can get to know you better.  
Or press "Skip" to continue. ⏩"""
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Пропустить 🔄" if lang == "ru" else "Skip 🔄", callback_data="skip_album")]
                ])
            await state.set_state(RegState.media)
            data = await state.get_data()
            
            msg = await message.bot.send_message(chat_id=message.from_user.id ,text=txt, reply_markup=keyboard)
            data["idmsg_media"]=msg.message_id
            await state.update_data(data=data)


            
        









@router.message(Command("block"))
async def handle_message(message: types.Message, user: User = None, user_none: bool = False):
    user= await User.get_or_none(user_id=message.from_user.id)
    if user:
        user.status_block="Deactive"
        await user.save()

@router.message(Command("del"))
async def handle_message(message: types.Message, state: FSMContext, user: User = None, user_none: bool = False):
    user= await User.get_or_none(user_id=message.from_user.id)
    
    if user:
        user.medias=None
        await user.save()

        
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
Теперь давай настроим твой профиль, чтобы ты мог(ла) быстрее найти интересных людей. 🌟

➡️ Укажи свое имя, чтобы мы могли начать!
"""
        else:
            txt = """<b>Great! 🎉</b>
Now let’s set up your profile so you can start meeting interesting people faster. 🌟

➡️ Please provide your name to get started!
    """
        await callback_query.bot.edit_message_text(text=txt, chat_id=user_id, message_id=callback_query.message.message_id, reply_markup=None)
        
        
        await state.set_state(RegState.name)
        
    elif user.name is not  None and user.age ==None:
        keyboard = None
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
        await callback_query.bot.edit_message_text(text=txt, chat_id=user_id, message_id=callback_query.message.message_id, reply_markup=None)

        await state.set_state(RegState.age)

    elif user.name is not  None and user.age is not None and user.gender ==None:
        if lang == "ru":
            txt = """<b>Возраст указан! ✅</b>
Отлично, теперь укажи свой пол, чтобы мы могли сделать рекомендации ещё точнее. 🌟

➡️ Выбери один из вариантов:

""" 
            inline_keyboard=[]
            inline_keyboard.append([InlineKeyboardButton(text="👩 Женский", callback_data="gender_fem")])
            inline_keyboard.append([InlineKeyboardButton(text="👨 Мужской", callback_data="gender_mal")])
            inline_keyboard.append([InlineKeyboardButton(text="🌈 Другое", callback_data="gender_oth")])

            keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        else:
            txt = """<b>Age provided! ✅</b>
Great, now let’s specify your gender to make our suggestions even more accurate. 🌟

➡️ Please choose one of the options:

"""     
            inline_keyboard=[]
            inline_keyboard.append([InlineKeyboardButton(text="👩 Female", callback_data="gender_fem")])
            inline_keyboard.append([InlineKeyboardButton(text="👨 Male", callback_data="gender_mal")])
            inline_keyboard.append([InlineKeyboardButton(text="🌈 Other", callback_data="gender_oth")])

            keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        await state.set_state(RegState.gender)
        await callback_query.bot.edit_message_text(text=txt, chat_id=user_id, message_id=callback_query.message.message_id, reply_markup=keyboard)

    elif user.name is not  None and user.age is not None and user.gender is not None and user.preferences ==None:
        inline_keyboard = []
    
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
        await callback_query.bot.edit_message_text(text=txt, chat_id=user_id, message_id=callback_query.message.message_id, reply_markup=keyboard)

    elif user.name is not None and user.age is not None and user.gender is not None and user.preferences is not None and user.location is None:
    # Создаем клавиатуру с кнопкой отправки локации
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
        await callback_query.bot.edit_message_text(text=txt, chat_id=user_id, message_id=callback_query.message.message_id, reply_markup=keyboard)

    elif user.name is not None and user.age is not None and user.gender is not None and user.preferences is not None and user.location is not None and user.about is None:
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
    elif user.name is not None and user.age is not None and user.gender is not None and user.preferences is not None and user.location is not None and user.about is not None and user.hobbies is None:
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
        hobbies = user.hobbies or []  # Получаем текущие увлечения пользователя

        # Формируем кнопки для увлечений, по 3 в ряд
        for i, (number, interest_ru, interest_en) in enumerate(interests[:15], start=1):
            text = ("🔹" if str(number) in hobbies else "") + (interest_ru if lang == "ru" else interest_en)
            row.append(InlineKeyboardButton(
                text=text,
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
            if hobbies:
                txt = f"<b>У вас уже выбрано {len(hobbies)}/5 увлечений ✅</b>\n"
            else:
                txt = "<b>Записали ✅</b>\n"
            txt += "Отлично, теперь выбери до 5 увлечений, которые описывают тебя. 🌟\n\n➡️ Нажимай на кнопки, чтобы выбрать увлечения. Когда закончишь, нажми \"<b>Сохранить✅</b>\"."
        else:
            if hobbies:
                txt = f"<b>You have already selected {len(hobbies)}/5 hobbies ✅</b>\n"
            else:
                txt = "<b>Saved ✅</b>\n"
            txt += "Great, now select up to 5 hobbies that describe you. 🌟\n\n➡️ Click on the buttons to select your hobbies. Once you're done, click \"<b>Save✅</b>\"."

        await callback_query.bot.edit_message_text(text=txt, chat_id=user_id, message_id=callback_query.message.message_id, reply_markup=keyboard)
    elif user.name is not None and user.age is not None and user.gender is not None and user.preferences is not None and user.location is not None and user.about is not None and user.hobbies is not None and user.medias is None:
        txt ="""🎉 <b>Отлично!</b> Ваши хобби успешно сохранены.  

Теперь отправьте от <b>1 до 3 медиа</b> (фотографии или видео), чтобы другие могли узнать вас лучше.  
Или нажмите "Пропустить", чтобы продолжить. ⏩""" if lang == "ru" else """🎉 <b>Great!</b> Your hobbies have been successfully saved.  

Now, please send <b>1 to 3 media</b> (photos or videos) so others can get to know you better.  
Or press "Skip" to continue. ⏩"""
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Пропустить 🔄" if lang == "ru" else "Skip 🔄", callback_data="skip_album")]
            ])
        await state.set_state(RegState.media)
        data = await state.get_data()
        
        msg = await callback_query.bot.send_message(chat_id=callback_query.from_user.id ,text=txt, reply_markup=keyboard)
        data["idmsg_media"]=msg.message_id
        await state.update_data(data=data)




  






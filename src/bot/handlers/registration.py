from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from src.models import User
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext, BaseStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


router = Router()

@router.message(CommandStart())
async def handle_message(message: types.Message, user: User = None, user_none: bool = False):
    if user:
        await message.answer(f"Welcome back, {user.name}!")
    elif user_none:
        await message.answer("You are not registered. Please register to continue.")

@router.message(Command("block"))
async def handle_message(message: types.Message, user: User = None, user_none: bool = False):
    user= await User.get_or_none(user_id=message.from_user.id)
    if user:
        user.status_block="Deactive"
        await user.save()

@router.message(Command("del"))
async def handle_message(message: types.Message, user: User = None, user_none: bool = False):
    user= await User.get_or_none(user_id=message.from_user.id)
    
    if user:
        await user.delete()
        
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
async def callback_handler(callback_query: CallbackQuery, state: FSMContext ):
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
            
    elif user.name is not  None and user.age ==None:
        keyboard = None
        if lang == "ru":
            txt = """<b>Имя уже указано! ✅</b>
Отлично, давай продолжим настройку твоего профиля. 🌟

➡️ Пожалуйста, укажи свой возраст, чтобы мы могли предложить подходящих людей!
"""
        else:
            txt = """<b>Name already provided! ✅</b>
Great, let’s continue setting up your profile. 🌟

➡️ Please provide your age so we can suggest suitable matches!
"""
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

        keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
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
    elif user.name is not None and user.age is not None and user.gender is not None and user.preferences is not None and user.location is not None and user.about is not None and user.interests is None:
        keyboard = InlineKeyboardMarkup(row_width=3)
        
        # Увлечения на двух языках с номерами
        interests = [
            (1, "Спорт", "Sport"), (2, "Музыка", "Music"), (3, "Путешествия", "Travel"), 
            (4, "Кино", "Movies"), (5, "Кулинария", "Cooking"), (6, "Искусство", "Art"), 
            (7, "Танцы", "Dancing"), (8, "Технологии", "Technology"), (9, "Литература", "Literature"), 
            (10, "Фотография", "Photography"), (11, "Игры", "Games"), (12, "Природа", "Nature"), 
            (13, "Автомобили", "Cars"), (14, "Мода", "Fashion"), (15, "Здоровье", "Health")
        ]
    
    # Формируем кнопки для первой страницы
        for number, interest_ru, interest_en in interests[:15]:
            keyboard.add(InlineKeyboardButton(
                text=interest_ru if lang == "ru" else interest_en,
                callback_data=f"intrs_{number}"
            ))
    
    # Добавляем стрелки навигации
        keyboard.row(
            InlineKeyboardButton(text="⬅️" if lang == "ru" else "⬅️ Back", callback_data="intrs_page_prev"),
            InlineKeyboardButton(text="➡️" if lang == "ru" else "➡️ Next", callback_data="intrs_page_next")
        )
        
        if lang == "ru":
            txt = """<b>Расскажи о себе указано! ✅</b>
Отлично, теперь выбери до 5 увлечений, которые описывают тебя. 🌟

➡️ Нажимай на кнопки, чтобы выбрать увлечения. Когда закончишь, нажми "Далее".
"""
        else:
            txt = """<b>About yourself saved! ✅</b>
Great, now select up to 5 hobbies that describe you. 🌟

➡️ Click on the buttons to select your hobbies. Once you're done, click "Next".
"""


    await callback_query.bot.edit_message_text(text=txt, chat_id=user_id, message_id=callback_query.message.message_id, reply_markup=keyboard)
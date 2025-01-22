from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand, BotCommandScopeChat
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



@router.message(Command("lang"))
async def set_name(message: types.Message, state: FSMContext, lang: str):
    user = await User.get_or_none(user_id=message.from_user.id)
    if user.lang:
        if user.lang=="ru":
            lang='en'
            user.lang=lang
            await user.save()
        else:
            lang='ru'
            user.lang=lang
            await user.save()
        await set_user_specific_commands(message.bot, message.from_user.id, lang)
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
        txt ="""Вы измменили язык ✅
        
ℹ️ Воспользуйтесь боковым меню ↙️\nчтобы открыть детали подписки или посмотреть профиль.""" if lang=='ru' else"""You have changed the language ✅

ℹ️ Use the side menu ↙️\nto access subscription details or view your profile."""

        await message.answer(txt, reply_markup=keyboard)





async def set_user_specific_commands(bot:Bot, user_id, lang):
    # Определяем команды для пользователя
    user_specific_commands = [
        
        BotCommand(command="myprofile", description="Профиль" if lang=='ru' else "Profile"),
        BotCommand(command="help", description="Помощь"if lang=='ru' else "Help"),
        BotCommand(command="subs", description="Подписка" if lang=='ru' else "Subscription"),
        BotCommand(command="ref", description="Реф. программа" if lang=='ru' else "Ref. program"),
        BotCommand(command="lang", description="Изменить язык" if lang=='ru' else "Change language")
    ]

    # Устанавливаем команды только для указанного пользователя
    await bot.set_my_commands(
        commands=user_specific_commands,
        scope=BotCommandScopeChat(chat_id=user_id)
    )

async def delete_user_specific_commands(bot: Bot, user_id: int):
    """
    Удаляет команды, установленные для конкретного пользователя.
    """
    await bot.delete_my_commands(
        scope=BotCommandScopeChat(chat_id=user_id)
    )
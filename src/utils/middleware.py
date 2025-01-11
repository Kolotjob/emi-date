import logging
from aiogram import BaseMiddleware
from aiogram.types import Update
from typing import Callable, Any, Awaitable
from src.models import User
from aiogram.types import CallbackQuery
from src.utils.generate_uid import generate_uid_code
from src.bot.handlers.registration import choise_lang


class LoggingMiddleware(BaseMiddleware):
    """
    Middleware for logging all incoming updates and outgoing responses.
    """

    async def __call__(
        self,
        handler: Callable[[Update, dict], Awaitable[Any]],
        event: Update,
        data: dict,
    ) -> Any:
        # Логируем входящее событие
        logging.info(f"Incoming update: {event}")

        # Получаем user_id из обновления
        user_id = event.from_user.id if event.from_user else None

        if user_id:
            # Проверяем, существует ли пользователь в базе данных
            user = await User.get_or_none(user_id=user_id)
            if user:
                if user.status_block == "Active":
                    data["user"] = user 
                    if user.lang =="nochoise":
                        data["lang"]= "ru" if event.from_user.language_code=="ru" or event.from_user.language_code=="uk" else "en"
                        return await choise_lang(event, data)
                    else:
                        data["lang"]=user.lang
                else:
                    # Если пользователь заблокирован, возвращаем статус 403
                    await event.answer("Ваш аккаунт заблокирован.")
                    return 403
            else:
                # Проверяем, есть ли реферальный код в сообщении команды
                if event.text and "/start" in event.text:
                    parts = event.text.split(" ")
                    if len(parts) > 1:
                        uid_ref = parts[1]  # Получаем реферальный код
                        ref_user = await User.get_or_none(uid_code=uid_ref)
                        if ref_user:
                            uid_ref=ref_user.uid_code
                            if ref_user.lang == "ru":
                                await event.bot.send_message(ref_user.user_id, "У вас новый реферал")
                            else:
                                await event.bot.send_message(ref_user.user_id, "You have a new referral")
                        else:
                            uid_ref = None
                    else:
                        uid_ref = None
                else:
                    uid_ref = None

                # Генерируем уникальный UID для нового пользователя
                users = await User.all().values_list("uid_code", flat=True)
                uid = await generate_uid_code(uids=users)

                # Создаём нового пользователя
                user = await User.create(user_id=user_id, uid_code=uid, referral_uid=uid_ref)
                data["user"] = user 
                data["lang"]= "ru" if event.from_user.language_code=="ru" or event.from_user.language_code=="uk" else "en"
                return await choise_lang(event, data) # Помечаем, что пользователь отсутствует

        # Передаём управление следующему обработчику
        
        response = await handler(event, data)

        # Логируем ответ
        logging.info(f"Outgoing response: {response}")

        return response




class CallbackMiddleware(BaseMiddleware):
    """
    Middleware для обработки callback-запросов.
    Проверяет статус пользователя и передаёт язык пользователя.
    """

    async def __call__(
        self,
        handler: Callable[[CallbackQuery, dict], Awaitable[Any]],
        event: CallbackQuery,
        data: dict,
    ) -> Any:
        # Логируем входящее событие
        logging.info(f"Incoming callback query: {event}")

        # Получаем user_id из callback
        user_id = event.from_user.id if event.from_user else None

        if user_id:
            # Проверяем, существует ли пользователь в базе данных
            user = await User.get_or_none(user_id=user_id)
            if user:
                if user.status_block == "Active":
                    data["user"] = user
                    data["lang"] = user.lang or ("ru" if event.from_user.language_code in ["ru", "uk"] else "en")
                else:
                    # Если пользователь заблокирован, отправляем сообщение и возвращаем статус 403
                    await event.answer("Ваш аккаунт заблокирован.", show_alert=True)
                    return 403
            else:
                # Если пользователь отсутствует, предлагаем выбрать язык
                data["lang"] = "ru" if event.from_user.language_code in ["ru", "uk"] else "en"
                if event.data == "lang_ru" or event.data == "lang_en":
                    data["lang"] = "ru" if event.data == "lang_ru" else "en"
                    return await handler(event, data)
                return await choise_lang(event.message, data)

        # Передаём управление следующему обработчику
        response = await handler(event, data)

        # Логируем ответ
        logging.info(f"Outgoing response for callback query: {response}")

        return response

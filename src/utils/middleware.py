import logging
from aiogram import BaseMiddleware, types
from aiogram.types import Update
from typing import Callable, Any, Awaitable
from aiogram.fsm.context import FSMContext
from src.models import User
from aiogram.types import CallbackQuery
from src.utils.generate_uid import generate_uid_code
from src.bot.handlers.registration import choise_lang


class LoggingMiddleware(BaseMiddleware):
    """
    Middleware for logging all incoming updates and outgoing responses,
    ensuring user profile completeness and language setup.
    """

    async def __call__(
        self,
        handler: Callable[[Update, dict], Awaitable[Any]],
        event: Update,
        data: dict,
    ) -> Any:
        # Логируем входящее событие
        logging.info(f"Incoming update: {event}")
        state: FSMContext
        state: FSMContext = data.get("state")  # FSMContext передается через data
        current_state = await state.get_state() if state else None
        # Получаем user_id из обновления
        user_id = event.from_user.id if event.from_user else None

        if user_id:
            # Проверяем, существует ли пользователь в базе данных
            user = await User.get_or_none(user_id=user_id)
            if user:
                if user.status_block == "Active":
                    data["user"] = user
                    
                    # Устанавливаем язык
                    if user.lang == "nochoise":
                        data["lang"] = "ru" if event.from_user.language_code in ["ru", "uk"] else "en"
                        return await choise_lang(event, data)
                    else:
                        data["lang"] = user.lang

                    # Проверка на полноту профиля
                    
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
                        user.medias
                    ]) and event.text and ("/start" not in event.text and "/del" not in event.text) and current_state is None:
                        message_text = (
                            "Кажется, ваш профиль заполнен не до конца. \u2028"
                            "Нажмите /start, чтобы заполнить профиль и скорее приступить к поиску нужных людей."
                            if user.lang == "ru" else
                            "It seems your profile is incomplete. \u2028"
                            "Press /start to complete your profile and start connecting with people."
                        )
                        if isinstance(event, types.Message):
                            await event.answer(message_text)
                        return
                else:
                    # Если пользователь заблокирован, возвращаем статус 403
                    if isinstance(event, types.Message):
                        await event.answer("Ваш аккаунт заблокирован." if user.lang == "ru" else "Your account is blocked.")
                    return 403
            else:
                # Новый пользователь
                uid_ref = None
                if event.text and "/start" in event.text:
                    parts = event.text.split(" ")
                    if len(parts) > 1:
                        uid_ref = parts[1]
                        ref_user = await User.get_or_none(uid_code=uid_ref)
                        if ref_user:
                            if ref_user.lang == "ru":
                                await event.bot.send_message(ref_user.user_id, "У вас новый реферал")
                            else:
                                await event.bot.send_message(ref_user.user_id, "You have a new referral")

                # Генерация UID
                users = await User.all().values_list("uid_code", flat=True)
                uid = await generate_uid_code(uids=users)

                # Создание нового пользователя
                user = await User.create(user_id=user_id, uid_code=uid, referral_uid=uid_ref)
                data["user"] = user
                data["lang"] = "ru" if event.from_user.language_code in ["ru", "uk"] else "en"
                return await choise_lang(event, data)

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

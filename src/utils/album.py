from aiogram import BaseMiddleware, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from typing import Callable, Awaitable, Dict, Any, List, Optional
from cachetools import TTLCache
from asyncio import sleep
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
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


DEFAULT_LATENCY = 0.2
DEFAULT_TTL = 0.600

router = Router()
# Middleware для обработки меди-альбомов
class AlbumMiddleware(BaseMiddleware):
    def __init__(
        self,
        groupmedia_handler: Callable[[Message, List[Dict[str, str]], List[int]], Awaitable[Any]],
        latency: float = DEFAULT_LATENCY,
        ttl: float = DEFAULT_TTL,
    ) -> None:
        super().__init__()
        self.groupmedia_handler = groupmedia_handler
        self.latency = latency
        self.cache: TTLCache = TTLCache(maxsize=10_000, ttl=ttl)

    @staticmethod
    async def get_media_data(message: Message) -> Optional[Dict[str, str]]:
        if message.photo:
            return {"file_id": message.photo[-1].file_id, "type": "photo", "message_id": message.message_id}
        if message.video:
            return {"file_id": message.video.file_id, "type": "video", "message_id": message.message_id}
        return None

    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, Message) and event.media_group_id is not None:
            state: FSMContext = data.get("state")

            if not state:
                return await handler(event, data)

            current_state: Optional[State] = await state.get_state()

            # Проверяем, находится ли пользователь в состоянии RegState.media
            if current_state != "RegState:media":
                return 403

            key = event.media_group_id
            media_data = await self.get_media_data(event)

            if not media_data:
                return await handler(event, data)

            # Если альбом уже собирается, добавляем текущий файл
            if key in self.cache:
                self.cache[key]["media_data"].append(media_data)
                return None

            # Создаем новый альбом в кэше
            self.cache[key] = {
                "media_data": [media_data]
            }

            # Ждем, пока все части альбома дойдут
            await sleep(self.latency)

            # Передаем собранный альбом и message_id для удаления в groupmedia_handler
            media_data_list = self.cache.pop(key)["media_data"]
            message_ids = [media["message_id"] for media in media_data_list]
            return await self.groupmedia_handler(event, media_data_list, message_ids, state)

        return await handler(event, data)
    




# Функция для обработки одиночного медиа
@router.message(RegState.media)
async def set_media(message: types.Message, user: User, state: FSMContext, lang: str):
    if message.media_group_id is None and (message.photo or message.video):  
        # Проверяем одиночные фото/видео
        if user:
            media = user.medias or []
            if len(media) < 3:
                media_data = {
                    "file_id": message.photo[-1].file_id if message.photo else message.video.file_id,
                    "type": "photo" if message.photo else "video"
                }
                await message.bot.delete_message(message.from_user.id, message.message_id)
                media.append(media_data)
                user.medias = media
                await user.save()

                

                # Обновляем сообщение прогресса
                data = await state.get_data()
                msg_id = None
                if "idmsg_media" in data:
                    msg_id=data["idmsg_media"]
                count = len(media)
                if count ==3:
                    txt = (
                    f"Сохранено {count}/3 медиа. Нажмите 'Сохранить'." 
                    if lang == "ru" 
                    else f"Saved {count}/3 media. Click 'Save'."
                )
                else:   
                    txt = (
                        f"Сохранено {count}/3 медиа. Отправьте ещё одно или нажмите 'Сохранить'." 
                        if lang == "ru" 
                        else f"Saved {count}/3 media. Send another one or click 'Save'."
                    )

                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Сохранить ✅" if lang == "ru" else "Save ✅", callback_data="save_album")]
                ])

                if msg_id:
                    try:
                        await message.bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id, text=txt, reply_markup=keyboard)
                    except:
                        sent_message = await message.bot.send_message(chat_id=message.chat.id, text=txt, reply_markup=keyboard)
                        await state.update_data(idmsg_media=sent_message.message_id)
                else:
                    sent_message = await message.bot.send_message(chat_id=message.chat.id, text=txt, reply_markup=keyboard)
                    await state.update_data(idmsg_media=sent_message.message_id)
            else:
                txt = "Вы уже отправили максимальное количество медиа! 📸" if lang == "ru" else "You have already sent the maximum amount of media! 📸"
                await message.answer(txt)

# Функция для обработки меди-альбомов
async def groupmedia(message: Message, media_data_list: List[Dict[str, str]], message_ids , state: FSMContext):
    
    chat_id = message.chat.id  # Или используйте другой chat_id, если нужно
    print(message_ids)
    # Проверяем количество файлов в базе данных
    for id in message_ids:
        await message.bot.delete_message(message.from_user.id, id)
    user = await User.get_or_none(user_id=message.from_user.id)
    if not user:
        await message.answer("Ошибка: пользователь не найден.")
        return
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сохранить ✅" if user.lang == "ru" else "Save ✅", callback_data="save_album")]
    ])
    existing_files = user.medias or []

    # Если уже есть 2 файла, добавляем только первый файл из альбома
    if len(existing_files) == 2:
        existing_files.append(media_data_list[0])
        user.medias = existing_files
        await user.save()

        # Удаляем сообщение с медиа

        # Обновляем сообщение прогресса
        txt = (
            "Сохранён только первый файл из альбома. Теперь у вас 3/3 медиа. Нажмите 'Сохранить'." 
            if user.lang == "ru" 
            else "Only the first file from the album has been saved. You now have 3/3 media. Click 'Save'."
        )
        data = await state.get_data()
        msg_id = None
        if "idmsg_media" in data:
            msg_id=data["idmsg_media"]

        if msg_id:
            try:
                await message.bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id, text=txt, reply_markup=keyboard)
            except:
                sent_message = await message.bot.send_message(chat_id=message.chat.id, text=txt, reply_markup=keyboard)
                await state.update_data(idmsg_media=sent_message.message_id)
        else:
            sent_message = await message.bot.send_message(chat_id=message.chat.id, text=txt, reply_markup=keyboard)
            await state.update_data(idmsg_media=sent_message.message_id)
        return

    # Если альбом содержит больше 3 файлов, сохраняем только первые 3
    if len(existing_files) + len(media_data_list) > 3:
        remaining_slots = 3 - len(existing_files)
        existing_files.extend(media_data_list[:remaining_slots])
        user.medias = existing_files
        await user.save()

        # Удаляем сообщение с медиа
        # await message.delete()

        # Обновляем сообщение прогресса
        txt = (
            f"Сохранены только первые {remaining_slots} файла из альбома. Теперь у вас 3/3 медиа. Нажмите 'Сохранить'."
            if user.lang == "ru" 
            else f"Only the first {remaining_slots} files from the album have been saved. You now have 3/3 media. Click 'Save'."
        )
        data = await state.get_data()
        msg_id = None
        if "idmsg_media" in data:
            msg_id=data["idmsg_media"]

        if msg_id:
            try:
                await message.bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id, text=txt, reply_markup=keyboard)
            except:
                sent_message = await message.bot.send_message(chat_id=message.chat.id, text=txt, reply_markup=keyboard)
                await state.update_data(idmsg_media=sent_message.message_id)
        else:
            sent_message = await message.bot.send_message(chat_id=message.chat.id, text=txt, reply_markup=keyboard)
            await state.update_data(idmsg_media=sent_message.message_id)
        return

    # Если всё в порядке, сохраняем весь альбом
    existing_files.extend(media_data_list)
    user.medias = existing_files
    await user.save()

    # Удаляем сообщение с медиа

    # Обновляем сообщение прогресса
    if existing_files==3:
        txt = (
        f"Сохранено {len(existing_files)}/3 медиа. Нажать 'Сохранить'."
        if user.lang == "ru" 
        else f"Saved {len(existing_files)}/3 media. Click 'Save'."
    )
    else:
        txt = (
            f"Сохранено {len(existing_files)}/3 медиа. Можете отправить ещё одно или нажать 'Сохранить'."
            if user.lang == "ru" 
            else f"Saved {len(existing_files)}/3 media. You can send another one or click 'Save'."
        )

    

    # await message.answer(txt, reply_markup=keyboard)÷
    data = await state.get_data()
    msg_id = None
    if "idmsg_media" in data:
        msg_id=data["idmsg_media"]

    if msg_id:
        try:
            await message.bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id, text=txt, reply_markup=keyboard)
        except:
            sent_message = await message.bot.send_message(chat_id=message.chat.id, text=txt, reply_markup=keyboard)
            await state.update_data(idmsg_media=sent_message.message_id)
    else:
        sent_message = await message.bot.send_message(chat_id=message.chat.id, text=txt, reply_markup=keyboard)
        await state.update_data(idmsg_media=sent_message.message_id)


@router.callback_query(lambda c: "skip_album" in c.data, RegState.media)
async def callback_handler(callback_query: CallbackQuery, user: User, state: FSMContext, lang: str):
   print(0)
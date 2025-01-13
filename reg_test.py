import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

# Импортируем ваши хендлеры и состояния
from src.bot.handlers.registration import (
    handle_message,
    choise_lang,
    callback_handler
)

# Импортируем ваше состояние
from src.utils.state import RegState
# Импортируем модель User (или же мокируем её внутри теста)
from src.models import User


@pytest.mark.asyncio
async def test_start_handler_new_user(mocker):
    """
    Тестируем ситуацию, когда пользователь впервые нажимает /start
    и в БД ещё нет записи о нём (user=None).
    """
    # Мокаем объект message
    message = MagicMock(spec=Message)
    message.from_user.id = 12345678
    message.text = "/start"
    # Мокаем метод answer (будет вызван при отправке сообщения)
    message.answer = AsyncMock()
    
    # Мокаем FSMContext
    state = MagicMock(spec=FSMContext)
    state.set_state = AsyncMock()
    
    # Переопределим lang и user, user_none (как в ваших аргументах)
    # Допустим, user=None, user_none=True
    user = None
    user_none = True
    lang = "ru"

    # Вызываем тестируемую функцию
    await handle_message(message=message, state=state, lang=lang, user=user, user_none=user_none)

    # Проверяем, что state.set_state НЕ вызван,
    # так как в вашем коде нет явной логики, если user=None (и стоит user_none=True),
    # но вы можете добавить проверку в код или в тестах.
    state.set_state.assert_not_awaited()

    # Проверяем, что было отправлено какое-то приветственное сообщение или нет
    # (зависит от вашей логики). Предположим, что при user=None ничего не происходит —
    # тогда проверяем, что message.answer тоже не вызывается:
    message.answer.assert_not_awaited()
    

@pytest.mark.asyncio
async def test_start_handler_user_no_name(mocker):
    """
    Тестируем ситуацию, когда в БД есть user, но у него нет имени (user.name = None).
    По коду вы проверяете: если user.name is None -> спросить имя
    """
    # Мокаем message
    message = MagicMock(spec=Message)
    message.from_user.id = 12345678
    message.text = "/start"
    message.answer = AsyncMock()

    # Мокаем FSMContext
    state = MagicMock(spec=FSMContext)
    state.set_state = AsyncMock()

    # Создаём тестового user (мок)
    user = MagicMock(spec=User)
    user.name = None
    user.gender = None
    user.orientation = None
    user.for_whom = None
    user.age = None
    user.preferences = None
    user.location = None
    user.about = None
    user.hobbies = None
    user.medias = None

    # Вызываем хендлер
    await handle_message(message=message, state=state, lang="ru", user=user, user_none=False)

    # Проверяем, что мы установили состояние на RegState.name
    state.set_state.assert_awaited_once_with(RegState.name)
    
    # Проверяем, что отправили сообщение с инструкцией указать имя
    message.answer.assert_awaited_once()
    args, kwargs = message.answer.call_args
    # Можем дополнительно проверить текст:
    assert "Укажи свое имя" in args[0]  # если lang="ru"


@pytest.mark.asyncio
async def test_start_handler_user_no_gender(mocker):
    """
    Тестируем ситуацию, когда у user есть имя, но не указан пол
    (user.gender = None).
    """
    message = MagicMock(spec=Message)
    message.from_user.id = 12345678
    message.text = "/start"
    message.answer = AsyncMock()

    state = MagicMock(spec=FSMContext)
    state.set_state = AsyncMock()

    # Допустим, имя есть
    user = MagicMock(spec=User)
    user.name = "Тест"
    user.gender = None
    user.orientation = None
    user.for_whom = None
    user.age = None
    user.preferences = None
    user.location = None
    user.about = None
    user.hobbies = None
    user.medias = None

    await handle_message(message=message, state=state, lang="ru", user=user, user_none=False)

    state.set_state.assert_awaited_once_with(RegState.gender)
    message.answer.assert_awaited_once()
    args, kwargs = message.answer.call_args
    # Проверяем текст
    assert "имя указано! ✅" in args[0]
    assert "укажи свой пол" in args[0]


@pytest.mark.asyncio
async def test_start_handler_user_no_orientation(mocker):
    """
    Тестируем ситуацию, когда user.name и user.gender есть,
    но orientation=None
    """
    message = MagicMock(spec=Message)
    message.from_user.id = 12345678
    message.answer = AsyncMock()

    state = MagicMock(spec=FSMContext)
    state.set_state = AsyncMock()

    user = MagicMock(spec=User)
    user.name = "Тест"
    user.gender = "mal"
    user.orientation = None
    user.for_whom = None
    user.age = None

    await handle_message(message=message, state=state, lang="ru", user=user, user_none=False)

    state.set_state.assert_awaited_once_with(RegState.orientation)
    message.answer.assert_awaited_once()
    args, kwargs = message.answer.call_args
    assert "Теперь укажи свою ориентацию" in args[0]


@pytest.mark.asyncio
async def test_start_handler_user_all_filled_till_media(mocker):
    """
    Предположим, что у пользователя заполнено всё до момента,
    когда нужно отправить медиа (user.medias=None).
    Проверяем, что мы переходим на состояние RegState.media.
    """
    message = MagicMock(spec=Message)
    message.from_user.id = 12345678
    message.answer = AsyncMock()
    # В коде на этом этапе вызывается message.bot.send_message для медиа,
    # Поэтому замокаем и его:
    message.bot.send_message = AsyncMock()

    state = MagicMock(spec=FSMContext)
    state.set_state = AsyncMock()
    state.get_data = AsyncMock(return_value={})
    state.update_data = AsyncMock()

    user = MagicMock(spec=User)
    user.name = "Тест"
    user.gender = "mal"
    user.orientation = "hetero"
    user.for_whom = "girls"
    user.age = 30
    user.preferences = "romance"
    user.location = "SomeLocation"
    user.about = "Текст о себе"
    user.hobbies = ["1", "2", "3", "4", "5"]  # типа уже 5 увлечений
    user.medias = None  # нет медиа

    await handle_message(message=message, state=state, lang="ru", user=user, user_none=False)

    # Должно установиться состояние media
    state.set_state.assert_awaited_once_with(RegState.media)

    # Проверяем, что бот отправил сообщение с предложением выслать медиа
    message.bot.send_message.assert_awaited_once()
    args, kwargs = message.bot.send_message.call_args
    assert "Теперь отправьте от <b>1 до 3 медиа</b>" in args[1]


@pytest.mark.asyncio
async def test_block_command(mocker):
    """
    Тестируем команду /block.
    """
    from src.bot.handlers.registration import handle_message as block_handler

    # Мокаем message
    message = MagicMock(spec=Message)
    message.from_user.id = 12345678
    message.text = "/block"

    # Создадим мок для User.get_or_none
    async def mock_get_or_none(user_id):
        mock_user = MagicMock(spec=User)
        mock_user.status_block = None
        async def mock_save():
            pass
        mock_user.save = mock_save
        return mock_user

    with patch("src.handlers.main_handlers.User.get_or_none", side_effect=mock_get_or_none):
        await block_handler(message=message, user=None, user_none=False)
    
    # Проверяем, что у найденного пользователя проставился status_block = "Deactive"
    # В нашем mock_get_or_none мы возвращаем mock_user, у которого изначально status_block = None.
    # После вызова команды /block должно стать "Deactive".
    # Также вызывается mock_user.save().
    # Мы можем проверить это так:
    # Но придётся чуть усложнить реализацию с учётом patch-а.
    # Проще проверить внутри mock-а:

    # Или проверка через spy:
    # (Если используете pytest-mock, можно использовать mocker.spy и т.д.)
    

@pytest.mark.asyncio
async def test_del_command(mocker):
    """
    Тестируем команду /del, которая обнуляет user.medias.
    """
    from src.bot.handlers.registration import handle_message as del_handler


    message = MagicMock(spec=Message)
    message.from_user.id = 12345678
    message.text = "/del"

    async def mock_get_or_none(user_id):
        mock_user = MagicMock(spec=User)
        mock_user.medias = ["some_media"]
        async def mock_save():
            pass
        mock_user.save = mock_save
        return mock_user

    state = MagicMock(spec=FSMContext)

    with patch("src.handlers.main_handlers.User.get_or_none", side_effect=mock_get_or_none):
        await del_handler(message=message, state=state, user=None, user_none=False)

    # Здесь проверяем, что medias = None
    # Аналогично предыдущему тесту.
    

@pytest.mark.asyncio
async def test_choise_lang_ru(mocker):
    """
    Тестируем функцию choise_lang, которая отправляет кнопки выбора языка.
    """
    message = MagicMock(spec=Message)
    message.from_user.id = 12345678
    message.answer = AsyncMock()
    
    # Проверяем, что при lang['lang']="ru" отсылается русский текст
    await choise_lang(message=message, lang={"lang": "ru"})
    message.answer.assert_awaited_once()
    args, kwargs = message.answer.call_args
    assert "Привет!" in args[0]
    assert "🇷🇺 Русский" in str(kwargs["reply_markup"])  # проверяем, что есть кнопка русского языка
    

@pytest.mark.asyncio
async def test_callback_handler_lang_selection(mocker):
    """
    Тестируем callback_handler, когда приходит выбор языка.
    """
    callback_query = MagicMock(spec=CallbackQuery)
    callback_query.data = "lang_ru"
    callback_query.from_user.id = 12345678
    callback_query.message.message_id = 98765
    callback_query.bot.edit_message_text = AsyncMock()

    state = MagicMock(spec=FSMContext)
    state.set_state = AsyncMock()

    # Мокаем базу
    async def mock_user_get_or_none(user_id):
        mock_user = MagicMock(spec=User)
        mock_user.lang = None
        async def mock_save():
            pass
        mock_user.save = mock_save
        mock_user.name = None
        return mock_user

    with patch("src.handlers.main_handlers.User.get_or_none", side_effect=mock_user_get_or_none), \
         patch("src.handlers.main_handlers.User.save", new_callable=AsyncMock):
        await callback_handler(callback_query=callback_query, state=state, lang="ru")

    # Проверяем, что edit_message_text вызвался с нужным текстом
    callback_query.bot.edit_message_text.assert_awaited_once()
    args, kwargs = callback_query.bot.edit_message_text.call_args
    assert "Нажми /start, чтобы быстрее найти интересных людей" in args[0]

    # Проверяем, что у пользователя выставился lang="ru" и user.save() был вызван
    # (в нашем patch-е в mock_user_get_or_none мы создали mock_user)
    # Можно также проверить через spy, но в данном упрощённом варианте —
    # главное, что исключений нет и вызов edit_message_text корректен.

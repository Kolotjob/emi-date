from aiogram.fsm.state import StatesGroup
from aiogram.fsm.state import State


class RegState(StatesGroup):

    name =State()
    age = State()
    gender = State()
    preferences = State()
    location = State()
    about = State()
    media = State()
    hobbies = State()
    show = State()
    orientation = State()
    done = State()



 
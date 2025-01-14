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




class SearchPeople(StatesGroup):
    search = State()
    like = State()
    superlike = State()
    dislike = State()
    block = State()
    report = State()
    stop = State()
    message = State()
    show = State()
    show_profile = State()
    show_media = State()
    show_hobbies = State()
    show_about = State()
    show_location = State()
    show_preferences = State()


class ReditState(StatesGroup):

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
 
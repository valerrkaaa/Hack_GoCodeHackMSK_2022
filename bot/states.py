from aiogram.dispatcher.filters.state import State, StatesGroup


class Questionnaire(StatesGroup):
    start = State()
    text = State()
    image = State()

from aiogram.dispatcher.filters.state import State, StatesGroup


class Questionnaire(StatesGroup):
    text = State()
    image = State()

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from states import Questionnaire
from bot_token import token
from aiogram import types
import aiogram
import json
from typing import List


bot = aiogram.Bot(token=token)
dp = aiogram.Dispatcher(bot, storage=MemoryStorage())
questions: List[dict]


def init_questions():
    global questions
    with open('questions.json', 'r', encoding='utf-8') as file:
        questions = json.load(file)


@dp.message_handler(commands=['register'])
async def start(message: types.Message):
    await message.answer('Приветственное сообщение')
    await message.answer(questions[0]['text'])
    await Questionnaire.text.set()

    state = dp.current_state(user=message.from_user.id)
    async with state.proxy() as data:
        data['last_answer_id'] = 0
        data['answer_array'] = [{'answer_id': 1}]


@dp.message_handler(state=Questionnaire.text)
async def get_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        # TODO проверка на правильный тип того, что отправил пользователь

        data['answer_array'][data['last_answer_id']]['content'] = message.text
        data['answer_array'][data['last_answer_id']]['content_type'] = 'text'

        data['last_answer_id'] += 1
        data['answer_array'].append({'answer_id': data['last_answer_id']})
    if questions[data['last_answer_id']]['answer_type'] == 'text':
        await message.answer(questions[data['last_answer_id']]['text'])
        await state.set_state(Questionnaire.text)
    else:
        print('!')
        await state.finish()


def main():
    init_questions()
    aiogram.executor.start_polling(dp)


if __name__ == '__main__':
    main()

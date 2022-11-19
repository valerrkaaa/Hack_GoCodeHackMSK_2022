from excel_parser.excel_parser import get_json_from_excel
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
    try:
        questions = get_json_from_excel(
            'D:\\Programming\\python\\Programms\\Bots\\Hack_GoCodeHackMSK_2022\\excel_parser\\questions.xlsx')
        return True
    except FileNotFoundError:
        print('Не найден файл excel со списком вопросов!')
        return False
    # with open('questions.json', 'r', encoding='utf-8') as file:
    #     questions = json.load(file)


@dp.message_handler(commands=['register'])
async def start(message: types.Message):
    await message.answer('Приветственное сообщение')
    await message.answer(questions[0]['text'])
    await Questionnaire.text.set()

    state = dp.current_state(user=message.from_user.id)
    async with state.proxy() as data:
        data['last_answer_id'] = 0
        data['answer_array'] = [{'answer_id': data['last_answer_id']}]


@dp.message_handler(content_types=['text'], state=Questionnaire.text)
async def get_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        save_info_to_state_data(data, message.text)
        print(data['answer_array'])
    if data['last_answer_id'] == len(questions):
        finish_questionnaire_state(data['answer_array'][:-1])
        await state.finish()
        print('finish')
    else:
        await message.answer(questions[data['last_answer_id']]['text'])
        if questions[data['last_answer_id']]['answer_type'] == 'text':
            await message.answer('Спасибо, данные отправлены сотруднику нашей компании.\n'
                                 'Вам будет отправлено сообщение, когда он рассмотрит Вашу заявку.')
            await state.set_state(Questionnaire.text)
            print('wait text')
        else:
            await state.set_state(Questionnaire.image)
            print('wait img')


@dp.message_handler(content_types=['text'], state=Questionnaire.image)
async def hook_wrong_type_for_image(message: types.Message, state: FSMContext):
    await message.answer('Необходима фотография')


@dp.message_handler(content_types=['photo'], state=Questionnaire.image)
async def get_image(message: types.Message, state: FSMContext):
    photo_id = message.photo[0].file_id
    async with state.proxy() as data:
        save_info_to_state_data(data, photo_id)
        print(data['answer_array'])

        if data['last_answer_id'] == len(questions):
            finish_questionnaire_state(data['answer_array'][:-1])
            await message.answer('Спасибо, данные отправлены сотруднику нашей компании.\n'
                                 'Вам будет отправлено сообщение, когда он рассмотрит Вашу заявку.')
            await state.finish()
            print('finish')
        else:
            await message.answer(questions[data['last_answer_id']]['text'])
            if questions[data['last_answer_id']]['answer_type'] == 'text':
                await state.set_state(Questionnaire.text)
                print('wait text')
            else:
                await state.set_state(Questionnaire.image)
                print('wait img')


def finish_questionnaire_state(result_array: List[dict]):
    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(result_array, file, indent=4, ensure_ascii=False)


def save_info_to_state_data(data, content: str):
    data['answer_array'][data['last_answer_id']]['content'] = content
    data['answer_array'][data['last_answer_id']]['content_type'] = questions[data['last_answer_id']]['answer_type']
    data['answer_array'][data['last_answer_id']]['field_name'] = questions[data['last_answer_id']]['field_name']

    data['last_answer_id'] += 1
    data['answer_array'].append({'answer_id': data['last_answer_id']})


def main():
    if init_questions():
        aiogram.executor.start_polling(dp)


if __name__ == '__main__':
    main()

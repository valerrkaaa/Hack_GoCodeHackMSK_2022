from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from states import Questionnaire
from bot_runner import dp
from typing import List
import json
from Files import work_with_files
from PowerPoint import pptx_saver
from Word import word_saver

all_questions: List[list]
questions: List[dict]


def register_questionnaire_handlers(dp1: Dispatcher, question_list: List[dict]):
    global all_questions

    all_questions = question_list
    dp1.register_message_handler(start, commands=['register'])
    dp1.register_message_handler(get_text, content_types=['text'], state=Questionnaire.text)
    dp1.register_message_handler(hook_wrong_type_for_image, content_types=['text'], state=Questionnaire.image)
    dp1.register_message_handler(get_image, content_types=['photo'], state=Questionnaire.image)
    dp1.register_message_handler(reg, state=Questionnaire.start)


async def reg(message: types.Message, state: FSMContext):
    global questions

    if message.text in [str(i) for i in range(10)]:
        if int(message.text) >= len(all_questions):
            await message.answer(f'Введённое число больше {len(all_questions) - 1}')
            await message.answer('Введите номер формы опроса:')
            await state.set_state(Questionnaire.start)
        else:
            questions = all_questions[int(message.text)]
            await message.answer('Сообщение в начале опроса')
            await message.answer(questions[0]['text'])
            await state.set_state(Questionnaire.text)
            state = dp.current_state(user=message.from_user.id)
            async with state.proxy() as data:
                data['last_answer_id'] = 0
                data['answer_array'] = [{'answer_id': data['last_answer_id']}]
    else:
        await message.answer(f'Необходимо ввести число!')
        await message.answer('Введите номер формы опроса:')
        await state.set_state(Questionnaire.start)


# @dp.message_handler(commands=['register'])
async def start(message: types.Message):
    # await message.answer('Сообщение в начале опроса')
    # await message.answer(questions[0]['text'])
    # await Questionnaire.text.set()
    await message.answer('Введите номер формы опроса:')
    await Questionnaire.start.set()

    # state = dp.current_state(user=message.from_user.id)
    # async with state.proxy() as data:
    #     data['last_answer_id'] = 0
    #     data['answer_array'] = [{'answer_id': data['last_answer_id']}]


# @dp.message_handler(content_types=['text'], state=Questionnaire.text)
async def get_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        save_info_to_state_data(data, message.text)
    if data['last_answer_id'] == len(questions):
        await finish_questionnaire_state(data['answer_array'][:-1])
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


def save_info_to_state_data(data, content: str):
    data['answer_array'][data['last_answer_id']]['content'] = content
    data['answer_array'][data['last_answer_id']]['content_type'] = questions[data['last_answer_id']]['answer_type']
    data['answer_array'][data['last_answer_id']]['field_name'] = questions[data['last_answer_id']]['field_name']

    data['last_answer_id'] += 1
    data['answer_array'].append({'answer_id': data['last_answer_id']})


async def finish_questionnaire_state(result_array: List[dict]):
    # TODO сгенерировать файлы и сохранить в папку

    file_name = work_with_files.get_full_path('Files\\NewFiles\\' + result_array[0]['content'])
    await pptx_saver.save_pptx(result_array, file_name)
    await word_saver.save_word(result_array, file_name)
    await word_saver.save_pdf(file_name)

    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(result_array, file, indent=4, ensure_ascii=False)


# @dp.message_handler(content_types=['text'], state=Questionnaire.image)
async def hook_wrong_type_for_image(message: types.Message, state: FSMContext):
    if message.text == '-':
        async with state.proxy() as data:
            save_info_to_state_data(data, message.text)
            await message.answer(questions[data['last_answer_id']]['text'])
            if questions[data['last_answer_id']]['answer_type'] == 'text':
                await state.set_state(Questionnaire.text)
                print('wait text')
            else:
                await state.set_state(Questionnaire.image)
                print('wait img')
    else:
        await message.answer('Необходима фотография')


# @dp.message_handler(content_types=['photo'], state=Questionnaire.image)
async def get_image(message: types.Message, state: FSMContext):

    photo_path = work_with_files.get_full_path('Files\\tempimages\\' + message.photo[-1].file_id + '.jpg')

    await message.photo[-1].download(photo_path)
    async with state.proxy() as data:
        save_info_to_state_data(data, photo_path)

    if data['last_answer_id'] == len(questions):
        await finish_questionnaire_state(data['answer_array'][:-1])
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

from excel_parser.excel_parser import get_json_from_excel
from aiogram.utils import executor
import questionnaire_handlers
from bot_runner import dp


def get_questions():
    try:
        return get_json_from_excel(
            'D:\\Programming\\python\\Programms\\Bots\\Hack_GoCodeHackMSK_2022\\excel_parser\\questions.xlsx')
    except FileNotFoundError:
        print('Не найден файл excel со списком вопросов!')
        return None


def main():
    questions = get_questions()
    if questions:
        questionnaire_handlers.register_questionnaire_handlers(dp, questions)
        executor.start_polling(dp)


if __name__ == '__main__':
    main()


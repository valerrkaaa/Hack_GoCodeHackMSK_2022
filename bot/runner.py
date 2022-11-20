from excel_parser.excel_parser import get_json_from_excel
from Files.work_with_files import get_full_path
from aiogram.utils import executor
import questionnaire_handlers
from bot_runner import dp
import admin_handler


def get_questions(path):
    try:
        return get_json_from_excel(path)
    except FileNotFoundError:
        print('Не найден файл excel со списком вопросов!')
        return None


def main():
    questions = get_questions(get_full_path('excel_parser\\questions.xlsx'))
    if questions:
        questionnaire_handlers.register_questionnaire_handlers(dp, questions)
        admin_handler.register_admin_handlers(dp)
        executor.start_polling(dp)


if __name__ == '__main__':
    main()


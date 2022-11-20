import aiogram
from PowerPoint import pptx_saver
from Word import word_saver
import json
from Files import work_with_files


with open(r'D:\Programming\python\Programms\Bots\Hack_GoCodeHackMSK_2022\bot\result.json', 'r', encoding='utf-8') as file:
    result_array = json.load(file)


async def a():
    file_name = work_with_files.get_full_path('Files\\NewFiles\\' + result_array[0]['content'])
    await pptx_saver.save_pptx(result_array, file_name)
    await word_saver.save_word(result_array, file_name)

if __name__ == '__main__':
    a()

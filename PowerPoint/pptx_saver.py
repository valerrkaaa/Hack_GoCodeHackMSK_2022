import os

from bot.bot_runner import bot
from Files import work_with_files
import pptx


async def save_pptx(result_array):
    pptx_path = work_with_files.get_full_path('PowerPoint\\pptx_template.pptx')

    presentation = pptx.Presentation(pptx_path)
    for layout in presentation.slides:
        for e in layout.shapes:
            for result_element in result_array:
                if result_element['content_type'] == 'image':
                    if e.text == result_element['field_name']:
                        # await bot.
                        # image_path = work_with_files.get_full_path('Files\\tempimages\\' + result_element['content'] + '.jpg')
                        # # image_info = await bot.get_file(result_element['content'])
                        # image = await bot.download_file(result_element['content'])
                        # with open(image_path, 'wb') as new_file:
                        #     new_file.write(image)
                        layout.shapes.add_picture(result_element['content'], e.left, e.top, e.width, e.height)

                        e.element.getparent().remove(e.element)
                        os.remove(result_element['content'])
    presentation.save('out.pptx')

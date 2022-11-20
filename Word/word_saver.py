from docxtpl import DocxTemplate, InlineImage
from Files import work_with_files
from docx.shared import Mm


async def save_word(result_array, file_name):
    word_path_input = work_with_files.get_full_path('Word\\word_template.docx')
    word_path_output = file_name + '.docx'

    tpl = DocxTemplate(word_path_input)

    render_dict = {}
    for result_element in result_array:

        if result_element['content_type'] == 'text':
            render_dict[result_element['field_name'].replace('{{', '').replace('}}', '')] = result_element['content']
        elif result_element['content_type'] == 'image':
            if result_element['content'] != '-':
                render_dict[result_element['field_name']] = InlineImage(
                    tpl, image_descriptor=result_element['content'], width=Mm(150))
    tpl.render(render_dict)
    tpl.save(word_path_output)

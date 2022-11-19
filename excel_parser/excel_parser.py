import openpyxl


def get_json_from_excel(path) -> list:
    workbook = openpyxl.load_workbook(path)
    wb = workbook[workbook.sheetnames[0]]

    output = []
    for line in range(2, len(wb['A']) + 1):
        output.append({
            "text": wb[f'A{line}'].value,
            "field_name": wb[f'B{line}'].value,
            "answer_type": wb[f'C{line}'].value
        })
    return output

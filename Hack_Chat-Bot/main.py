import pathlib

from docx import Document
from pathlib import Path


class Memo:

    def __init__(self):
        self.tags = ['1tag', '2tag', '3tag', '4tag', '5tag',
                     '6tag', '7tag', '8tag', '9tag', '10tag',
                     '11tag', '12tag', '13tag']

        # self.temp_path = ['Summary_temp.docx', 'Market_temp.docx', 'Plans_temp.docx', 'Product_temp.docx',
        #                   'Team_temp.docx', 'Terms_temp.docx', 'Traction_temp.docx', 'Contact_temp.docx']

    # шаблоны
    def get_paras(self, path):
        self.document = Document(path)
        self.paras = self.document.paragraphs

    # создание части меморандума
    def part_build(self, text_answers, name_temp):
        self.get_paras(Path(pathlib.Path.cwd(), 'templates', name_temp))
        for para in self.paras:
            for i in range(len(self.tags)):  # берем параграф, ищем в нем теги
                if para.text.find(self.tags[i]) != -1:
                    para.text = para.text.replace(self.tags[i], text_answers[i])  # меняем соответсвующий тег
        self.document.save(name_temp.split('_')[0] + '.docx')


# sum = ['Васян INC', 'авто', 'компания была основана в июле 2003 года Мартином Эберхардом и Марком '
#                             'Тарпеннингом, но нынешнее руководство компании называет сооснователями Илона '
#                             'Маска, Джеффри Брайана Страубела и Иэна Райта. В 2019 году Tesla стала '
#                             'крупнейшим производителем электромобилей в мире.', 'Электро бритвы, нет авто',
#        'уникальна ну', 'Американия', 'много кто', 'Армерика, Русь, и еще там',
#        'что-то делаем', 'Хакатон взяли за 3 рубля', 'ГазпромНефть', 'Запустили в космос',
#        'До сих пор летит']
# pr = [sum[3], 'Для Глока жизнь без трэкшн-контроля стала нормой после того, как он провел несколько сезонов в Champ '
#               'Car и GP2, научившись пилотировать мощные машины без зоны безопасности в виде электронных средств '
#               'помощи',
#       'Это ключевое место всей бизнес-модели. Нужно описать сегменты целевой аудитории, '
#       'то есть людей, которые будут покупать ваши товары или услуги. Важно понять, '
#       'кто ваши клиенты, какие качества продукта для них важны, сколько они готовы платить и за '
#       'что.', 'фото']
trm = ['1234', '165', '2890', '10', 'цель цель цель цель цель цель цель цель цель цель цель ']

test = Memo()

test.part_build(trm, 'Terms_temp.docx')

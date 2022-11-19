import pathlib

from docx import Document
from pathlib import Path


class Memo:

    def __init__(self):
        self.summary_tags = ['comp_name', 'work_with', 'comp_short_story', 'comp_product',
                             'product_uniq', 'product_local', 'product_rivalry', 'product_market',
                             'comp_cases', 'comp_ accel', 'comp_ invest', 'comp_pilot',
                             'pilot_result']
        self.product_tags = ['comp_product', 'traction_pilot', 'business_model', 'product_photo']

    # шаблоны
    def get_paras(self, path):
        self.document = Document(path)
        self.paras = self.document.paragraphs

    # создание саммари
    def summary_build(self, summary):
        self.get_paras(Path(pathlib.Path.cwd(), 'templates', 'Summary_temp.docx'))
        for para in self.paras:
            for i in range(len(self.summary_tags)):  # берем параграф, ищем в нем теги
                if para.text.find(self.summary_tags[i]) != -1:
                    para.text = para.text.replace(self.summary_tags[i], summary[i])  # меняем соответсвующий тег

        self.document.save('Summary.docx')

    # создание описания продукта
    def product_build(self, product):
        self.get_paras(Path(pathlib.Path.cwd(), 'templates', 'Product_temp.docx'))
        for para in self.paras:
            for i in range(len(self.product_tags)):
                if para.text.find(self.product_tags[i]) != -1:
                    para.text = para.text.replace(self.product_tags[i], product[i])
        self.document.save('Product.docx')

    # создание описания рынка
    def market_build(self):
        pass

    # создание описания результатов
    def results_build(self):
        pass

    # создание информации о команде
    def team_build(self):
        pass

    # создание описания планов
    def plans_build(self):
        pass

    # создание описания по условиям сделки
    def terms_build(self):
        pass

def main():
    sum = ['Васян INC', 'авто', 'компания была основана в июле 2003 года Мартином Эберхардом и Марком '
                                'Тарпеннингом, но нынешнее руководство компании называет сооснователями Илона '
                                'Маска, Джеффри Брайана Страубела и Иэна Райта. В 2019 году Tesla стала '
                                'крупнейшим производителем электромобилей в мире.', 'Электро бритвы, нет авто',
           'уникальна ну', 'Американия', 'много кто', 'Армерика, Русь, и еще там',
           'что-то делаем', 'Хакатон взяли за 3 рубля', 'ГазпромНефть', 'Запустили в космос',
           'До сих пор летит']
    pr = [sum[3], 'Для Глока жизнь без трэкшн-контроля стала нормой после того, как он провел несколько сезонов в Champ '
                  'Car и GP2, научившись пилотировать мощные машины без зоны безопасности в виде электронных средств '
                  'помощи',
          'Это ключевое место всей бизнес-модели. Нужно описать сегменты целевой аудитории, '
          'то есть людей, которые будут покупать ваши товары или услуги. Важно понять, '
          'кто ваши клиенты, какие качества продукта для них важны, сколько они готовы платить и за '
          'что.', 'фото']

    test = Memo()
    # test.summary_build(sum)
    test.product_build(pr)

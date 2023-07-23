from hhparser import HHParser
from dbcreator import DBCreator
from dbmanager import DBManager


def choose_one(choose_dict):
    """Возвращает выбор пользователя из предложенных в словаре {1: 'вариант-1', 2: 'вариант-2',..}"""
    while True:
        print(", ".join((" - ".join((str(n), q)) for n, q in choose_dict.items())))
        position = input()
        if not position.isdigit() or int(position) < min(choose_dict) or int(position) > max(choose_dict):
            print('должен быть введён номер из предложенных')
            continue
        else:
            return int(position)

def mine():
    hhparser = HHParser()
    dbcreator = DBCreator()

    print('Хотите создать базу данных и наполнить её вакансиями?')
    if choose_one({0: 'использовать имеющуюся', 1: 'создать и наполнить'}):
        print('ждите выполнения запросов к НН примерно 3 минуты')
        dbcreator.create_database()
        dbcreator.write_employers(employers)
        for employer in employers:
            data = hhparser.get_vacancies(employer[0])
            if data:
                dbcreator.write_vacancies(data)

"""Список работодателей и их ID на НН"""
employers = [(4934, 'билайн'),
             (3776, 'ПАО "МТС"'),
             (2748, 'ПАО "Ростелеком"'),
             (3529, 'Сбер для экспертов'),
             (78638, 'Тинькофф'),
             (4181, 'ПАО "ВТБ" Розничный бизнес'),
             (3809, 'Сибур'),
             (1740, 'Яндекс'),
             (577743, 'Росатом'),
             (39305, 'ПАО "Газпромнефть"')]

if __name__ == '__main__':
    mine()


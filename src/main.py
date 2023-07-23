from hhparser import HHParser
from dbcreator import DBCreator
from dbmanager import DBManager
import pprint


def choose_one(choose_dict):
    """Возвращает выбор пользователя из предложенных в словаре {1: 'вариант-1', 2: 'вариант-2',..}"""
    while True:
        print("\n".join((" - ".join((str(n), q)) for n, q in choose_dict.items())))
        position = input()
        if not position.isdigit() or int(position) < min(choose_dict) or int(position) > max(choose_dict):
            print('должен быть введён номер из предложенных')
            continue
        else:
            return int(position)

def mine():
    hhparser = HHParser()
    dbcreator = DBCreator()
    dbmanager = DBManager()
    while True:
        print('Хотите создать базу данных и наполнить её вакансиями?')
        if choose_one({0: 'использовать имеющуюся', 1: 'создать и наполнить'}):
            print('ждите выполнения запросов к НН примерно 3 минуты')
            dbcreator.create_database()
            dbcreator.write_employers(employers)
            for employer in employers:
                data = hhparser.get_vacancies(employer[0])
                if data:
                    dbcreator.write_vacancies(data)

        print('Что хотите сделать дальше:')
        choose = choose_one({0: 'Выйти из программы',
                       1: 'Получить список всех компаний и количество вакансий у каждой компании',
                       2: 'Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию',
                       3: 'Получить среднюю зарплату по вакансиям',
                       4: 'Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям',
                       5: 'Получить список всех вакансий, в названии которых содержатся переданные в метод слова (списком), например “python”'})
        if not choose:
            quit()
        elif choose == 1:
            pprint.pprint(dbmanager.get_companies_and_vacancies_count())
        elif choose == 2:
            pprint.pprint(dbmanager.get_all_vacancies())
        elif choose == 3:
            pprint.pprint(dbmanager.get_avg_salary())
        elif choose == 4:
            pprint.pprint(dbmanager.get_vacancies_with_higher_salary())
        elif choose == 5:
            keyword = input('Введите ключевые слова: ')
            pprint.pprint(dbmanager.get_vacancies_with_keyword(keyword.lower().strip().split()))


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


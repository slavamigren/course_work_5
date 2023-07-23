import requests
from requests.exceptions import HTTPError
import time
from dotenv import load_dotenv
import os
import pprint


class HHParser:
    """Класс для парсинга HH"""

    def __init__(self):
        self.vacancies_method = 'https://api.hh.ru/vacancies'

    def get_vacancies(self, employer_id):
        """
        Формирует список словарей со всеми доступными вакансиями по конкретному работодателю,
        на вход принимает только id работодателя на НН
        """
        vacancies = []
        page = 0
        while True:
            params = {
                'employer_id': employer_id,
                'page': page,  # Индекс страницы поиска на HH
                'per_page': 100  # Максимальное кол-во вакансий на 1 странице
            }
            try:
                response = requests.get(self.vacancies_method, params=params)
            except requests.exceptions.HTTPError as err:
                print(f'Соединение с HH недоступно, ошибка: {err}')

            for vacancy in response.json()['items']:
                vacancy_tuple = (employer_id,
                                 vacancy['area']['name'],
                                 vacancy['name'],
                                 int(vacancy['salary']['from']) if vacancy['salary'] is not None and vacancy['salary']['from'] is not None else None,
                                 int(vacancy['salary']['to']) if vacancy['salary'] is not None and vacancy['salary']['to'] is not None else None,
                                 vacancy['snippet']['requirement'],
                                 vacancy['snippet']['responsibility'],
                                 vacancy['alternate_url'])
                vacancies.append(vacancy_tuple)
            page += 1
            if page >= response.json()['pages']:
                break
            time.sleep(0.1)
        return vacancies



if __name__ == '__main__':
    a = HHParser()
    l = a.get_vacancies(3776)
    #pprint.pprint(l)
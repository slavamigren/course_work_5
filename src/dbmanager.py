from dotenv import load_dotenv
import os
import psycopg2
import pprint


class DBManager:
    """Класс для запросов к бд с работодателями"""

    def __init__(self):
        load_dotenv()
        self.db_params =dict(host=os.getenv("host"),
                             database=os.getenv("database"),
                             user=os.getenv("user"),
                             password=os.getenv("password"))

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        conn = psycopg2.connect(**self.db_params)

        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT employers.employer_name, COUNT(*) "
                                   "FROM vacancies "
                                   "JOIN employers USING(employer_id) "
                                   "GROUP BY employers.employer_name")
                    result = cursor.fetchall()
        finally:
            conn.close()
        return result

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        conn = psycopg2.connect(**self.db_params)

        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT employers.employer_name, "
                                   "vacancies.vacancy_name, "
                                   "vacancies.salary_from, "
                                   "vacancies.salary_to, "
                                   "vacancies.url "
                                   "FROM vacancies "
                                   "JOIN employers USING(employer_id)")
                    result = cursor.fetchall()
        finally:
            conn.close()
        return result

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        conn = psycopg2.connect(**self.db_params)

        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT AVG(vacancies.salary_from) "
                                   "FROM vacancies "
                                   "WHERE vacancies.salary_from IS NOT NULL")
                    result = cursor.fetchone()
        finally:
            conn.close()
        return int(result[0])

    def get_vacancies_with_higher_salary(self):
        """
         Получает список всех вакансий, у которых зарплата
         выше средней по всем вакансиям.
        """
        conn = psycopg2.connect(**self.db_params)

        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("""SELECT employers.employer_name,
                                      vacancies.vacancy_name,
                                      vacancies.salary_from,
                                      vacancies.salary_to,
                                      vacancies.url
                                      FROM vacancies JOIN employers USING(employer_id)
                                      WHERE vacancies.salary_from IS NOT NULL
                                      AND vacancies.salary_from > (SELECT AVG(vacancies.salary_from)
                                                                   FROM vacancies
                                                                   WHERE vacancies.salary_from IS NOT NULL)""")
                    result = cursor.fetchall()
        finally:
            conn.close()
        return result

    def get_vacancies_with_keyword(self, words):
        '''
         Получает список всех вакансий, в названии которых
         содержатся переданные в метод слова (списком), например “python”.
        '''
        like = "%' OR vacancies.vacancy_name LIKE'%".join(words)
        conn = psycopg2.connect(**self.db_params)
        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"""SELECT employers.employer_name, 
                                      vacancies.vacancy_name,
                                      vacancies.salary_from,
                                      vacancies.salary_to,
                                      vacancies.url
                                      FROM vacancies
                                      JOIN employers USING(employer_id)
                                      WHERE vacancies.vacancy_name LIKE '%{like}%'""")
                    result = cursor.fetchall()
        finally:
            conn.close()
        return result


if __name__ == '__main__':
    a = DBManager()
    pprint.pprint(a.get_vacancies_with_keyword('продавец'.split()))
from dotenv import load_dotenv
import os
import psycopg2


class DBCreator:
    """Класс для запросов к бд с работодателями"""

    def __init__(self):
        load_dotenv()
        self.db_params =dict(host=os.getenv("host"),
                             database=os.getenv("database"),
                             user=os.getenv("user"),
                             password=os.getenv("password"))

    def write_vacancies(self, vacancies):
        """Обновляет вакансии в базе данных по конкретной компании"""
        conn = psycopg2.connect(**self.db_params)

        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM vacancies WHERE employer_id = %s", (vacancies[0][0],))
                    cursor.executemany("INSERT INTO vacancies "
                                       "(employer_id, "
                                       "city, "
                                       "vacancy_name, "
                                       "salary_from, "
                                       "salary_to, "
                                       "requirement, "
                                       "responsibility, "
                                       "url) "
                                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", vacancies)
        finally:
            conn.close()

    def write_employers(self, employers):
        """Записывает работодателей в базу данных"""
        conn = psycopg2.connect(**self.db_params)

        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("TRUNCATE TABLE employers")
                    cursor.executemany("INSERT INTO employers VALUES (%s, %s)", employers)
        finally:
            conn.close()

    def create_database(self):
        """Создаёт базу данных"""
        conn = psycopg2.connect(host=self.db_params["host"],
                                database='postgres',
                                user=self.db_params["user"],
                                password=self.db_params["password"])
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(f"""SELECT pg_terminate_backend(pg_stat_activity.pid)
                           FROM pg_stat_activity
                           WHERE pg_stat_activity.datname = \'{self.db_params['database']}\'
                           AND pid <> pg_backend_pid();""")
        cursor.execute(f"DROP DATABASE IF EXISTS {self.db_params['database']}")
        cursor.execute(f"CREATE DATABASE {self.db_params['database']}")
        cursor.close()
        conn.close()

        conn = psycopg2.connect(**self.db_params)
        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"CREATE TABLE employers "
                                   f"(employer_id int PRIMARY KEY, "
                                   f"employer_name varchar(100) NOT NULL)")
                    cursor.execute(f"CREATE TABLE vacancies "
                                   f"(vacancy_id serial PRIMARY KEY, "
                                   f"employer_id int NOT NULL, "
                                   f"city varchar(100), "
                                   f"vacancy_name text, "
                                   f"salary_from int, "
                                   f"salary_to int, "
                                   f"requirement text, "
                                   f"responsibility text, "
                                   f"url text);")

        finally:
            conn.close()

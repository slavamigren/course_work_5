--Создать базу данных и таблицы для хранения вакансий
CREATE DATABASE vacancies_db;

CREATE TABLE employers
(
employer_id int PRIMARY KEY,
employer_name varchar(100) NOT NULL
);

CREATE TABLE vacancies
(
vacancy_id serial PRIMARY KEY,
employer_id int NOT NULL,
city varchar(100),
vacancy_name text,
salary_from int,
salary_to int,
requirement text,
responsibility text,
url text
);


--Получить список всех компаний и количество вакансий у каждой компании.
SELECT employers.employer_name, COUNT(*)
FROM vacancies
JOIN employers USING(employer_id)
GROUP BY employers.employer_name

--Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
SELECT employers.employer_name, vacancies.vacancy_name, vacancies.salary_from, vacancies.salary_to, vacancies.url
FROM vacancies
JOIN employers USING(employer_id)

--Получает среднюю зарплату по вакансиям.
SELECT AVG(vacancies.salary_from)
FROM vacancies
WHERE vacancies.salary_from IS NOT NULL


--Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
SELECT employers.employer_name, vacancies.vacancy_name, vacancies.url
FROM vacancies
JOIN employers USING(employer_id)
WHERE vacancies.salary_from IS NOT NULL AND vacancies.salary_from > (SELECT AVG(vacancies.salary_from) FROM vacancies WHERE vacancies.salary_from IS NOT NULL)

-- получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”
SELECT employers.employer_name, vacancies.vacancy_name, vacancies.url
FROM vacancies
JOIN employers USING(employer_id)
WHERE vacancies.vacancy_name LIKE '%python%' OR vacancies.vacancy_name LIKE '%аналитик%'
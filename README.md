# Курсовая работа №5
  
***
Программа предлагает простой интерфейс для сбора и элементарной аналитики всех 
доступных вакансий по 10 компаниям (список кортежей в main.py, куда необходимо 
занести id и название компании с hh.ru)

***
## Назначение модулей и файлов:

- queries.sql - перечислены запросы sql, использованные в проекте (просто для
ознакомления)
- hhparser.py - реализует классы с одним методом (не считая __init__) для
скачивания по API с НН вакансии указанного id работодателя
- dbcreator.py - реализует методы для создания базы данных и заполнения её
данными с HH (заполняются две таблицы с работодателями и вакансиями)
- dbmanager.py - реализует методы по простой аналитике данных из базы
  (подробнее смотрите комментарии в модуле)
- main.py - просто демонстрирует работу модулей в простейшем цикле работы
с пользователем. Смело запускайте (если у Вас установлена postgres и вы создали файл .env
с параметрами подключения:
#postgresql
host=localhost
database=vacancies_db
user=postgres
password=...).

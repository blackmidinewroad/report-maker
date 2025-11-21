# Report Maker
Скрипт читает CSV-файлы с данными о закрытых задачах сотрудников, формирует отчеты и выводит их в консоли.


## Установка и запуск
1. **Создайте локальную копию репозитория**:
   ```shell
   git clone https://github.com/blackmidinewroad/report-maker.git
   cd report-maker
   ```

2. **Установите необходимые зависимости**
      ```shell
      pip install -r requirements.txt
      ```

3. **Запустите скрипт**:
   ```shell
    python main.py --files <paths/to/empl/files> --report <report_name>
   ```
   Используйте `python3` на macOS.

   - Замените `paths/to/empl/files` на реальные пути к файлам (разделенные пробелами) с данными о закрытых задачах (например, если файлы в корне проекта: `employees1.csv employees2.csv`; или используя полные пути: `C:\Users\JohnDoe\Downloads\employees1.csv C:\Users\JohnDoe\Downloads\employees2.csv`)   
   - Замените `report_name` на реальное название отчета (например, `performance`)


## Пример запуска скрипта
![Run Example](screenshots/run_example.png)


## Запуск тестов
   ```shell
    python -m pytest
   ```


## Доступные отчеты
   - `performance` - средняя эффективность сотрудников по должностям.


## Добавление новых отчетов
1. **Создайте функцию, которая будет производить вычисления**

    Сигнатура функции:
   ```python
   def calc_new_report(employees_data: list[dict]) -> dict[str, float | int]:
       ... 
   ```

2. **Добавьте ее в список отчетов `REPORTS` в `main.py`**:
   ```python
    REPORTS = {
        'performance': calc_performance,
        'new_report': calc_new_report,
    }
   ```

3. **Используйте параметры вывода отчета (если требуется)**

    При вызове `display_report` в `main()` можно указать:
    - `grouping_col_name` - для чего производились расчеты (например: `position`, `skill`)
    - `is_sorted` - нужно ли сортировать результаты в отчете
    - `is_reverse_sort` - обратная ли сортировка

4. **Запуск скрипта**:
   ```shell
    python main.py --files employees1.csv employees2.csv --report new_report
   ```


## Пример содержимого CSV-файла
   ```csv
    name,position,completed_tasks,performance,skills,team,experience_years
    Alex Ivanov,Backend Developer,45,4.8,"Python, Django, PostgreSQL, Docker",API Team,5
    Maria Petrova,Frontend Developer,38,4.7,"React, TypeScript, Redux, CSS",Web Team,4
    John Smith,Data Scientist,29,4.6,"Python, ML, SQL, Pandas",AI Team,3
    Anna Lee,DevOps Engineer,52,4.9,"AWS, Kubernetes, Terraform, Ansible",Infrastructure Team,6
    Mike Brown,QA Engineer,41,4.5,"Selenium, Jest, Cypress, Postman",Testing Team,4
   ```
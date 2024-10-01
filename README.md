### Запуск проекта в dev-режиме:
### 1) Клонировать репозиторий на свой компьютер:
#### <command>
    git clone https://gitlab.crja72.ru/django/2024/autumn/course/students/261067-almasvildanoff-course-1187
#### </command>

### 2) Создать виртуальное окружение:

#### <command>
    python -m venv venv 
#### </command>

### 3) Запустить виртуальное окружение:

#### На Windows:
#### <command>
    venv\Scripts\activate
#### </command>

#### На Linux:
#### <command>
    source venv/bin/activate
#### </command>

### 4) Установка зависимостей:

#### Основные:
#### <command>
    pip install -r requirements/prod.txt
#### </command>

#### Для тестов:
#### <command>
    pip install -r requirements/test.txt
#### </command>

#### Для разработки:
#### <command>
    pip install -r requirements/dev.txt
#### </command>

### 5) Переход к папке lyceum:
#### <command>
    cd lyceum
#### </command>

### 6) Запуск проекта:
#### <command>
    python manage.py runserver
#### </command>

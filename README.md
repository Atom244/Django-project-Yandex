### Запуск проекта в dev-режиме:

- ### Клонировать репозиторий на свой компьютер:

#### <command>

    git clone https://gitlab.crja72.ru/django/2024/autumn/course/students/261067-almasvildanoff-course-1187

#### </command>

- ### Создать виртуальное окружение:

#### <command>

    python -m venv venv

#### </command>

- ### Запустить виртуальное окружение:

#### На Windows:

#### <command>

    venv\Scripts\activate

#### </command>

#### На Linux:

#### <command>

    source venv/bin/activate

#### </command>

- ### Установка зависимостей:

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

- ### Создание файла .env для хранения переменных окружения:

#### Создайте файл .env:

#### <command>

    touch .env

#### </command>

#### Запишите в файл Env секретный ключ ('SECRET_KEY'):

#### На Linux:
#### <command>

    cat <<EOF > .env
    SECRET_KEY = '<secret key>'
    ALLOWED_HOSTS = '<allowed hosts>'
    DEBUG = '<debug>'
    EOF

#### </command>

#### На Windows:
#### <command>

    echo SECRET_KEY = '^<secret key^>' >> .env
    echo ALLOWED_HOSTS = '^<allowed hosts^>' >> .env
    echo DEBUG = '^<debug^>' >> .env

#### </command>
- ### Переход к папке lyceum:

#### <command>

    cd lyceum

#### </command>

- ### Запуск проекта:

#### <command>

    python manage.py runserver

#### </command>

![pipeline status](https://gitlab.crja72.ru/django/2024/autumn/course/students/261067-almasvildanoff-course-1187/badges/master/pipeline.svg)

![pipeline status](https://gitlab.crja72.ru/django/2024/autumn/course/students/261067-almasvildanoff-course-1187/badges/main/pipeline.svg)

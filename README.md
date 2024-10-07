![pipeline status](https://gitlab.crja72.ru/django/2024/autumn/course/students/261067-almasvildanoff-course-1187/badges/main/pipeline.svg)

### Запуск проекта в dev-режиме:

- ### Клонирование репозитория на свой компьютер:

#### <command>

    git clone https://gitlab.crja72.ru/django/2024/autumn/course/students/261067-almasvildanoff-course-1187

#### </command>

- ### Создание виртуального окружения:

#### <command>

    python -m venv venv

#### </command>

- ### Запуск виртуального окружения:

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

#### Создайте файл **.env**:

#### На Linux:

#### <command>

    touch .env

#### </command>

#### На Windows:

#### <command>

    echo. > .env

#### </command>

#### Запишите в файл Env следующие данные:

#### На Linux:

#### <command>

    cat <<EOF > .env
    DJANGO_SECRET_KEY = '<secret key>'
    DJANGO_ALLOWED_HOSTS = '<allowed hosts>'
    DJANGO_DEBUG = '<bool>'
    DJANGO_ALLOW_REVERSE = '<bool>'
    EOF

#### </command>

#### На Windows:

#### <command>

    echo DJANGO_SECRET_KEY = '^<secret key^>' >> .env
    echo DJANGO_ALLOWED_HOSTS = '^<allowed hosts^>' >> .env
    echo DJANGO_DEBUG = '^<bool^>' >> .env
    echo DJANGO_ALLOW_REVERSE = '^<bool^>' >> .env

#### </command>

###### Также вы могли скопировать данные для примера из **.env.example** в **.env**

- ### Переход к папке lyceum:

#### <command>

    cd lyceum

#### </command>

- ### Запуск проекта:

#### <command>

    python manage.py runserver

#### </command>

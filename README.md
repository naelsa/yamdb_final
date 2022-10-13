[![Django-app workflow](https://github.com/naelsa/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/naelsa/yamdb_final/actions/workflows/yamdb_workflow.yml)
## Проект YaMDb

### Описание:
Проект YaMDb собирает отзывы пользователей на произведения, если подробнее:
```
 - Писать отзыв к произведениям
 - Выставлять оценки произведениям
 - Находить интеоесующие произведения
 - Искать произведения по категориям и жанрам
 ```

### Технологии:
При реализации проекта были использованы следующие основные технологии, фреймворки и библиотеки:

```
Python 3.8
Django 2.2.16
Django Rest FrameWork 3.12.4
REST API
```
___

### Как запустить проект:

<details>
  <summary markdown="span">Нажми, чтобы увидеть инструкцию</summary>
 
 -------

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:naelsa/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Импортировать данные:

```
python3 manage.py loaddata fixtures.json
```

Запустить проект:

```
python3 manage.py runserver
```

</details>

_____

<details>
  <summary markdown="span">Запуск проекта в Docker-контейнере</summary>
 
 ------

Заполнить переменные окружения в `.env`
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
 
```

Запустить `docker-compose` командой:

```
docker-compose up -d --build

```

Собрать статику и выполнить миграции, создать суперпользователя:

```
docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input

```

Импортировать тестовые данные:

```
docker-compose exec web python manage.py loaddata fixtures.json
```
  
</details>


_____

<details>
  <summary markdown="span">Api-документация</summary>
 
 ------

```
http://localhost/redoc/
 
```

  
</details>


### Автор:
- [Хасбутдинов Наил](https://github.com/naelsa)
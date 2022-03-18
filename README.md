# PostIt
## Блог-платформа

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Небольшая социальная сеть где вы можете постить записи и создавать группы

## Возможности

- Создание пользоавтеля
- Создание постов с картинками 
- Комментирование постов других пользователей и подписывание на них
- Просмотр постов других авторов
- Редактирование постов и создание групп

## Технологии
- Phyton 3.7

## Запуск проекта

Все необходимые зависимости указаны в файле requirements.txt

Установка зависимостей и запуск сервера

```sh
install requirements.txt
pip install -r requirements.txt
```

После установки зависимостей и инициализации вы должны сделать миграции (не забудьте активировать виртуальное окружение)

```sh
python manage.py makemigrations
python manage.py migrate
```

Создание администратора для доступа к панели администрирования 

```sh
python manage.py createsuperuser
```

Запуск сервера

```sh
python manage.py runserver
```





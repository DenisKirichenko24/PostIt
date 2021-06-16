Сайт с системой публикации блогов пользователей с возможностью создания постов с загрузкой фотографией. Добавлена возможность комментировать, подписываться на авторов. Это будет сайт, на котором можно создать свою страницу. Если на нее зайти, то можно посмотреть все записи автора. Пользователи смогут заходить на чужие страницы, подписываться на авторов и комментировать их записи. Есть возможность модерировать записи. Также можно создавать сообщества и публиковать записи в сообществах

Стек технологий
Python 3 Django 3.7

Технические требования
Все необходимые пакеты перечислены в requirements.txt
Запуск приложения
Установите зависимости из requirements.txt:
pip install -r requirements.txt
После того как все зависимости установятся и завершат свою инициализацию, примените все необходимые миграции:
python manage.py makemigrations
python manage.py migrate
Для доступа к панели администратора создайте администратора:
python manage.py createsuperuser
Запустите приложение:
python manage.py runserver

[![CI](https://github.com/yandex-praktikum/hw05_final/actions/workflows/python-app.yml/badge.svg?branch=master)](https://github.com/yandex-praktikum/hw05_final/actions/workflows/python-app.yml)

# VideoService
### Описание:
**Проект VideoService** — это REST API для хранения, просмотра и управления видео-контентом.

### Технологии:
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)


## Поднятие контейнера БД PostgreSQL в Docker
1. Клонируйте репозиторий и перейдите в него в командной строке.
2. Создайте и активируйте виртуальное окружение, установите зависимости:
```bash
git clone https://github.com/Seniacat/Foodgram.git
cd video_service
python -m venv venv
source venv/Script/activate
python -m pip install --upgrade pip
cd video_service
pip install -r requirements.txt
```
3. Cоздать и открыть файл .env с переменными окружения:
```bash
touch .env
```
*Пример содержимого файла .env находится в корне проекта в файле .env.example.*

4. Из корневой директории проекта выполнить команду:
```bash
docker compose -f docker-compose.yml up -d
```
5. Выполнить миграции из директории video_service:
```bash
python manage.py migrate
```
6. Запустить сервер:
```bash
python manage.py runserver
```
## Дополнительно:
- Эндпоинты API доступны по адресу:
```
http://127.0.0.1:8000/api/docs/
```
- Создать суперпользователя можно командой:
```bash
python manage.py createsuperuser
```
- Доступны кастомные скрипты для создания и удаления данных БД:
```bash
python manage.py upload_test_file
python manage.py delete_test_file
```

### Автор
- [Горьковой Егор](https://github.com/EgorGorkovoj)
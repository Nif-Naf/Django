## Главный проект по Django.

### Как запустить.
1) Установка Docker(если почему-то не установлен).
2) Собрать а потом запустить проект командой: docker-compose up --build
3) Опционально. Для доступа в административную панель создать суперпользователя.
4) Перейти по адресу: http://localhost:8000/

### Краткое описание приложений.
## Файловое хранилище.
Приложение может сохранять любые файлы(пока все виды файлов не проверены).
Доступно два действия:
- Загрузка файлов в файловое хранилище(которое тоже локальное). По адресу: http://localhost:8000/api/v1/storage/upload/
- Получение информации по всем файлам в файловом хранилище. По адресу:  http://localhost:8000/api/v1/storage/files/

### Полезные команды.
Работа с проектом.
``` commandline
docker-compose run --rm django python manage.py makemigrations storage
docker-compose run --rm django python manage.py migrate
docker-compose run --rm django python manage.py createsuperuser
```
Разработка.
``` commandline
docker-compose run --rm django python manage.py startapp name_of_app
```
Отладка контейнеров.
``` commandline
docker-compose exec container_name bash
docker inspect container_name
```
Запуск тестов.
``` commandline
docker-compose exec django python manage.py test apps.storage
docker-compose exec django python manage.py test apps.storage.tests.test_stability
```

### Что еще предстоит сделать?
- Настроить: flake-8, pre-commit.
- До настроить healthchecker в docker-compose.

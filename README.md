# API YaMDb c применением CI и CD

[![](https://github.com/TutunkinVladislav/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/TutunkinVladislav/yamdb_final/actions/runs/4963003220)

Проект API YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Для приложения настроен Continuous Integration (CI) и Continuous Deployment (CD).

Реализован:
* автоматический запуск тестов;
* обновление образов на DockerHub;
* автоматический деплой на боевой сервер при push-е в главную ветку main.

### Стек:
- Python 3.7
- Django 3.2
- Gunicorn 20.0.4
- Nginx 1.21.3
- Postgres 13.0
- Docker 20.10.24

### Шаблон наполнения env-файла
```
DB_NAME='postgres' # имя базы данных
POSTGRES_USER='postgres' # логин для подключения к базе данных
POSTGRES_PASSWORD='postgres' # пароль для подключения к БД
DB_HOST='db' # название сервиса (контейнера)
DB_PORT='5432' # порт для подключения к БД
```

### Запуск проекта
Клонируем репозиторий и создаём файл `.env` в папке infra.

#### Настройка workflow
Для использования Continuous Integration (CI) и Continuous Deployment (CD): в
репозитории GitHub нужно перейти `Settings/Secrets and variables/Actions` прописать Secrets -
переменные окружения для доступа к сервисам:
```
DB_ENGINE - django.db.backends.postgresql
DB_NAME - postgres (имя БД)
POSTGRES_USER - postgres (логин для подключения к БД)
POSTGRES_PASSWORD - (пароль для подключения к БД)
DB_HOST - db (название контейнера)
DB_PORT - 5432 (порт для подключения к БД)
HOST - (имя или IP хоста/домена)
DOCKER_USERNAME - (имя пользователя в DockerHub)
DOCKER_PASSWORD  - (пароль пользователя в DockerHub)
USER - (имя пользователя "Виртуальной машины" в Yandex Cloud)
SSH_KEY - (приватный ssh-ключ "cat ~/.ssh/id_rsa")
PASSPHRASE - (пароль для ssh-ключа)
TELEGRAM_TO - (id аккаунт в Telegram)
TELEGRAM_TOKEN  - (токен бота)
```
При push в ветку main автоматически отрабатывают сценарии:
* *tests* - проверка кода на соответствие стандарту PEP8 и запуск pytest.
* *build_and_push_to_docker_hub* - сборка и доставка докер-образов на DockerHub
* *deploy* - автоматический деплой проекта на боевой сервер. Выполняется
копирование файлов из DockerHub на сервер;
* *send_message* - отправка уведомления в Telegram.


#### Подготовка удалённого сервера
* Войти на удалённый сервер:
```
ssh <username>@<ip_address>
```
* Остановить службу `nginx`:
```
sudo systemctl stop nginx
```
* Установить Docker и Docker-compose:
```
sudo apt update
sudo apt upgrade -y
sudo apt install docker.io
sudo apt install docker-compose -y
```
* Проверить корректность установки Docker-compose:
```
sudo docker-compose --version
```
* На сервере создать директорию `nginx`:
```
mkdir nginx
```
* Скопировать файлы `docker-compose.yaml` и
`nginx/default.conf` из проекта (локально) на сервер в
`home/<username>/docker-compose.yaml` и
`home/<username>/nginx/default.conf` соответственно:
  * перейти в директорию с файлом `docker-compose.yaml` и выполните:
  ```
  scp docker-compose.yaml <username>@<ip_address>:/home/<username>/
  ```
  * перейти в директорию с файлом `default.conf` и выполните:
  ```
  scp default.conf <username>@<ip_address>:/home/<username>/nginx/
  ```

#### После успешного деплоя
* Создать суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```
* Для проверки работоспособности приложения, перейти на страницу:
```
http:/84.201.139.210/admin/
```

#### Документация для YaMDb доступна по адресу:
```
http:/84.201.139.210/redoc/
```

### Автор проекта:
[Владислав Тутункин](https://github.com/TutunkinVladislav)

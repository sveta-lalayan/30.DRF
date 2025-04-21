
# 30.DRF
Описание проекта

Это проект на Django REST Framework (DRF), развернутый на виртуальной машине с IP 10.130.0.12 с использованием Docker Compose.

Требования

Docker Engine (v20.10+)
Docker Compose (v2.0+)
Git
Установка

Клонирование репозитория:
git clone https://github.com/ваш-логин/30.drf.git && cd 30.drf
Настройка переменных окружения:
cp .env.example .env
Затем отредактируйте файл .env:
DEBUG=0
SECRET_KEY=ваш-секретный-ключ
POSTGRES_USER=пользователь_бд
POSTGRES_PASSWORD=пароль_бд
POSTGRES_DB=drf_db
Запуск с Docker Compose

Запуск всех сервисов: docker-compose up -d --build

Состав сервисов:

web: Django-приложение (порт 8000)
db: База данных PostgreSQL
redis: Кэш Redis
Проверка работы

Проверить контейнеры: docker-compose ps
Протестировать API: curl http://10.130.0.12:8000/api/healthcheck/
Проверить БД: docker-compose exec db psql -U $POSTGRES_USER -d $POSTGRES_DB -c "\dt"
Управление

Миграции: docker-compose exec web python manage.py migrate
Суперпользователь: docker-compose exec web python manage.py createsuperuser
Статика: docker-compose exec web python manage.py collectstatic --no-input
Обслуживание

Остановка: docker-compose down
Логи: docker-compose logs -f web
Бэкап БД: docker-compose exec db pg_dump -U $POSTGRES_USER $POSTGRES_DB > backup.sql
Восстановление: docker-compose exec -T db psql -U $POSTGRES_USER -d $POSTGRES_DB < backup.sql
Решение проблем

Если порт 8000 занят: sudo lsof -i :8000 и kill -9 <PID>
Проблемы с БД: docker-compose down -v && docker-compose up -d
Очистка Docker: docker system prune -a --volumes

Структура проекта

Основные файлы:

docker-compose.yml
Dockerfile
.env.example

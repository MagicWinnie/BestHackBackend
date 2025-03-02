# BestHack — Backend часть

Команда: True Legends

## Описание

В данном репозитории представлен backend маркетплейса для эффективной купли-продажи остатков топлива. Платформа решает проблему утилизации излишков топлива, помогая поставщикам реализовать остатки, а потребителям — приобрести топливо по выгодным ценам.

В системе используется современный стек технологий:

- Python является основным (и единственным) языком разработки
- FastAPI обеспечивает высокопроизводительный REST API с автоматической документацией (например, Swagger)
- MongoDB в сочетании с Beanie (ODM) предоставляет гибкую и масштабируемую схему данных
- Система безопасности включает JWT-аутентификацию, хэширование паролей и защиту от распространенных уязвимостей
- Асинхронная обработка запросов позволяет эффективно обрабатывать большое количество транзакций

Архитектура проекта построена с учетом возможности горизонтального масштабирования и простой интеграции с другими сервисами через API.

## Архитектура

Описание файлов в проекте:

```tree
.
├── certs/                # Сертификаты для JWT аутентификации
│   ├── jwt-private.pem   # Приватный ключ для подписи токенов
│   └── jwt-public.pem    # Публичный ключ для верификации токенов
├── src/
│   ├── api/              # API модули разделены по функциональным блокам
│   │   ├── auth/         # Аутентификация и авторизация
│   │   │   ├── dependencies.py  # Зависимости для DI
│   │   │   ├── routes.py        # Эндпоинты API
│   │   │   ├── schemas.py       # Pydantic-схемы для запросов/ответов
│   │   │   └── service.py       # Бизнес-логика
│   │   ├── lot/          # Управление лотами (остатками топлива)
│   │   ├── order/        # Управление заказами
│   │   └── user/         # Управление пользователями
│   ├── core/             # Ядро приложения
│   │   ├── auth/         # Компоненты аутентификации
│   │   │   ├── api_key.py           # Обработка API ключей
│   │   │   └── password_handler.py  # Хэширование паролей
│   │   ├── config.py     # Конфигурация приложения
│   │   ├── database.py   # Инициализация и управление MongoDB
│   │   ├── models/       # Модели данных для MongoDB (Beanie)
│   │   │   ├── blacklist_jwt.py # Модель для отозванных JWT
│   │   │   ├── lot.py           # Модель лота с топливом
│   │   │   ├── order.py         # Модель заказа
│   │   │   └── user.py          # Модель пользователя
│   │   └── repositories/ # Слой доступа к данным
│   │       ├── blacklist_jwt.py # Репозиторий для работы с отозванными JWT
│   │       ├── lot.py           # Репозиторий для лотов
│   │       ├── order.py         # Репозиторий для заказов
│   │       └── user.py          # Репозиторий для пользователей
│   └── main.py           # Точка входа в приложение
├── docker-compose.yml    # Конфигурация Docker Compose
├── Dockerfile            # Конфигурация Docker образа
├── pyproject.toml        # Конфигурация инструментов разработки
└── requirements.txt      # Зависимости проекта
```

Проект реализован с использованием архитектурного паттерна MVC (Model-View-Controller), адаптированного для REST API:

- **Model**: Представлен моделями в `core/models`, которые описывают структуру данных и взаимодействие с MongoDB через Beanie
- **View**: Представлен Pydantic-схемами в `api/*/schemas.py`, определяющие формат данных запросов и ответов
- **Controller**: Представлен эндпоинтами в `api/*/routes.py`, которые обрабатывают HTTP-запросы и координируют взаимодействие между моделями и представлениями

Дополнительно архитектура расширена слоями **Repository** (для абстракции доступа к данным) и **Service** (для инкапсуляции бизнес-логики) для соответствия принципам чистой архитектуры.

## Как запускать

### Локально

1. Склонируйте репозиторий:

   `git clone https://github.com/MagicWinnie/BestHackBackend.git`

2. Перейдите в директорию проекта:

   `cd BestHackBackend`

3. Создайте виртуальное окружение:

   `python -m venv .venv`

4. Активируйте виртуальное окружение:

   Windows: `venv\Scripts\activate`  
   Unix/Linux: `source venv/bin/activate`

5. Установите зависимости:

   `pip install -r requirements.txt`

6. Создайте файл `.env` с переменными окружения.

7. Запустите сервер приложения:

   `uvicorn src.main:app --host 0.0.0.0 --port 8888`

### Docker

1. Склонируйте репозиторий:

   `git clone https://github.com/MagicWinnie/BestHackBackend.git`

2. Перейдите в директорию проекта:

   `cd BestHackBackend`

3. Запустите Docker Compose:

   `docker-compose up --build -d`

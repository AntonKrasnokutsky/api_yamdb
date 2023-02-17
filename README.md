# API_YAmdb

## Авторы
Разработка курса и заданий Яндекс.Практикум
Иполнители:
- Алексей Акимов
- Алексей Соколов
- Антон Краснокутский

## Описание
Проект разрабатывался на курсе Python-разработчик Яндекс.Практикум. Является учебным командным проектом по изучению Django REST framework.
Предоставляет следующие эндпоинты:
- Авторизация (/api/v1/auth/)
- Категории произведений (/api/v1/categories/)
- Категория жанров (/api/v1/genres/)
- Произведения (/api/v1/titles/)
- Отзывы (/api/v1/titles/{title_id}/reviews/)
- Коментарии к отзывам (/api/v1/titles/{title_id}/reviews/{review_id}/comments/)
- Управлеие пользователями (/api/v1/users/)

## Технология
API_yatube использует ряд технологий:

- Django 3.2
- Django REST framework 3.12.4
- Simple JWT 4.7.2
- Django filter 22.1

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/AntonKrasnokutsky/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3.9 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python -m pip install -U pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

### Приvер запроса
При использовании на локальном сервере
#### Получение произведения
```
method GET
http://127.0.0.1:8000/api/v1/titles/
```
Пример ответа
```
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "id": 0,
            "name": "string",
            "year": 0,
            "rating": 0,
            "description": "string",
            "genre": [
                {
                    "name": "string",
                    "slug": "string"
                }
            ],
            "category": {
                "name": "string",
                "slug": "string"
            }
        }
    ]
}
```

#### Подробная информация о запросах здесь:
```
http://127.0.0.1:8000/redoc/
```

### API для блога с базовым функционалом создания постов, подписок на авторов, авторизацией по JWT токенам
**Примеры запросов в полной документации: после запуска проекта перейдите на http://127.0.0.1:8000/swagger/**

### Запуск проекта
Клонировать репозиторий:
```
git clone git@github.com:ReneNorth/api_final_yatube.git
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

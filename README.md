# stories.andreymal.org

Данный репозиторий содержит статические файлы, шаблоны и конфигурацию сайта
[stories.andreymal.org](https://stories.andreymal.org/), работающего на
движке [mini_fiction](https://github.com/andreymal/mini_fiction).


## Быстрый старт с Vagga

Если вы являетесь счастливым пользователем линукса с ядром, собранным с
`CONFIG_USER_NS=y`, то у вас есть возможность
[установить Vagga](http://vagga.readthedocs.org/en/latest/installation.html#ubuntu)
и получить готовый контейнер для разработки mini_fiction
(примечание: автор репозитория не из таких счастливчиков, поэтому
бесперебойная работа не гарантируется; о проблемах просьба сообщать):

1. Скачивание всех нужных данных

  `git clone https://github.com/andreymal/stories.andreymal.org`

  `cd stories.andreymal.org`

  `git clone https://github.com/andreymal/mini_fiction`

2. Установка и создание базы MySQL:

  `vagga db_init`

3. Запуск веб-сервера и всех связанных сервисов:

  `vagga run`

  (Первый запуск vagga будет долгим в связи с установкой контейнеров.)

  После запуска не выключайте до завершения настройки.

4. Подключение контента к свежеустановленному движку:

  `cp -Rp media.dump run/storage/main/media`

  `vagga manage loaddb /work/db.dump`

  `vagga manage collectstatic` — Выполнять при каждом обновлении статики

  `vagga manage createsuperuser` — Если нужно

При каждом изменении файлов проекта следует перезапускать uwsgi (а для
статики ещё и collectstatic). Если это сильно надоедает, можно вместо
uwsgi запустить встроенный сервер Flask, который умеет перезапускаться
автоматически:

`vagga run --exclude uwsgi`

`vagga devserver`

При работающем `vagga run` доступны следующие сервисы:

* Сам сайт: `http://localhost:5005/`

* Почтовый сервер Mailcatcher: `http://localhost:1080/`

* Отчёт о работе воркера Celery: `http://localhost:5555/`

* А также SphinxQL на порту 9360, MySQL на порту 3305, memcached на порту
  11219, uwsgi на порту 1818 и Redis на порту 6379.


## Установка вручную

* Устанавливаем Python 3.4 или выше

* Скачиваем репозиторий

```
git clone https://github.com/andreymal/stories.andreymal.org
cd stories.andreymal.org
```

* Далее устанавливаем сам mini_fiction. Некоторые зависимости вроде
  lxml, Pillow или scrypt могут собираться из исходников; подробнее
  см. в документации по mini_fiction.

Для разработки (virtualenv по вкусу):

```
virtualenv --no-site-packages env
. env/bin/activate

git clone https://github.com/andreymal/mini_fiction
cd mini_fiction

pip install -r optional-requirements.txt
make develop
cd ..  # назад в каталог stories.andreymal.org
```

Для просто потыкать и для production:

```
pip install mini_fiction[full]
```

* Настраиваем сам сайт:

```
cp local_settings.example.py local_settings.py

# Прописываем в переменных окружения, где искать конфигурацию
MINIFICTION_SETTINGS=local_settings.Local; export MINIFICTION_SETTINGS
PYTHONPATH=.; export PYTHONPATH
```

В файле `local_settings.py` предлагается настроить подключение к MySQL и отправку почты.

* Инициализируем данные (здесь и далее команды выполняются в virtualenv при его наличии
  и в корне проекта; также не забывайте указать файл настроек в переменных окружения):

```
mini_fiction loaddb db.dump
cp -Rp media.dump media
mini_fiction collectstatic  # Выполнять при каждом обновлении статики
mini_fiction createsuperuser  # Если нужно
```

* Теперь можно запустить сервер:

```
mini_fiction runserver
```

* Запуск Celery для обработки различных задач:

```
celery -A mini_fiction worker --loglevel=INFO
```

* Запуск Sphinx для поиска рассказов и глав (тоже из-под virtualenv, если он есть):

```
searchd -c sphinxconf.sh
```

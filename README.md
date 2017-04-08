# stories.andreymal.org

Данный репозиторий содержит статические файлы, шаблоны и конфигурацию сайта
[stories.andreymal.org](https://stories.andreymal.org/), работающего на
движке [mini_fiction](https://github.com/andreymal/mini_fiction).


## Установка

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
virtualenv env
. env/bin/activate

git clone https://github.com/andreymal/mini_fiction
cd mini_fiction

pip install -r optional-requirements.txt
make develop
cd ..  # назад в каталог stories.andreymal.org
```

Для просто потыкать и для production:

```
pip install 'mini_fiction[full]==0.0.3'
```

* Настраиваем сам сайт:

```
cp local_settings.example.py local_settings.py
```

(Возможно, понадобится прописать переменную окружения `PYTHONPATH=.` в случае,
если `local_settings.py` не подхватится сам по себе.)

В файле `local_settings.py` предлагается настроить подключение к MySQL и отправку почты.

* Проверяем работоспособноть настроек:

```
mini_fiction status
```

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

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
  см. в документации по mini_fiction. Пример установки dev-версии
  из репозитория (для боевого окружения вы можете собрать и установить
  whl-пакет):

```
virtualenv env
. env/bin/activate

git clone https://github.com/andreymal/mini_fiction
cd mini_fiction

pip install -r optional-requirements.txt
make develop
cd ..  # назад в каталог stories.andreymal.org
```

* Настраиваем сам сайт:

```
cp local_settings.example.py local_settings.py
```

(Возможно, понадобится прописать переменную окружения `PYTHONPATH=.` в случае,
если `local_settings.py` не подхватится сам по себе.)

В файле `local_settings.py` предлагается настроить `SECRET_KEY`, подключение
к MySQL, отправку почты и прочее.

* Загружаем и распаковываем актуальный дамп некоторых объектов базы данных
  (жанры, персонажи, картинки в шапке и т.п.) отсюда:

  https://stories.andreymal.org/dump/

  Помещаем `media` туда, где собственно должен располагаться каталог `media`
  (если вы изменили путь в настройках), а дамп базы загружаем следующей
  командой (после чего каталог `dump` можно удалить):

```
mini_fiction loaddb dump
```

* Если скачать дамп нет возможности или не хочется, то запускаем
  `mini_fiction seed` и всё остальное заполняем позже через админку.

* Проверяем работоспособность настроек:

```
mini_fiction status
```

* Если нужно, создаём суперпользователя:

```
mini_fiction createsuperuser
```

* Теперь можно запустить сервер:

```
mini_fiction runserver
```

* После запуска сайт станет доступен по адресу `http://localhost:5000/`

* Если вы хотите сгрузить каталог `static` куда-то отдельно для, например,
  раздачи через nginx, можно прописать в настройках путь к нужному вам
  каталогу, например: `STATIC_ROOT = os.path.join(os.getcwd(), 'static')` —
  и складировать туда статику командой `mini_fiction collectstatic`. Но тогда
  нужно не забывать повторять эту команду при каждом обновлении mini_fiction.

* Запуск Celery для обработки различных задач (в этом примере worker и beat
  в одном процессе):

```
celery -A mini_fiction worker -B --loglevel=INFO
```

* Запуск Sphinx для поиска рассказов и глав (тоже из-под virtualenv, если
  он есть):

```
searchd -c sphinxconf.sh --nodetach
```

* Для случая, когда виртуальное окружение находится здесь же в каталоге `env`,
  можно запускать Sphinx с помощью прилагаемого скрипта, который автоматически
  включает виртуальное окружение:

```
./sphinxstart.sh
```

Подробнее про настройку и развёртывание читайте в файле
`mini_fiction/INSTALL.md`.

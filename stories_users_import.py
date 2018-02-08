#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import random
import string
from datetime import datetime
from urllib.request import Request, urlopen

import lxml.html
import lxml.etree
from pony import orm
from flask import current_app

from mini_fiction.models import Author, Contact


def parse_user(user_id, raw_data):
    # TODO: decode cloudflare emails, e.g. https://stories.everypony.ru/accounts/18568/
    # https://github.com/andreymal/tabun_api/blob/aaff48e0c51e9c87065f659a6c7d12b07963e93e/tabun_api/utils.py#L921

    data_start = raw_data.find(b'<div class="row">')
    data_end = raw_data.find(b'<!-- Content end -->', data_start)
    if data_start < 0 or data_end < 0:
        return None

    raw_data = raw_data[data_start:data_end].decode('utf-8')
    div = lxml.html.fragments_fromstring(raw_data)[0].findall("div")[1]

    username = div.xpath('h1[@id="author-name"]/img')[0].tail.strip()
    bio = div.xpath('p[@class="author-description"]/text()')
    bio = bio[0].strip() if bio else ''

    contacts = []

    for a in div.xpath('p[@class="contact-links"]/a'):
        if a.get('class') == 'jabberlink':
            contacts.append({'name': 'xmpp', 'value': a.get('href')[5:]})
        elif a.get('class') == 'skypelink':
            contacts.append({'name': 'skype', 'value': a.get('href')[6:]})
        elif a.get('class') == 'tabunlink':
            contacts.append({'name': 'tabun', 'value': a.get('href')[:-1].rsplit('/', 1)[-1].strip()})
        elif a.get('class') == 'forumlink':
            contacts.append({'name': 'forum', 'value': a.get('href')})

    return {
        'id': user_id,
        'username': username,
        'date_joined': datetime(1970, 1, 1, 0, 0, 0),
        'bio': bio,
        'contacts': contacts,
    }

def grab_next_users(last_ids):
    last_id = max(last_ids)

    # Собираем пачку айдишников, которые будем проверять
    check_ids = [x for x in range(min(last_ids), last_id + 50) if x not in last_ids]

    interval = current_app.config['USERS_IMPORT_INTERVAL']

    failed = 0
    for user_id in check_ids:
        req = Request(current_app.config['USERS_IMPORT_SITE'] + '/accounts/{}/'.format(user_id))
        req.add_header('User-Agent', current_app.user_agent)

        try:
            # Качаем юзера
            raw_data = urlopen(req).read()
        except Exception:
            # Если нет аккаунта аж для трёх айдишников подряд, то считаем,
            # что никто просто ещё не нарегался, и прекращаем работу
            if user_id > last_id:
                failed += 1
                if failed >= 3:
                    break
            # Ошибки просто игнорируем
            time.sleep(interval)
            continue

        # Читаем юзера и возвращаем его при успехе
        userinfo = parse_user(user_id, raw_data)
        if userinfo:
            yield userinfo

        # Не дудосим сайт, спешить некуда
        time.sleep(interval)


def import_users():
    # Получаем последние id пользователей
    with orm.db_session:
        last_ids = orm.select(x.id for x in Author)
        if current_app.config.get('USERS_IMPORT_MAX_ID') is not None:
            max_id = current_app.config['USERS_IMPORT_MAX_ID']
            last_ids = last_ids.filter(lambda aid: aid <= max_id)
        last_ids = last_ids.order_by(-1)[:10]

    # Скачиваем новых пользователей, id которых больше, чем наш последний
    for userinfo in grab_next_users(last_ids):
        # Ох уж этот CloudFlare
        if not userinfo.get('username'):
            print('Found new user with id {0}, but without username! Replaced to __stories_account_{0}__. Saving'.format(userinfo['id']))
            userinfo['username'] = '__stories_account_{0}__'.format(userinfo['id'])
        else:
            print('Found new user {} with id {}, saving'.format(userinfo['username'], userinfo['id']))
        # Найденного нового пользователя создаём
        contacts = userinfo.pop('contacts')

        userinfo['activated_at'] = userinfo['date_joined']
        userinfo['session_token'] = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))

        with orm.db_session:
            author = Author(**userinfo)
            author.flush()
            for c in contacts:
                Contact(author=author, **c).flush()


def configure_app(register_hook):
    current_app.config.setdefault('USERS_IMPORT_SITE', 'https://stories.everypony.ru')
    current_app.config.setdefault('USERS_IMPORT_MAX_ID', None)
    current_app.config.setdefault('USERS_IMPORT_INTERVAL', 3)
    current_app.tasks['import_users'] = current_app.celery.task(name='import_users')(import_users)

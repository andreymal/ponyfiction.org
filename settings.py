#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mini_fiction.settings import Config as BaseConfig


class Config(BaseConfig):
    SITE_NAME = {'default': 'Библиотека stories.andreymal.org'}
    SITE_FEEDBACK = 'https://tabun.everypony.ru/talk/add/?talk_users=andreymal'

    CACHE_PREFIX = 'mfc_sao_'

    REGISTRATION_AUTO_LOGIN = True
    REGISTRATION_OPEN = False

    CELERY_ALWAYS_EAGER = False
    SPHINX_DISABLED = False

    PLUGINS = ['stories_migration']

    AVATARS_UPLOADING = True

    STATIC_V = '20170826'
    LOCALSTATIC_ROOT = 'localstatic'
    LOCALTEMPLATES = 'templates'

    STORY_COMMENTS_BY_GUEST = True
    NEWS_COMMENTS_BY_GUEST = True
    STARS_MINIMUM_VOTES = 1

    PUBLISH_SIZE_LIMIT = 20

    FAVICON_URL = '/localstatic/i/favicon.ico'

    DEFAULT_USERPIC = {'endpoint': 'localstatic', 'filename': 'i/userpic.jpg'}

    CONTACTS = [
        {
            'name': 'xmpp',
            'label': {
                'default': 'Jabber ID (XMPP)',
            },
            'schema': {
                'regex': r'^.+@([^.@][^@]+)',
                'error_messages': {'regex': 'Пожалуйста, исправьте ошибку в адресе jabber: похоже, он неправильный'}
            },
            'link_template': 'xmpp:{value}?message;type=chat',
            'title_template': '{value}',
        },
        {
            'name': 'skype',
            'label': {
                'default': 'Skype ID',
            },
            'schema': {
                'regex': r'^[a-zA-Z0-9\._-]+$',
                'error_messages': {'regex': 'Пожалуйста, исправьте ошибку в логине skype: похоже, он неправильный'}
            },
            'link_template': 'skype:{value}',
            'title_template': '{value}',
        },
        {
            'name': 'tabun',
            'label': {
                'default': 'Логин на Табуне',
            },
            'schema': {
                'regex': r'^[a-zA-Z0-9-_]+$',
                'error_messages': {'regex': 'Пожалуйста, исправьте ошибку в имени пользователя: похоже, оно неправильно'}
            },
            'link_template': 'https://tabun.everypony.ru/profile/{value}/',
            'title_template': '{value}',
        },
        {
            'name': 'forum',
            'label': {
                'default': 'Профиль на Форуме',
            },
            'schema': {
                'regex': r'^https?://forum.everypony.ru/memberlist.php\?.+$',
                'error_messages': {'regex': 'Вставьте полную ссылку на профиль'}
            },
            'link_template': '{value}',
            'title_template': '{value}',
        },
        {
            'name': 'vk',
            'label': {
                'default': 'Логин ВКонтакте',
            },
            'schema': {
                'regex': r'^[a-zA-Z0-9\._-]+$',
                'error_messages': {'regex': 'Пожалуйста, исправьте ошибку в логине ВК: похоже, он неправильный'}
            },
            'link_template': 'https://vk.com/{value}',
            'title_template': '{value}',
        },
    ]


class Development(Config):
    DEBUG = True
    SQL_DEBUG = True
    DEBUG_TB_ENABLED = True
    CHECK_PASSWORDS_SECURITY = False

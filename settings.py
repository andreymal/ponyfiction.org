#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from celery.schedules import crontab

import mini_fiction
from mini_fiction.settings import Config as BaseConfig


class Config(BaseConfig):
    SITE_NAME = {'default': 'Библиотека ponyfiction.org'}
    SITE_INDEX_TITLE = {'default': 'Библиотека ponyfiction.org'}
    SITE_DESCRIPTION = {'default': 'Библиотека фанфиков по вселенной сериала My Little Pony: Friendship is Magic'}
    SITE_FEEDBACK = 'https://tabun.everypony.ru/talk/add/?talk_users=andreymal'

    USER_AGENT_POSTFIX = 'ponyfiction.org/{}'.format(mini_fiction.__version__)

    CACHE_KEY_PREFIX = 'mfc_pf_'

    REGISTRATION_AUTO_LOGIN = True
    REGISTRATION_OPEN = False

    CELERY_ALWAYS_EAGER = False
    CELERY_CONFIG = dict(BaseConfig.CELERY_CONFIG)
    CELERY_CONFIG['beat_schedule'] = dict(BaseConfig.CELERY_CONFIG['beat_schedule'])
    CELERY_CONFIG['beat_schedule']['import_users'] = {
        'task': 'import_users',
        'schedule': crontab(minute='27,57'),
    }

    SPHINX_DISABLED = False

    PLUGINS = ['stories_migration', 'stories_users_import']

    USERS_IMPORT_MAX_ID = None

    CAPTCHA_CLASS = 'mini_fiction.captcha.ReCaptcha'
    CAPTCHA_FOR_GUEST_COMMENTS = True

    AVATARS_UPLOADING = True

    LOCALSTATIC_ROOT = 'localstatic'
    LOCALTEMPLATES = 'templates'

    STORY_COMMENTS_BY_GUEST = True
    NEWS_COMMENTS_BY_GUEST = True
    MINIMUM_VOTES_FOR_VIEW = 1

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

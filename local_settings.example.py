#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from settings import Development


class Local(Development):
    # DATABASE_ENGINE = 'mysql'
    # DATABASE = {
    #     'host': '127.0.0.1',
    #     'port': 3306,
    #     'user': 'fanfics',
    #     'passwd': 'fanfics',
    #     'db': 'mini_fiction',
    # }

    # SITE_URL = 'https://stories.andreymal.org'

    # ADMINS = ['admin@example.org']
    # ERROR_EMAIL_FROM = 'minifiction@example.org'
    # ERROR_EMAIL_HANDLER_PARAMS = {'mailhost': ('127.0.0.1', 1025)}

    # EMAIL_PORT = 1025
    # DEFAULT_FROM_EMAIL = 'minifiction@example.org'

    # REGISTRATION_OPEN = True
    # RECAPTCHA_PUBLIC_KEY = '...'
    # RECAPTCHA_PRIVATE_KEY = '...'
    # NOCAPTCHA = False

    # PROXIES_COUNT = 1
    # SECRET_KEY = 'foo'

    SPHINX_CONFIG = dict(Development.SPHINX_CONFIG)
    SPHINX_CONFIG['connection_params'] = {'host': '127.0.0.1', 'port': 9306, 'charset': 'utf8'}

    SPHINX_ROOT = os.path.join(os.path.abspath(os.getcwd()), 'sphinx')
    SPHINX_SEARCHD = dict(Development.SPHINX_SEARCHD)
    SPHINX_SEARCHD['listen'] = '0.0.0.0:9306:mysql41'
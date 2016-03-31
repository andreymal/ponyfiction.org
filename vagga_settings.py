#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from settings import Development


class Vagga(Development):
    DATABASE_ENGINE = 'mysql'
    DATABASE = {
        'host': '127.0.0.1',
        'port': 3305,
        'user': 'root',
        'passwd': 'fanfics',
        'db': 'mini_fiction',
    }

    MEMCACHE_SERVERS = ['127.0.0.1:11219']

    SITE_URL = 'http://localhost:5005'

    ADMINS = ['admin@vagga.example.org']
    ERROR_EMAIL_FROM = 'minifiction@vagga.example.org'
    ERROR_EMAIL_HANDLER_PARAMS = {'mailhost': ('127.0.0.1', 1025)}

    EMAIL_PORT = 1025
    DEFAULT_FROM_EMAIL = 'minifiction@vagga.example.org'

    STATIC_ROOT ='/storage/static'
    MEDIA_ROOT = '/storage/media'
    LOCALSTATIC_ROOT = '/work/localstatic'
    LOCALTEMPLATES = '/work/templates'

    PROXIES_COUNT = 1

    SPHINX_CONFIG = dict(Development.SPHINX_CONFIG)
    SPHINX_CONFIG['connection_params'] = {'host': '127.0.0.1', 'port': 9360, 'charset': 'utf8'}

    SPHINX_ROOT = '/sphinx'
    SPHINX_SEARCHD = dict(Development.SPHINX_SEARCHD)
    SPHINX_SEARCHD['listen'] = '0.0.0.0:9360:mysql41'

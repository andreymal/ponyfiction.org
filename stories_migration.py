#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import string
import urllib

from pony import orm
from pony.orm import db_session
from flask import Blueprint, current_app, request, redirect, url_for, render_template, abort
from flask_login import current_user

from mini_fiction.models import Author, PasswordResetProfile
from mini_fiction.database import db


class MigrationProfile(db.Entity):
    user_id = orm.Required(int, index=True)
    auth_token = orm.Required(str, 64, index=True)
    inline_token = orm.Required(str, 64)


bp = Blueprint('stories_migration', __name__)


templates = {
    'migration_new.html': '''{% extends base %}
{% from 'macro.html' import breadcrumbs with context %}
{% block content %}
<div class="row">
  <div class="span12">
    {{- breadcrumbs() }}
    <h1>{{ page_title }}</h1>
      <form action="" method="POST" enctype="multipart/form-data" class="form-horizontal migration-form">
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
        <fieldset>
          <div class="control-group{% if error %} error{% endif %}">
            <label class="control-label">Ник на {{ config['MIGRATION_NAME'] }}</label>
            <div class="controls">
              <input type="text" name="author" maxlength="255" />
            </div>
          </div>
        {% if error %}
          <div class="control-group error"><span class="help-inline">{{ error }}</span></div>
        {% endif %}
        <div class="form-actions">
          <button class="btn btn-primary" type="submit">Продолжить</button>
        </div>
      </fieldset>
    </form>
    {{- breadcrumbs() }}
  </div>
</div>
{% endblock %}
''',
    'migration_approve.html': '''{% extends base %}
{% from 'macro.html' import breadcrumbs with context %}
{% block content %}
<div class="row">
  <div class="span12" style="margin-top: 2em; margin-bottom: 2em;">
    {{- breadcrumbs() }}
    <h1>{{ page_title }}</h1>
    {% if nodownload %}
      <div class="alert alert-warning">Не получается посмотреть <a href="{{ nodownload_link }}" target="_blank">страницу аккаунта</a>: {{ nodownload }}.
      Если эта ошибка стабильно повторяется при каждом обновлении страницы и никуда не пропадает, сообщите об этом куда-нибудь.</div>
    {% endif %}
    Авторизуйтесь на <a href="{{ config['MIGRATION_SITE'] }}/" target="_blank">{{ config['MIGRATION_NAME'] }}</a> и в «Пару слов о себе» в настройках профиля добавьте следующие буковки:<br/><br/>
    <input readonly type="text" style="cursor: text; font-weight: bold; font-size: 1.35em; width: 100%;" value="{{ inline_token }}" /><br/><br/>
    После чего обновите эту страницу. Сайт прочитает эти буковки, убедится, что вы — это вы (ведь только вы сможете написать эти буковки), и пустит вас сюда.
    После этого эти буковки можно будет стереть.
    {{- breadcrumbs() }}
  </div>
</div>
{% endblock %}
'''
}


@bp.route('/stories_auth/', methods=('GET', 'POST'))
@db_session
def auth():
    error = None
    if request.method == 'POST':
        user = Author.get(username=request.form.get('author')) if request.form.get('author') else None
        if not user:
            error = 'Нет такого пользователя'
        elif user.email:
            error = 'У пользователя установлена электронная почта, получайте доступ через неё'
        else:
            r = MigrationProfile(
                user_id=user.id,
                auth_token=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(24)),
                inline_token=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(24)),
            )
            r.flush()
            return redirect(url_for('stories_migration.approve', auth_token=r.auth_token))
    return my_render_template('migration_new.html', error=error, page_title='Авторизация через ' + current_app.config['MIGRATION_NAME'])


@bp.route('/stories_auth/<auth_token>/', methods=('GET', 'POST'))
@db_session
def approve(auth_token):
    migration = MigrationProfile.get(auth_token=auth_token)
    if not migration:
        abort(404)
    nodownload = None
    nodownload_link = None

    data = current_app.cache.get('stories_migration_{}'.format(migration.user_id))
    if not data:
        link = '{}/accounts/{}/'.format(current_app.config['MIGRATION_SITE'], migration.user_id)
        req = urllib.request.Request(link)
        req.add_header('Accept', 'text/html, text/*, */*')
        req.add_header('Accept-Language', 'ru-RU,ru;q=0.8')
        req.add_header('User-Agent', 'Mozilla/5.0; mini_fiction')
        try:
            data = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', 'replace')
        except IOError as exc:
            nodownload = str(exc).replace('&', '&amp;').replace('<', '&lt;')
            nodownload_link = link
        # простейший анти-DDoS
        current_app.cache.set('stories_migration_{}'.format(migration.user_id), data, 2)

    if data and migration.inline_token in data:
        prp = PasswordResetProfile(
            user=Author.get(id=migration.user_id),
            activation_key=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(40)),
            activated=False,
        )
        prp.flush()
        for m in MigrationProfile.select(lambda x: x.user_id == migration.user_id):
            m.delete()
        migration = None
        return redirect(url_for('auth.password_reset_confirm', activation_key=prp.activation_key))

    return my_render_template(
        'migration_approve.html',
        nodownload=nodownload,
        nodownload_link=nodownload_link,
        inline_token=migration.inline_token,
        page_title='Авторизация через ' + current_app.config['MIGRATION_NAME']
    )


def my_render_template(name, **kwargs):
    template = current_app.jinja_env.from_string(templates[name])
    template.name = 'stories_migration/' + name
    return render_template(template, **kwargs)


def custom_nav():
    if current_user.is_authenticated:
        return ''
    return '<li id="nav_stories_auth"><a href="/stories_auth/">Войти через stories.everypony.ru</a></li>'


def configure_app(register_hook):
    current_app.config.setdefault('MIGRATION_SITE', 'https://stories.everypony.ru')
    current_app.config.setdefault('MIGRATION_NAME', 'stories.everypony.ru')
    current_app.register_blueprint(bp)
    register_hook('nav', custom_nav)

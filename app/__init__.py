import logging

import graypy
from flask import Flask
from raven import setup_logging
from raven.contrib.flask import Sentry
from raven.handlers.logging import SentryHandler

from app.models import db, data_store
from app.v1.logging_filters import RequestInfoFilter


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    # init DB
    db.init_app(app)

    # init redis
    data_store.init_app(app)

    # init v1 blueprint
    from app.v1.controller import v1_blueprint
    app.register_blueprint(v1_blueprint, url_prefix='/api/v1')

    # init graylog
    _init_graylog(app)

    # init sentry
    _init_sentry(app)

    return app


def _init_graylog(app):
    if app.config['LOGGING']:
        gelf_handler = graypy.GELFHandler(
            app.config['GRAYLOG_HOST'],
            chunk_size=graypy.LAN_CHUNK)
        gelf_handler.addFilter(RequestInfoFilter())
        app.logger.setLevel(logging.INFO)
        app.logger.addHandler(gelf_handler)


def _init_sentry(app):
    if app.config['ENABLE_SENTRY']:
        sentry = Sentry(app)
        sentry_handler = SentryHandler(sentry.client)
        sentry_handler.setLevel(logging.WARNING)
        app.logger.addHandler(sentry_handler)
        setup_logging(sentry_handler)

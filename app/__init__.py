import logging

import graypy
from flask import Flask

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

    _init_graylog(app)

    return app


def _init_graylog(app):
    if app.config['LOGGING']:
        gelf_handler = graypy.GELFHandler(
            app.config['GRAYLOG_HOST'],
            chunk_size=graypy.LAN_CHUNK)
        gelf_handler.addFilter(RequestInfoFilter())
        app.logger.setLevel(logging.INFO)
        app.logger.addHandler(gelf_handler)
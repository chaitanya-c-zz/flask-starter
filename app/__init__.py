from flask import Flask

from app.models import db, data_store
from app.v1.controller import v1_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    # init DB
    db.init_app(app)

    # init redis
    data_store.init_app(app)

    # init v1 blueprint
    app.register_blueprint(v1_blueprint, url_prefix='/api/v1')

    return app

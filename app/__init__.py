from flask import Flask
from flask_redis import Redis

from app.models import db
from app.v1.controller import v1_blueprint

data_store = Redis()


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

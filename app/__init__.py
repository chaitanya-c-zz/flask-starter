import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

data_store = redis.StrictRedis(
    host=app.config.get('REDIS_HOST'), port=app.config.get('REDIS_PORT')
)

# Register FlaskView with the app and a base route
from app.v1.controller.status_controller import StatusController
StatusController.register(app, route_base='/api/v1')

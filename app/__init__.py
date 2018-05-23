import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

data_store = redis.StrictRedis(
    host=app.config.get('REDIS_HOST'), port=app.config.get('REDIS_PORT')
)

from flask_redis import Redis
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
data_store = Redis()

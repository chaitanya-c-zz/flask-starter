import time

from sqlalchemy import create_engine

from app import create_app

app = create_app()
db_name = app.config.get('DB_NAME')
user = app.config.get('DB_USER')
password = app.config.get('DB_PASSWORD')
host = app.config.get('DB_HOST')


def create_db(retry=0):
    try:
        mysql_engine = create_engine(
            'mysql://{}:{}@{}'.format(user, password, host)
        )
        result = mysql_engine.execute(
            'CREATE DATABASE IF NOT EXISTS {}'.format(db_name)
        )
        result.close()
    except Exception:
        if retry > 3:
            raise
        time.sleep(1)
        create_db(retry + 1)


create_db()

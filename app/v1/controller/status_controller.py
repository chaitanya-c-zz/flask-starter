from flask import jsonify
from flask_classy import FlaskView, route

from app import db, data_store


class StatusController(FlaskView):
    """
       Controller class for status endpoints.
    """

    @route('/status', methods=['GET'])
    def status(self):
        """
        Gives status for MySQL and Redis
        """
        status = {
            'mysql': 'OK',
            'redis': 'OK',
        }
        status_code = 200
        try:
            db.engine.execute("select 1")
        except Exception:
            status['mysql'] = 'Error'
            status_code = 503
        try:
            data_store.ping()
        except Exception:
            status['redis'] = 'Error'
            status_code = 503
        return jsonify(status), status_code

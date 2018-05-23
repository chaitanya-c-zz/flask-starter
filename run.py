from datetime import datetime

from flask import request_finished, request, g

from app import create_app

app = create_app()


@request_finished.connect_via(app)
def request_logger(sender, response, **extra):
    g.response = response
    if app.config['LOGGING']:
        app.logger.info("%s %s%s [%d]" % (
            request.method,
            request.script_root,
            request.path,
            response.status_code
        ))


@app.before_request
def before_request():
    g.start_time = datetime.now()


if __name__ == '__main__':
    app.run(host='0.0.0.0')

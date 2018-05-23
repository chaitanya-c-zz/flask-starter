import datetime
import logging
import socket
import time

from flask import request, g


class RequestInfoFilter(logging.Filter):
    """
    Request Info Filter adds extra information about the request into logs.
    """

    def filter(self, record):
        record.application = "Rx-TATEngine"
        record.host = socket.gethostname()
        record.timestamp = time.time()
        record.version = "1.1"

        # For workers
        if not request:
            return True
        record.request_url = request.base_url
        record.request_method = request.method
        record.user_agent = request.headers.get('User-Agent')
        record.request_ip = request.remote_addr
        record.request_referer = request.referrer
        record.cid = getattr(g, 'Cid', None)
        record.timezone = getattr(g, 'timezone', None)
        record.request_host = request.headers.get('Host')
        start_time = getattr(g, 'start_time', None)
        if start_time:
            timedelta = datetime.datetime.now() - start_time
            record.response_time = timedelta.total_seconds()
        response = getattr(g, 'response', None)
        if response:
            record.response_code_v2 = response.status_code
            if response.status_code in [400, 403]:
                record.error_message = response.data

            if 400 > response.status_code:
                record.level = 6  # 6 - Info
            elif 409 == response.status_code:
                record.level = 5  # 5 - Notice
            elif 400 == response.status_code:
                record.level = 5  # 5 - Notice
            elif 500 > response.status_code:
                record.level = 3  # 3 - Error
            else:
                record.level = 2  # 2 - Critical

            if request.method == 'POST':
                post_data = []
                for k, v in request.form.iteritems():
                    if self.filter_key(k):
                        post_data.append((k, '*' * 8))
                    else:
                        post_data.append((k, v))
                record.request_post_data = str(post_data)
            elif request.method == 'GET':
                args = []
                for k, v in request.args.iteritems():
                    if k.lower() == 'secret':
                        args.append((k, '*' * 8))
                    else:
                        args.append((k, v))
                record.request_args = str(args)

        return True

    def filter_key(self, key):
        regexes = [
            'email_id', 'number'
        ]
        for regex in regexes:
            if regex in key.lower():
                return True
        return False

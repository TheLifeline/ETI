from flask.logging import default_handler
from flask import has_request_context, request
from ..config import basedir
import logging
import time
import os

class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None
        return super().format(record)

class webLog(object):
    def __init__(self, app):
        formatter = RequestFormatter(
            '[%(asctime)s] %(remote_addr)s requested [%(url)s] %(levelname)s in %(module)s:\n'
            '\t %(message)s'
        )
        default_handler.setFormatter(formatter)
        logging.getLogger('werkzeug').addHandler(default_handler)
        logging.getLogger('werkzeug').addHandler(self._get_fh(formatter))
        app.logger.name = 'app'
    
    def _get_fh(self,formatter=None,level=logging.NOTSET):
        rq = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        log_path = os.path.join(basedir,"logs")
        if not os.path.isdir(log_path):
            os.makedirs(log_path)
        log_name = os.path.join(log_path, rq + '.log')
        logfile = log_name
        
        fh = logging.FileHandler(logfile, mode='w')
        fh.setLevel(level)
        if formatter:
            fh.setFormatter(formatter)
        return fh

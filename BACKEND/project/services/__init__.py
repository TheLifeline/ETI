from .webJwt import webJwtServices
from flask_cors import CORS
from .ES import ESTool
from .webLog import webLog
esdb = ESTool()

def init_app(app):
    global esdb
    webJwtServices(app)
    webLog(app)
    CORS(app)
    esdb.init(app=app)
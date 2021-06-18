from .webJwt import webJwtServices
from flask_cors import CORS
from .ES import init
from .webLog import webLog

def init_app(app):
    webJwtServices(app)
    webLog(app)
    CORS(app)
    init()
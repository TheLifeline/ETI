from .webJwt import webJwtServices
from flask_cors import CORS
from .ES import init

def init_app(app):
    webJwtServices(app)
    CORS(app)
    init()
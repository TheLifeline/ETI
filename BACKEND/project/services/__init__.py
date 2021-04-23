from .webJwt import webJwtServices
from flask_cors import CORS

def init_app(app):
    webJwtServices(app)
    CORS(app)
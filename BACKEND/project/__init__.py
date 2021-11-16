from flask import Flask
from .config import config
from . import models, routes, services
from .models.Case import Case,get_all_case_info
from .models.User import User
from .models.File import File,file_type
import random

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    models.init_app(app)
    routes.init_app(app)
    services.init_app(app)

    if config_name!="production":
        with app.app_context():
            models.db.create_all()
            user = User(username="admin",password="123")      
            models.db.session.add(user)
            models.db.session.commit()
            case = Case(caseName="test")
            models.db.session.add(case)
            models.db.session.commit()
    return app

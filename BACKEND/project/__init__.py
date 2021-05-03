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
            user = User(username="123",password="123")      
            models.db.session.add(user)
            models.db.session.commit()
            case = Case(caseName="test")
            models.db.session.add(case)
            models.db.session.commit()
            temp_id=Case.query.filter_by(caseName="test").first().id
            temp_caseName="test"
            for i in range(10):
                fileType=random.choice(file_type)
                file1 = File(caseID=temp_id,fileName="test",fileOrigin="test",fileType=fileType,fileLable="test",fileDescribe="test")
                models.db.session.add(file1)
                models.db.session.commit()
    return app

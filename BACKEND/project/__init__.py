from flask import Flask
from .config import config
from . import models, routes, services
from .models.Case import Case,get_all_case_info
from .models.User import User
from .models.File import File

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
            file1 = File(caseID=temp_id,downloadPath="test",fileName="test",fileOrigin="test",fileType="image",fileLable="test",fileDescribe="test")
            models.db.session.add(file1)
            models.db.session.commit()
            file1 = File(caseID=temp_id,downloadPath="test",fileName="test",fileOrigin="test",fileType="text",fileLable="test",fileDescribe="test")
            models.db.session.add(file1)
            models.db.session.commit()
            file1 = File(caseID=temp_id,downloadPath="test",fileName="test",fileOrigin="test",fileType="sheet",fileLable="test",fileDescribe="test")
            models.db.session.add(file1)
            models.db.session.commit()
            file1 = File(caseID=temp_id,downloadPath="test",fileName="test",fileOrigin="test",fileType="mirror",fileLable="test",fileDescribe="test")
            models.db.session.add(file1)
            models.db.session.commit()
            file1 = File(caseID=temp_id,downloadPath="test",fileName="test",fileOrigin="test",fileType="zip",fileLable="test",fileDescribe="test")
            models.db.session.add(file1)
            models.db.session.commit()
            file1 = File(caseID=temp_id,downloadPath="test",fileName="test",fileOrigin="test",fileType="others",fileLable="test",fileDescribe="test")
            models.db.session.add(file1)
            models.db.session.commit()
    return app

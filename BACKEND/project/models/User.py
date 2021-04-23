from . import db

class User(db.Model):
    __tablename__ = 'table_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    createtime = db.Column(db.DateTime())






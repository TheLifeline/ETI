from . import db

class File(db.Model):
    __tablename__ = 'table_file'
    id = db.Column(db.Integer, primary_key=True)
    caseID = db.Column(db.Integer)
    downloadPath = db.Column(db.String(600))
    fileName = db.Column(db.Text())
    fileOrigin = db.Column(db.Text())
    fileType = db.Column(db.Text())
    fileLable = db.Column(db.Text())
    fileDescribe = db.Column(db.Text())
    createtime = db.Column(db.DateTime())

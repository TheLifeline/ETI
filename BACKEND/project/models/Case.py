from . import db
from .File import file_type

class Case(db.Model):
    __tablename__ = 'table_case'
    id = db.Column(db.Integer, primary_key=True)
    caseName = db.Column(db.String(20))
    createtime = db.Column(db.DateTime())

def get_all_case_info():
    sql = "select table_case.id,caseName," + str(','.join(["sum(case when fileType = '{}' then 1 else 0 end)".format(i) for i in file_type])) + " from table_case LEFT OUTER join table_file ON table_case.id = table_file.caseID group by table_case.id;"
    result = db.session.execute(sql)
    keys=["caseID","caseName"] +[i+"Count" for i in file_type]
    result_list = result.fetchall()
    result = [dict(zip(keys, values)) for values in result_list]
    return result

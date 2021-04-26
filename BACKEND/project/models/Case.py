from . import db

class Case(db.Model):
    __tablename__ = 'table_case'
    id = db.Column(db.Integer, primary_key=True)
    caseName = db.Column(db.String(20))
    createtime = db.Column(db.DateTime())

def get_all_case_info():
    result = db.session.execute("""
select table_case.id,
       caseName,
       sum(case when fileType = 'image' then 1 else 0 end)  as imageCount,
       sum(case when fileType = 'text' then 1 else 0 end)   as textCount,
       sum(case when fileType = 'sheet' then 1 else 0 end)  as sheetCount,
       sum(case when fileType = 'mirror' then 1 else 0 end) as mirrorCount,
       sum(case when fileType = 'zip' then 1 else 0 end)    as zipCount,
       sum(case when fileType = 'others' then 1 else 0 end) as othersCount
from table_case
         LEFT OUTER join table_file
              ON table_case.id = table_file.caseID
group by table_case.id;
    """)
    keys=["caseID","caseName","imageCount","textCount","sheetCount","mirrorCount","zipCount","othersCount"]
    result_list = result.fetchall()
    result = [dict(zip(keys, values)) for values in result_list]
    return result

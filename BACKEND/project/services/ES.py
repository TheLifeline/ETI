from elasticsearch_dsl import Document, Integer, Keyword, Text, Boolean
from elasticsearch_dsl import Q, Search, connections

# Define a default Elasticsearch client
connect = connections.create_connection(hosts=['localhost:19200'])


class FileInfo(Document):
    caseID = Integer()
    fileType = Keyword()  # 需要传入列表类型
    fileLable = Keyword()
    downloadPath = Text(analyzer='simple')
    fileDescribe = Text(analyzer='ik_smart')
    caseName = Text(analyzer='ik_smart', fields={'raw': Keyword()})
    fileName = Text(analyzer='ik_smart', fields={'raw': Keyword()})
    fileOrigin = Text(analyzer='ik_smart', fields={'raw': Keyword()})
    isDelete = Boolean()

    class Index:
        name = 'file'
        settings = {
            "number_of_shards": 2,
        }

    def save(self, ** kwargs):
        self.isDelete=False
        return super(FileInfo, self).save(** kwargs)

def search_file_in_ES(query_str, caseID=None):
    s = Search(using=connect, index="file").filter('match', isDelete=False)
    if caseID is not None:
        s = s.filter("match", caseID=caseID)
    s = s.query('bool', should=[Q("match", fileDescribe=query_str),
                                Q("match", fileName=query_str),
                                Q("match", fileOrigin=query_str),
                                Q('bool', should=[Q("match", fileType=query_str),
                                                  Q("match", fileLable=query_str),
                                                  Q("match", caseName=query_str),
                                                  Q("match", downloadPath=query_str)])])

    response = s.execute()
    json_list = []
    for hit in response:
        result = dict(zip(dir(hit), [getattr(hit, name) for name in dir(hit)]))
        result["id"] = result["meta"].id
        result.pop("meta")
        json_list.append(result)
    return json_list

def save_file(**Keyword):
    FileInfo(**Keyword).save()

def init():
    FileInfo.init()

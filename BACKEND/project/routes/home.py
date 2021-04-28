from flask import Blueprint
from flask_jwt import jwt_required, current_identity
from werkzeug.utils import secure_filename
from flask import jsonify,request

from ..config import basedir
from ..models.Case import get_all_case_info
from .. import models
import threading
import os


home_bp = Blueprint('home_bp', __name__)
UPLOAD_FOLDER = os.path.join(basedir,"temp")

@home_bp.route('/', methods=['GET', 'POST'])
@jwt_required()
def index():
    return "Hello World!", 200

@home_bp.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    chunkNumber = request.form.get("chunkNumber")
    # currentChunkSize = request.form.get("currentChunkSize")
    # totalSize = request.form.get("totalSize")
    # identifier = request.form.get("identifier")
    filename = request.form.get("filename")
    totalChunks = request.form.get("totalChunks")
    # relativePath = request.form.get("relativePath")
    describe = request.form.get("describe")
    print(describe)
    if file.filename == '':
        return jsonify({"errno":400, "msg":"no file "})
    if file:
        filename = secure_filename(file.filename)
        save_name = f"{chunkNumber}-{filename}"
        file.save(os.path.join(UPLOAD_FOLDER, save_name))
        if totalChunks ==chunkNumber:
            threading.Thread(merg_file(filename,int(totalChunks),UPLOAD_FOLDER)).start()
        return jsonify({"errno":0, "msg":"succeed "})

def merg_file(filename,totalChunks,file_path):
    chunkNumber = 1  # 分片序号
    with open(os.path.join(file_path,filename), 'wb') as target_file:  # 创建新文件
        while True:
            if chunkNumber > totalChunks:
                break
            else:
                try:
                    source_file_path = os.path.join(file_path,f"{chunkNumber}-{filename}")
                    source_file = open(source_file_path, 'rb')  # 按序打开每个分片
                    target_file.write(source_file.read())  # 读取分片内容写入新文件
                    source_file.close()
                    os.remove(source_file_path)
                except(IOError) as e:
                    print(e)
                    break
                chunkNumber += 1

@home_bp.route('/caseinfo', methods=['GET'])
def get_case_info():
    return jsonify(get_all_case_info())

@home_bp.route('/addCase', methods=['POST'])
def add_case():
    caseNmae = request.get_json()["caseNmae"]
    case = models.Case.Case(caseName=caseNmae)
    models.db.session.add(case)
    models.db.session.commit()
    return jsonify({"msg":"success"})

@home_bp.route('/delCase', methods=['POST'])
def del_case():
    pass
    # TODO
    return jsonify({"msg":"success"})
from flask import Blueprint
from flask import jsonify,request
from flask import send_file, send_from_directory
from flask_jwt import jwt_required, current_identity

from ..config import basedir
from ..models.File import File
from project import models
import threading
import os


file_bp = Blueprint('file_bp', __name__)
ROOT_UPLOAD_FOLDER = os.path.join(basedir,"temp")

@file_bp.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        chunkNumber = request.form.get("chunkNumber")
        totalChunks = request.form.get("totalChunks")
        filename = request.form.get("filename")
        describe = request.form.get("describe")
        fileOrigin = request.form.get("fileOrigin")
        fileType = request.form.get("fileType")
        fileLable = request.form.get("fileLable")
        caseID = request.form.get("caseID")
        upload_folder = os.path.join(ROOT_UPLOAD_FOLDER,str(caseID))
        if file is None:
            return jsonify({"msg":"未上传文件！"}),400
        if totalChunks == 1:
            file.save(os.path.join(upload_folder, filename))
            file1 = File(caseID=caseID,fileName=filename,fileOrigin=fileOrigin,fileType=fileType,fileLable=fileLable,fileDescribe=describe)
            models.db.session.add(file1)
            models.db.session.commit()
        else:
            file.save(os.path.join(upload_folder, f"{chunkNumber}-{filename}"))
            if totalChunks ==chunkNumber:
                threading.Thread(merg_file(filename,int(totalChunks),upload_folder)).start()
                file1 = File(caseID=caseID,fileName=filename,fileOrigin=fileOrigin,fileType=fileType,fileLable=fileLable,fileDescribe=describe)
                models.db.session.add(file1)
                models.db.session.commit()
        return jsonify({"msg":"success"})
    except Exception as err:
        return jsonify({"msg":str(err)}) ,500

@file_bp.route('/test', methods=['POST'])
def test_file():
    try:
        caseID = request.get_json()["caseID"]
        caseName = request.get_json()["caseName"]
        fileName = request.get_json()["fileName"]
        upload_folder = os.path.join(ROOT_UPLOAD_FOLDER,str(caseID))
        if not os.path.isdir(upload_folder):
            os.makedirs(upload_folder)
        else:
            if os.path.isfile(os.path.join(upload_folder,fileName)):
                return jsonify({"msg":"文件已经存在，请勿重复上传！"}) ,400
        return jsonify({"msg":"success"})
    except Exception as err:
        return jsonify({"msg":str(err)}) ,500

@file_bp.route('/search', methods=['POST'])
def search_file():
    # todo
    pass

@file_bp.route('/download/<caseID>/<filename>', methods=['POST'])
def download_file():
    # todo
    pass

def merg_file(filename,totalChunks,file_path):
    # todo
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
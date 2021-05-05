from flask import Blueprint
from flask import jsonify,request
from flask import send_file, send_from_directory, make_response
from flask_jwt import jwt_required, current_identity
from werkzeug.exceptions import HTTPException, NotFound

from ..config import basedir
from ..models.File import File
from ..models.Case import Case
from ..services.ES import search_file_in_ES,save_file
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
        caseName = request.form.get("caseName")
        upload_folder = os.path.join(ROOT_UPLOAD_FOLDER,str(caseID))
        if file is None:
            return jsonify({"msg":"未上传文件！"}),400
        if totalChunks == 1:
            file.save(os.path.join(upload_folder, filename))
            temp_file = File(caseID=caseID,fileName=filename,fileOrigin=fileOrigin,fileType=fileType,fileLable=fileLable,fileDescribe=describe).save()
            save_file(meta={'id': temp_file.id},caseName=caseName,caseID=caseID,fileName=filename,fileOrigin=fileOrigin,fileType=fileType,fileLable=fileLable,fileDescribe=describe)
        else:
            file.save(os.path.join(upload_folder, f"{chunkNumber}-{filename}"))
            if totalChunks ==chunkNumber:
                threading.Thread(merg_file(filename,int(totalChunks),upload_folder)).start()
                temp_file = File(caseID=caseID,fileName=filename,fileOrigin=fileOrigin,fileType=fileType,fileLable=fileLable,fileDescribe=describe).save()
                save_file(meta={'id': temp_file.id},caseName=caseName,caseID=caseID,fileName=filename,fileOrigin=fileOrigin,fileType=fileType,fileLable=fileLable,fileDescribe=describe)
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
    try:
        searchStr = request.get_json()["searchStr"]
        if searchStr=='':
            return jsonify(json_list=[])
        caseID = None
        if "caseID" in request.get_json():
            caseID = request.get_json()["caseID"]
        return jsonify(json_list=search_file_in_ES(searchStr,caseID))
    except Exception as err:
        return jsonify({"msg":str(err)}) ,500

@file_bp.route('/download/<caseID>/<fileName>', methods=['GET'])
def download_file(caseID,fileName):
    try:
        directory = os.path.join(ROOT_UPLOAD_FOLDER,str(caseID))
        response = make_response(send_from_directory(directory, fileName, as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(fileName.encode().decode('latin-1'))
        return response
    except HTTPException as err:
        return jsonify({"msg":"请求的文件有误"}) ,400
    except NotFound as err:
        return jsonify({"msg":"请求的文件有误"}) ,400
    except Exception as err:
        return jsonify({"msg":str(err)}) ,500

def merg_file(filename,totalChunks,file_path):
    # todo 错误控制
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
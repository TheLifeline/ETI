from flask import Blueprint
from flask import jsonify,request
from flask import send_file, send_from_directory
from flask_jwt import jwt_required, current_identity

from ..config import basedir
import threading
import os


file_bp = Blueprint('file_bp', __name__)
UPLOAD_FOLDER = os.path.join(basedir,"temp")

@file_bp.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        chunkNumber = request.form.get("chunkNumber")
        totalChunks = request.form.get("totalChunks")
        filename = request.form.get("filename")
        describe = request.form.get("describe")
        caseID = request.form.get("caseID")
        if file is None:
            return jsonify({"msg":"未上传文件！"}),400
        file.save(os.path.join(UPLOAD_FOLDER, f"{chunkNumber}-{filename}"))
        if totalChunks ==chunkNumber:
            threading.Thread(merg_file(filename,int(totalChunks),UPLOAD_FOLDER)).start()
        return jsonify({"msg":"success"})
    except Exception as err:
        return jsonify({"msg":str(err)}) ,500

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
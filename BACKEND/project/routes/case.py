from flask import Blueprint
from flask_jwt import jwt_required, current_identity
from werkzeug.utils import secure_filename
from flask import jsonify,request
from flask import send_file, send_from_directory

from ..config import basedir
from ..models.Case import get_all_case_info
from .. import models
import threading
import os


case_bp = Blueprint('case_bp', __name__)
UPLOAD_FOLDER = os.path.join(basedir,"temp")


@case_bp.route('/caseinfo', methods=['GET'])
def get_case_info():
    try:
        return jsonify(get_all_case_info())
    except Exception as err:
        return jsonify({"msg":str(err)}) ,500

@case_bp.route('/addCase', methods=['POST'])
def add_case():
    try:
        caseName = request.get_json()["caseName"]
        if caseName == "":
            return jsonify({"msg":"案例名为空！"}),400
        if models.Case.Case.query.filter_by(caseName=caseName).first() is not None:
            return jsonify({"msg":"这个案例已经存在！"}),400
        case = models.Case.Case(caseName=caseName)
        models.db.session.add(case)
        models.db.session.commit()
        return jsonify({"msg":"success"})
    except Exception as err:
        print(err)
        return jsonify({"msg":str(err)}) ,500

@case_bp.route('/delCase', methods=['POST'])
def del_case():
    pass
    # TODO
    return jsonify({"msg":"success"})
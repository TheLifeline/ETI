from flask import Blueprint
from flask_jwt import jwt_required, current_identity


home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/', methods=['GET', 'POST'])
def index():
    return "Hello World!", 200

@home_bp.route('/jwttest', methods=['GET', 'POST'])
@jwt_required()
def test():
    return "Success!", 200
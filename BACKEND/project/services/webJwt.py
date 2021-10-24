from ..models.User import User
from flask_jwt import JWT

from flask import jsonify
from collections import OrderedDict


def authenticate(username, password):
    result = User.query.filter_by(username=username, password=password).first()
    return result


def identity(payload):
    return User.query.filter_by(id=payload['identity']).scalar()


def error_callback(error):
    return jsonify(OrderedDict([
        ('status_code', error.status_code),
        ('error', error.error),
        ('msg', error.description),
    ])), error.status_code, error.headers


class webJwtServices(object):
    def __init__(self, app):
        self.jwt = JWT(app, authenticate, identity)
        self.jwt.jwt_error_callback = error_callback

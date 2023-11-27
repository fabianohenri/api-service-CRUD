from flask import request
from flask_restx import Resource

from api.login_api_MIGRARPARAAUTH import UserLogin


class UserLoginApi(Resource):

    @staticmethod
    def post():
        dados = request.get_json(silent=True)
        return UserLogin.login(dados['email'], dados['password'])

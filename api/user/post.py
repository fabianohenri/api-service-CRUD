import json

from flask import request, Response
from flask_restx import Resource

from controller.user_controller import UsersController
from util.logging_format import LoggingFormat
from controller.validate_data_controller import VerifyData


class UserApiPost(Resource):

    # @auth.login_required
    def post(self):
        """
        Cadastro de novo usuário.
        :parameter: email = string
        :parameter: password = string
        :return: token = string
        """
        dados = request.get_json(silent=True)
        # Caso não haja dados, será retornado erro.
        if not dados:
            response = {"message": "Error ao gravar no banco."}
            LoggingFormat.format(request.method + " " + request.path + " - Resposta: " +
                                 str(response['message']), "Info")
            return Response(json.dumps(response), status=404, mimetype="application/json")

        # Varificando se tem name
        verify = VerifyData().verify(parametro='name', texto=True)
        if not verify:
            response = {"message": "Parametro 'name' inválido ou inexistente"}
            LoggingFormat.format(request.method + " " + request.path + " - Resposta: " +
                                 str(response['message']), "Error")
            return Response(request.method + " " + json.dumps(response), status=404, mimetype="application/json")

        # Verificando se tem 'E-mail'.
        verify = VerifyData().verify(parametro='email', email=True)
        if not verify:
            response = {"message": "Parametro 'email' inválido ou inexistente"}
            LoggingFormat.format(request.method + " " + request.path + " - Resposta: " +
                                 str(response['message']), "Error")
            return Response(json.dumps(response), status=404, mimetype="application/json")

        # Veriicando se tem senha
        if not dados['password']:
            response = {"message": "Parametro 'password' inválido ou inexistente"}
            LoggingFormat.format(request.method + " " + request.path + " - Resposta: " +
                                 str(response['message']), "Error")
            return Response(json.dumps(response), status=404, mimetype="application/json")

        # Ao salvar a senha preciso criptografar ela.

        # Após feita toda a verificação e passado, chamo o post
        response = UsersController().post_users()
        return response

import json

from flask import request, Response
from flask_restx import Resource

from controller.user_controller import UsersController
from util.logging_format import LoggingFormat
from controller.validate_data_controller import VerifyData


class UserApiPut(Resource):

    # @auth.login_required
    def put(self):
        """
        Alteração de um usuário
        :parameter: id = int
        :parameter: name = string
        :parameter: email = string
        :parameter: password = string
        :return:
        """

        dados = request.get_json(silent=True)
        # Caso não haja dados, será retornado erro.
        if not dados:
            response = {"message": "Error ao alterar dados no banco."}
            LoggingFormat.format(request.method + " " + request.path + " - Resposta: " +
                                 str(response['message']), "Info")
            return Response(json.dumps(response), status=404, mimetype="application/json")

        # Verificando se existe o parâmetro id no json e valida
        verify = VerifyData().verify(parametro='id', inteiro=True)
        if not verify:
            response = {"message": "Valor de id inválido ou inxistente."}
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

        # Verificando se tem E-mail
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

        # Chamando a alteração após validar os dados informados.
        response = UsersController().put_user()

        return response


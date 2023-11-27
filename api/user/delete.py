import json

from flask import request, Response
from flask_restx import Resource

from controller.user_controller import UsersController
from resources.authentication import auth
from util.logging_format import LoggingFormat
from util.utils import VerifyData


class UserApiDelete(Resource):

    # @auth.login_required
    def delete(self, user_id):
        """
        Deleção de um usuáro
        :parameter user_id: 'Int'
        :return:
        """

        # Caso não haja dados, será retornado erro.
        if not user_id:
            response = {"message": "Error ao alterar dados no banco."}
            LoggingFormat.format(request.method + " " + request.path + " - Resposta: " +
                                 str(response['message']), "Info")
            return Response(json.dumps(response), status=404, mimetype="application/json")

        verify = VerifyData().verify_id(user_id)
        if not verify:
            response = {"message": "Valor de id inválido ou inxistente."}
            LoggingFormat.format(request.method + " " + request.path + " - Resposta: " +
                                 str(response['message']), "Info")
            return Response(json.dumps(response), status=404, mimetype="application/json")

        response = UsersController().delete_user(user_id)

        LoggingFormat.format(request.method + " " + request.path + " - Resposta: " +
                             str(response), "Info")
        return response

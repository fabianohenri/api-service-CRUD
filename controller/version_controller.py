import json

from flask import request, Response
from sqlalchemy.exc import OperationalError

from models.version_model import VersionModel
from util.config import db
from util.logging_format import LoggingFormat
from controller.validate_data_controller import VerifyData


class VersionController:
    def __init__(self):
        self.__dados = request.get_json(silent=True)

    @staticmethod
    def get_version():
        try:
            response = VersionModel.query.filter_by(id="1").first()
        except OperationalError:
            return None

        return response

    def update_version(self):
        db_version = VersionModel.query.filter_by(id="1").first()
        # Validando se obteve retorno da pesquisa

        # Validar se teve existe versão no parametro.
        if 'version' not in self.__dados:
            message = "Parametro version não inválido ou inexistente."
            response = {"message": message}
            return Response(json.dumps(response), status=404, mimetype="application/json")

        virify = VerifyData().verify(parametro="version", version=True)
        if not virify:
            message = "Versão informada não é valida. Ex: 1.0"
            response = {"message": message}
            LoggingFormat.format(request.method + " " + request.path + " - Resposta: " +
                                 str(response['message']), "Info")
            return Response(json.dumps(response), status=404, mimetype="application/json")

        try:
            # Verificando o valor da porta
            db_version.version = self.__dados['version']
            db.session.commit()
            message = f"Versão do banco atualizada para a versão: {self.__dados['version']}"
            response = {"message": message}
            LoggingFormat.format(request.method + " " + request.path + " - Resposta: " +
                                 str(response['message']), "Info")
            return Response(json.dumps(response), status=200, mimetype="application/json")
        except ValueError as e:
            response = {"message": "Erro ao atualizar a versão do sistema." + str(e)}
            return Response(json.dumps(response), status=404, mimetype="application/json")

import json
from hmac import compare_digest as compare_hash

import cryptocode
from flask import request, Response

from controller.variables_db import VariablesDataBase
from models.person_model import PersonModel
from util.logging_format import LoggingFormat


class UserLogin(VariablesDataBase):

    def login(self, recive_email, recive_password):
        # pesquisa o usuário
        try:
            message = f"Tentativa de login com o email: {recive_email}"
            LoggingFormat.format(message, "Info")
            data = PersonModel.query.filter_by(email=recive_email).first()
            if not data:
                message = f"Email {recive_email}, não encontrado na base de dados. Tente novamente"
                response = {"message": message}
                LoggingFormat.format(request.method + " " + request.path + "  - Resposta: " +
                                     str(response), "Info")
                return Response(json.dumps(response), status=401, mimetype="application/json")
            else:
                message = "Email encontrado. Validando senha."
                response = {"message": message}
                LoggingFormat.format(request.method + " " + request.path + "  - Resposta: " +
                                     str(response), "Info")

        except Exception as e:
            message = "Não foi possível efetuar a consulta do banco de dados." + str(e)
            response = {"message": message}
            LoggingFormat.format(request.method + " " + request.path + "  - Resposta: " +
                                 str(response), "Info")
            return Response(json.dumps(response), status=404, mimetype="application/json")

        # Desincripotografa o password salvo no banco.
        save_pass = cryptocode.decrypt(data.password, self.vars_db()["KEY_HASH"])

        # Compara os valores informados com o coletado no banco
        valid = compare_hash(save_pass, recive_password)

        if valid:
            message = f"Usuário: '{data.name}' logado!"
            response = {"id": data.id,
                        "email": data.email,
                        "name": data.name,
                        "message": message}
            LoggingFormat.format(request.method + " " + request.path + "  - Resposta: " +
                                 str(response), "Info")
            return Response(json.dumps(response), status=200, mimetype="application/json")
        else:
            message = f"Senha informado não compativel com a ultima salva. Tente novamente."
            response = {"message": message}
            LoggingFormat.format(request.method + " " + request.path + "  - Resposta: " +
                                 str(response), "Info")
        return Response(json.dumps(response), status=401, mimetype="application/json")
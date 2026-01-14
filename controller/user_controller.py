import json

import cryptocode
from flask import request, Response
from sqlalchemy import exc
from sqlalchemy.exc import OperationalError

from controller.variables_db import VariablesDataBase
from models.person_model import PersonModel
from util.config import db
from util.logging_format import LoggingFormat


class UsersController(VariablesDataBase):
    def __init__(self):
        self.__dados = request.get_json(silent=True)

    @staticmethod
    def get_user_by_id(user_id=None):
        # Valida se existe o id na requisição.
        if user_id is not None:
            try:
                data = PersonModel.query.filter_by(id=user_id).first()
            except Exception as e:
                message = "Não foi possível efetuar a consulta do banco de dados." + str(e)
                response = {"is_exist": False, "message": message}
                LoggingFormat.format(request.method + " " + request.path + "  - Resposta: " +
                                     str(response), "Info")
                return Response(json.dumps(response), status=404, mimetype="application/json")

            # Valida se existe dados a retornar ou não.
            if data:
                response = {"is_exist": True, "id": data.id, "name": data.name,
                            "email": data.email, "password": data.password}
                LoggingFormat.format(request.method + " " + request.path + "  - Resposta: " +
                                     str(response), "Info")
                return Response(json.dumps(response), status=200, mimetype="application/json")
            else:
                response = {"is_exist": False, "message": "Id não encontrada"}
                LoggingFormat.format(request.method + " " + request.path + " - Resposta: " +
                                     str(response), "Info")
                return Response(json.dumps(response), status=406, mimetype="application/json")
        else:
            response = {"is_exist": False, "message": "O parametro user_id não informado."}
            LoggingFormat.format(request.method + " " + request.path + " - Resposta: " +
                                 str(response), "Info")
            return Response(json.dumps(response), status=404, mimetype="application/json")

    @staticmethod
    def get_user_by_email(user_email=None):
        # Valida se existe o id na requisição.
        if user_email is not None:
            try:
                data = PersonModel.query.filter_by(email=user_email).first()
            except Exception as e:
                message = "Não foi possível efetuar a consulta do banco de dados." + str(e)
                response = {"is_exist": False, "message": message}
                LoggingFormat.format(request.method + " " + request.path + "  - Resposta: " +
                                     str(response), "Info")
                return Response(json.dumps(response), status=404, mimetype="application/json")

            # Valida se existe dados a retornar ou não.
            if data:
                response = {"is_exist": True, "id": data.id, "name": data.name, "email": data.email, "password": data.password}
                LoggingFormat.format(request.method + " " + request.path + "  - Resposta: " +
                                     str(response), "Info")
                return Response(json.dumps(response), status=200, mimetype="application/json")
            else:
                response = {"is_exist": False, "message": "Email não encontrada"}
                LoggingFormat.format(request.method + " " + request.path + " - Resposta: " +
                                     str(response), "Info")
                return Response(json.dumps(response), status=406, mimetype="application/json")
        else:
            response = {"is_exist": False, "message": "O parametro user_email não informado."}
            LoggingFormat.format(request.method + " " + request.path + " - Resposta: " +
                                 str(response), "Info")
            return Response(json.dumps(response), status=404, mimetype="application/json")

    @staticmethod
    def get_all_users():
        try:
            response_list = PersonModel.query.all()
        except OperationalError:
            message = "Não foi possível efetuar a consulta do banco de dados."
            response = {"is_exist": False, "message": message}
            LoggingFormat.format(request.method + " " + request.path + " - Resposta: " +
                                 str(response), "Info")
            return Response(json.dumps(response), status=404, mimetype="application/json")

        lista = {}
        for i in response_list:
            lista[f'{i}'] = {"id": i.id, "name": i.name, "email": i.email}

        LoggingFormat.format(request.method + " " + request.path + "- Resposta: " +
                             str(lista), "Info")
        return Response(json.dumps(lista), status=200, mimetype="application/json")

    def post_users(self):
        # Verificar se existe o parâmetro name no json
        try:
            vars = self.vars_db()
            password = cryptocode.encrypt(self.__dados['password'], vars["KEY_HASH"])
            new_user = PersonModel(name=self.__dados['name'],
                                   email=self.__dados['email'],
                                   password=password)
            db.session.add(new_user)
            db.session.commit()
            response = {"messege": f"O usuário {new_user.name} salvo com sucesso!"}
            LoggingFormat.format(request.method + " " + request.path + " " + str(self.__dados) + " - Resposta: " +
                                 str(response), "Info")
            return Response(json.dumps(response), status=200, mimetype="application/json")
        except exc.IntegrityError:
            # Se ao salvar já existir os dados, não aceita duplicação de dados.
            db.session.rollback()
            response = {"message": f"O nome: '{self.__dados['name']}' e/ou email: '{self.__dados['email']},"
                                   f" já existente na base de dados! "}
            LoggingFormat.format(request.method + " " + request.path + " " + str(self.__dados) + " - Resposta: " +
                                 str(response), "Info")
            return Response(json.dumps(response), status=404, mimetype="application/json")

        except exc.DataError:
            # Se o tamanho do dados for maior que o valor da tabela.
            db.session.rollback()
            message = "Valor informado nos campos, maior que a capacidade permitida."
            response = {"message": message}
            LoggingFormat.format(request.method + " " + request.path + " " + str(self.__dados) + " - Resposta: " +
                                 str(response), "Info")
            return Response(json.dumps(response), status=404, mimetype="application/json")
        except KeyError as e:
            db.session.rollback()
            message = "Um ou mais parametros informado não" + str(e)
            response = {"message": message}
            LoggingFormat.format(request.method + " " + request.path + " " + str(self.__dados) + " - Resposta: " +
                                 str(response), "Info")
            return Response(json.dumps(response), status=404, mimetype="application/json")

    def put_user(self):
        user = PersonModel.query.filter_by(id=self.__dados['id']).first()
        # Validando se obteve retorno da pesquisa
        if user:
            try:
                # Verificando o valor da porta
                user.name = self.__dados['name']
                user.email = self.__dados['email']
                user.password = self.__dados['password']
                db.session.commit()
                response = {"message": "Atualizado com sucesso com sucesso!"}
                LoggingFormat.format(request.method + " " + request.path + " " + str(self.__dados) + " - Resposta: " +
                                     str(response), "Info")
                return Response(json.dumps(response), status=200, mimetype="application/json")
            except ValueError as e:
                db.session.rollback()
                message = "Erro ao atualizar o nome usuário." + str(e)
                LoggingFormat.format(message, "Error")
                response = {"message": message}
                LoggingFormat.format(request.method + " " + request.path + " " + str(self.__dados) + " - Resposta: " +
                                     str(response), "Error")
                return Response(json.dumps(response), status=404, mimetype="application/json")
            except exc.IntegrityError:
                db.session.rollback()
                message = "Email ou Nome já existente no banco de dados."
                response = {"message": message}
                LoggingFormat.format(request.method + " " + request.path + " " + str(self.__dados) + " - Resposta: " +
                                     str(response), "Error")
                return Response(json.dumps(response), status=404, mimetype="application/json")
            except Exception as e:
                db.session.rollback()
                message = "Erro ao atualizar dados do usuário." + str(e)
                response = {"message": message}
                LoggingFormat.format(request.method + " " + request.path + " " + str(self.__dados) + " - Resposta: " +
                                     str(response), "Error")
                return Response(json.dumps(response), status=404, mimetype="application/json")
        else:
            message = "Usuário inválido."
            response = {"message": message}
            LoggingFormat.format(request.method + " " + request.path + " " + str(self.__dados) + " - Resposta: " +
                                 str(response), "Error")
            return Response(json.dumps(response), status=404, mimetype="application/json")

    def delete_user(self, user_id):
        user = PersonModel.query.filter_by(id=user_id).first()
        if user:
            try:
                db.session.delete(user)
                db.session.commit()
                response = {"message": f"O usuário '{user_id}' deletado com sucesso!"}
                LoggingFormat.format(request.method + " " + request.path + " " + str(self.__dados) + " - Resposta: " +
                                     str(response), "Info")
                return Response(json.dumps(response), status=200, mimetype="application/json")
            except exc.IntegrityError:
                message = f"Erro ao tentar excluír o usuário de id: {user_id}. "
                response = {"message": message}
                LoggingFormat.format(request.method + " " + request.path + " " + str(self.__dados) + " - Resposta: " +
                                     str(response), "Error")
                return Response(json.dumps(response), status=404, mimetype="application/json")
            except Exception as e:
                message = f"Errro ao tentar deletar o usuário {user_id}. Error: " + str(e)
                response = {"message": message}
            LoggingFormat.format(request.method + " " + request.path + " " + str(self.__dados) + " - Resposta: " +
                                 str(response), "Error")
            return Response(json.dumps(response), status=404, mimetype="application/json")
        else:
            message = f"Id {user_id}, não encontrado na base de dados para efetuar a exclusão. "
            response = {"message": message}
            LoggingFormat.format(request.method + " " + request.path + " " + str(self.__dados) + " - Resposta: " +
                                 str(response), "Alert")
            return Response(json.dumps(response), status=206, mimetype="application/json")


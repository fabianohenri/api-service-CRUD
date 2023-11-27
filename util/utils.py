import re

from flask import request


class VerifyData:
    """ Classe para validar o valor passado. Nela consigo determinar o tipo do arquiv que quero e o parametro que
            quero verificar para validação
        :param = campo que vou pegar no json
        :tipo = tipo de dados(string ou int)
    """

    def __init__(self):
        self.__dados = request.get_json(silent=True)

    @staticmethod
    def verify_id(params_id):
        try:
            valor = int(params_id)
            return True
        except:
            return False

    def verify(self, parametro, inteiro=False, texto=False, email=False, version=False):
        # Verificar se existe o parametro
        try:
            params = self.__dados[f'{parametro}']
            if not params:
                return False
        except:
            response = False
            return response

        # Verifica se é do tipo que eu precisa
        if inteiro:
            try:
                valor = int(self.__dados[f'{parametro}'])
                return True
            except:
                return False

        # Verificando se o valor do dado é negativo
        if inteiro and int(self.__dados[f'{parametro}']) <= 0:
            return False

        if texto:
            try:
                valor = int(self.__dados[f'{parametro}'])
                return False
            except:
                return True

        if email:
            try:
                regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
                if re.fullmatch(regex, self.__dados[f'{parametro}']):
                    return True
            except:
                return False

        if version:
            try:
                ver_float = float(self.__dados[f'{parametro}'])
                return True
            except:
                return False

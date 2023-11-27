#!/usr/bin/python
# -*- coding: utf-8 -*-
from waitress import serve

from controller.check_db_controller import CheckDB
from resources.routes import initialize_routes
from util.config import *

# Iniciar rotas
initialize_routes(api)

# Executar aplicacao
if __name__ == '__main__':

    # Validando se o banco está de pé antes de iniciar a api.
    if not CheckDB.validate():
        exit(1)

    serve(app, host='0.0.0.0', port=65500)



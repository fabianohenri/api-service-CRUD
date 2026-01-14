"""Arquivo com as configurações necessárias para o uso do SQLALCHEMY"""
import logging

from flask import Flask, Blueprint
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

from controller.variables_db import VariablesDataBase

# Log em debug
logging.basicConfig(level=logging.INFO, filemode='w',
                    format='%(asctime)s - %(threadName)s - %(''message)s')


VERSION = ''

app = Flask(__name__)
CORS(app)
blueprint = Blueprint('api', __name__)

api = Api(app, title='Api ms-infra-users',
          version='0.0',
          default="Users",
          default_label="",
          description='Api para controle de usuários',
          doc="/doc",
          prefix=f'/')


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = VariablesDataBase().connect_string()
db = SQLAlchemy(app)



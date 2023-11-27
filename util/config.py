"""Arquivo com as configurações necessárias para o uso do SQLALCHEMY"""
import logging
import os

from flask import Flask, Blueprint
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

from util.logging_format import LoggingFormat

# Log em debug
logging.basicConfig(level=logging.INFO, filemode='w',
                    format='%(asctime)s - %(threadName)s - %(''message)s')

# Local
from dotenv import load_dotenv
load_dotenv(".env", verbose=False)

# Produção
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
KEY_HASH = os.getenv('KEY_HASH')

db_string_connection = "postgresql://" + DB_USER + ":" + DB_PASS + "@" + DB_HOST +\
                                        ":" + DB_PORT + "/" + DB_NAME

# LoggingFormat.format(f"Api Online - v {VERSION}", "Success")

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
app.config['SQLALCHEMY_DATABASE_URI'] = db_string_connection
db = SQLAlchemy(app)



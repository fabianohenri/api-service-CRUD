import json

from flask import Response
from flask_restx import Resource

from controller.version_controller import VersionController


class VersionApiPut(Resource):

    @staticmethod
    def put():
        return VersionController().update_version()

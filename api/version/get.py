import json

from flask import Response
from flask_restx import Resource, Namespace

from controller.version_controller import VersionController

api = Namespace('Version', description='Work in Progress - To be deleted')


class VersionApiGet(Resource):

    @staticmethod
    def get():
        return Response(json.dumps(
                        {"version": VersionController.get_version().version}),
                        status=200,
                        mimetype="application/json")

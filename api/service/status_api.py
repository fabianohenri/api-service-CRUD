import json

from flask import Response
from flask_restx import Resource

from util.logging_format import LoggingFormat


class StatusApi(Resource):

    @staticmethod
    def get():
        LoggingFormat.format("Api respondendo", "Success")
        return Response(json.dumps(
                        {"message": "Api respondendo"}),
                        status=200,
                        mimetype="application/json")

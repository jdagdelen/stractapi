from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from stract.api import status


class Test(Resource):
    """
    A quick test for the API to see if it's running.
    """

    def get(self, message):
        """ Gets data from the server."""
        # Do something
        response = {
            "message": message
        }
        response = jsonify(response)
        response.status_code = status.HTTP_200_OK
        return response
from flask_restful import Resource
from stract.api import status

class Template(Resource):
    """
    A template for a Stract resource.
    """

    def get(self):
        """ Gets data from the server."""
        # Do something
        data = []
        return_status = status.HTTP_200_OK
        # return something and the appropriate status
        return data, status.HTTP_501_NOT_IMPLEMENTED
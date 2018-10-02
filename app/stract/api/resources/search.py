from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from stract.api import status
from stract.api.schemas import SearchSchema, AbstractSchema
from matstract.models.search import MatstractSearch
from matstract.models.authentication import require_api_key
from warnings import warn


class Search(Resource):
    """
    The Search resource. Allows user to request abstracts that fit a certain set of criteria including text seraches
    and filtering by material, properties, etc.

    Takes in a json of criteria in the form:

        {
            "query": {
                "text": "",
                "material": {"positive": [], "negative": []},
                "property": {"positive": [], "negative": []},
                "application": {"positive": [], "negative": []},
                "descriptor": {"positive": [], "negative": []},
                "characterization": {"positive": [], "negative": []},
                "synthesis": {"positive": [], "negative": []},
                "phase": {"positive": [], "negative": []},
                "author": {"positive": [], "negative": []},
                "journal": {"positive": [], "negative": []},
                "year": {"positive": [], "negative": []},
                "publisher": {"positive": [], "negative": []},
                "keyword": {"positive": [], "negative": []},
                },
            "limit": 100
        }

    """

    input_schema = SearchSchema()
    abstract_shema = AbstractSchema()
    abstracts_shema = AbstractSchema(many=True)

    def _prepare_response(self, query, limit):
        try:
            search = MatstractSearch.from_dict(query, max_results=limit)
            response = {
                "valid_response": True,
                "response": self.abstracts_shema.dump(search.results),
                "num_results": len(search.results)
            }
            code = status.HTTP_200_OK
        except AttributeError:
            response = {
                'valid_response': False,
                'error': 'Bad criteria.'
            }
            code = status.HTTP_400_BAD_REQUEST
        response = jsonify(response)
        response.status_code = code
        return response

    @require_api_key
    def get(self, query, limit=1000):
        return self._prepare_response(query, limit)

    @require_api_key
    def post(self):
        # Validate and deserialize input
        json_data = request.get_json()
        try:
            query = self.input_schema.load(json_data['query']).data
            limit = json_data['limit']
        except ValidationError as err:
            return jsonify(err.messages), status.HTTP_400_BAD_REQUEST

        return self._prepare_response(query, limit)


class MoreLikeThis(Resource):
    """
    The MoreLikeThis resource. Allows user to request abstracts that are similar to a piece of text
    and prioritize by material, properties, etc. Basically a text-first version of search that doesn't
    restrict results too strictly by other fields.
    """

    input_schema = SearchSchema()
    abstract_shema = AbstractSchema()
    abstracts_shema = AbstractSchema(many=True)

    def _prepare_response(self, query, limit):
        try:
            warn("This is not implemented in Matstract yet. Returning normal search results instead.")
            search = MatstractSearch.from_dict(query, max_results=limit)
            response = {
                "valid_response": True,
                "warning": "This is not implemented in Matstract yet. Returning normal search results instead.",
                "response": self.abstracts_shema.dump(search.results)
            }
            code = status.HTTP_200_OK
        except AttributeError:
            response = {
                'valid_response': False,
                'error': 'Bad criteria.'
            }
            code = status.HTTP_400_BAD_REQUEST
        response = jsonify(response)
        response.status_code = code
        return response

    def get(self, query, limit=1000):
        return self._prepare_response(query, limit)

    def post(self):
        # Validate and deserialize input
        json_data = request.get_json()
        try:
            query = self.input_schema.load(json_data['query']).data
            limit = json_data['limit']
        except ValidationError as err:
            return jsonify(err.messages), status.HTTP_400_BAD_REQUEST

        return self._prepare_response(query, limit)

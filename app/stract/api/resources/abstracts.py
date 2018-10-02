from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from stract.api import status
from stract.api.schemas import EntryRequestSchema, AbstractSchema
from matstract.models.database import AtlasConnection
from matstract.models.authentication import require_api_key
from bson import ObjectId

class Abstracts(Resource):
    """
    The Abstracts resource. Allows user to request abstracts using their ids and specify the fields to be returned.
    """
    input_schema = EntryRequestSchema()
    DB = AtlasConnection()
    get_type = {'id': DB.get_documents_by_id,
                'doi': DB.get_documents_by_doi}
    abstract_shema = AbstractSchema()
    abstracts_shema = AbstractSchema(many=True)

    # def abort_if_abstract_doesnt_exist(self, ids):
    #     # If id not found in MongoDB
    #     missing = []
    #     for id in ids:
    #         if id not in atlas:
    #             missing.append(id)
    #     if len(missing):
    #         abort(status.HTTP_404_NOT_FOUND, message="Cannot find Abstract for id(s) {}".format(missing))

    def _prepare_response(self, id, fields, id_type):
        id = id.split(',')
        if id_type == 'id' or id_type == 'doi':
            print(id)
            response = {
                "valid_response": True,
                "response": self.get_type[id_type](id)
            }
            code = status.HTTP_200_OK

        else:
            response = {
                "valid_response": False,
                "error": "Invalid id_type. Please use either 'doi' or 'id'.",
            }
            code = status.HTTP_400_BAD_REQUEST
        response = jsonify(response)
        response.status_code = code
        return response

    @require_api_key
    def get(self, id, fields=None, id_type='doi'):
        if fields == None:
            fields = ['title', 'authors', 'journal', 'doi', 'abstract']
        return self._prepare_response(id, fields, id_type)

    @require_api_key
    def post(self):
        try:
            json_data = request.get_json()
            # Validate input
            data = self.input_schema.load(json_data).data
            id = data['id']
            fields = data['fields']
            id_type = data.get('id_type', 'doi')
            return self._prepare_response(id, fields, id_type)
        except ValidationError as err:
            return jsonify(err.messages), status.HTTP_400_BAD_REQUEST

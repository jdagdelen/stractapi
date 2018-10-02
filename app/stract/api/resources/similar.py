import numpy as np
from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
import marshmallow.fields as fields
from flask_marshmallow.fields import URLFor
from stract.api import status
from matstract.models.similar_materials import SimilarMaterials
from matstract.models.authentication import require_api_key


class Similar(Resource):
    SM = SimilarMaterials()

    @require_api_key
    def get(self, material):
        try:
            if material is None:
                raise ValidationError("Must supply a material!")
            cutoff = request.args.get('cutoff', None)
            sm = SimilarMaterials()
            # if cutoff is None:
            #     return jsonify(sm.get_similar_mats(material))
            # else:
            #     return jsonify(sm.get_similar_mats(material, cutoff))
            response = {
                "valid_response": True,
                "response": sm.get_similar_mats(material)
            }
            status_code = status.HTTP_200_OK
        except:
            response = {
                "valid_response": False,
                "error": "Something went wrong..."
            }
            status_code = status.HTTP_400_BAD_REQUEST
        response = jsonify(response)
        response.status_code = status_code
        return response

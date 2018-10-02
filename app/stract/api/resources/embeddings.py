import numpy as np
from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
import marshmallow.fields as fields
from flask_marshmallow.fields import URLFor
from stract.api import status
from stract.api.schemas import EmbeddingSchema
from matstract.models.word_embeddings import EmbeddingEngine, Embedding
from matstract.models.authentication import require_api_key


class EmbeddingResource(Resource):
    EE = EmbeddingEngine()
    embedding_schema = EmbeddingSchema()
    embeddings_schema = EmbeddingSchema(many=True)

    def _prepare_response(self, wordphrases):
        try:
            embeddings = []
            for wp in wordphrases:
                compound = False
                embedding = Embedding(wp, '', self.EE.get_word_vector(wp), compound=False)
                if " " in wp and embedding.embedding is None:
                    embeddings.append(Embedding(wp, '', self.EE.get_word_vector(wp), compound=True))
                else:
                    embeddings.append(embedding)
            response = {
                "valid_response": True,
                "response": self.embeddings_schema.dump(embeddings)
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

    @require_api_key
    def get(self, wordphrase):
        wps = wordphrase.split(',')
        return self._prepare_response(wps)

    @require_api_key
    def post(self):
        json_data = request.get_json(force=True)
        print(json_data, "look")
        try:
            wordphrases = json_data["wordphrase"]
            wps = wordphrases.split(',')
            return self._prepare_response(wps)

        except KeyError as err:
            response = {
                "valid_response": False,
                "error": "Provided json file does not contain wordphrases."
            }
            response = jsonify(response)
            response.status_code = status.HTTP_400_BAD_REQUEST
            return response


class EmbeddingList(Resource):
    EE = EmbeddingEngine()
    embedding_schema = EmbeddingSchema()
    embeddings_schema = EmbeddingSchema(many=True)

    def _prepare_response(self, wordphrases):
        try:
            embeddings = []
            for wp in wordphrases:
                print(wp)
                embedding = Embedding(wp, '', self.EE.get_word_vector(wp), compound=False)
                print(embedding)
                if " " in wp and embedding.embedding is None:
                    embeddings.append(Embedding(wp, '', self.EE.get_word_vector(wp), compound=True))
                else:
                    embeddings.append(embedding)
            response = {
                "valid_response": True,
                "response": self.embeddings_schema.dump(embeddings)
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

    @require_api_key
    def post(self):
        json_data = request.get_json(force=True)
        try:
            wordphrases = json_data["wordphrase"]
            return self._prepare_response(wordphrases)

        except KeyError as err:
            response = {
                "valid_response": False,
                "error": "Provided json file does not contain wordphrases."
            }
            response = jsonify(response)
            response.status_code = status.HTTP_400_BAD_REQUEST
            return response


class Synonyms(Resource):
    EE = EmbeddingEngine()

    @require_api_key
    def get(self, wordphrase, top_k=8):
        try:

            response = {
                "valid_response": True,
                "response": {
                    'original_wordphrase': wordphrase,
                    'synonyms': self.EE.close_words(wordphrase, top_k)
                }
            }
            status_code = status.HTTP_200_OK
        except:
            response = {
                "valid_response": False,
                "error": "Could not get synonyms."
            }
            status_code = status.HTTP_400_BAD_REQUEST
        response = jsonify(response)
        response.status_code = status_code
        return response

# TODO: Make MatSearch into something more general (i.e. give X, get Y=(named entity type))

class MatSearch(Resource):
    EE = EmbeddingEngine()

    @require_api_key
    def get(self, wordphrase, top_k=100):
        try:

            response = {
                "valid_response": True,
                "response": {
                    'original_wordphrase': wordphrase,
                    'materials': self.EE.find_similar_materials(wordphrase, min_count=top_k)
                }
            }
            status_code = status.HTTP_200_OK
        except:
            response = {
                "valid_response": False,
                "error": "Could not get synonyms."
            }
            status_code = status.HTTP_400_BAD_REQUEST
        response = jsonify(response)
        response.status_code = status_code
        return response

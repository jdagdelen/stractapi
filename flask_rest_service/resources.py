import json
from flask import request, abort
from flask_restful import Resource
# from flask_rest_service import app, api, mongo, es
from bson.objectid import ObjectId
from flask_rest_service import app, api
from matstract.models.word_embeddings import EmbeddingEngine, number_to_substring


def search(search_text):
    if search_text is not None and search_text != "":
        ee = EmbeddingEngine()

        # the positive word vectors
        sentence = ee.phraser[ee.dp.process_sentence(search_text.split())][0]
        print("sentence:", sentence)
        # the negative word vectors
        n_sentence = None

        # finding materials sorted by similarity
        most_similar = ee.find_similar_materials(
            sentence=sentence,
            n_sentence=n_sentence,
            min_count=15,
            use_output_emb= False if ee.dp.is_simple_formula(sentence[0]) else True)

        # return top 50 results
        matlist = ee.most_common_form(most_similar[:100])
        material_names, material_scores, material_counts, _ = zip(*matlist)
        print("results:", material_names)
        return material_names
    else:
        return None

class Phrase(Resource):
    def get(self, phrase):
        results = search(phrase)
        print(results)
        return [r for r in results] if results else None


class Root(Resource):
    def get(self):
        return {
            'status': 'OK',
        }

api.add_resource(Root, '/')
api.add_resource(Phrase, '/search/<string:phrase>')
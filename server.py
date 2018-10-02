import json
from flask import Flask, request, jsonify
from flask_restful import Api
from stract.api.models import *
from matstract.models.database import AtlasConnection
from matstract.models.word_embeddings import EmbeddingEngine
from matstract.models.cluster_plot import ClusterPlot
from matstract.models.search import MatstractSearch
from matstract.models.similar_materials import SimilarMaterials
from matstract.models.errors import *
from stract.api.resources.search import Search
from stract.api.resources.test import Test
from stract.api.resources.embeddings import EmbeddingResource, EmbeddingList

db = AtlasConnection()
ee = EmbeddingEngine()

app = Flask(__name__)
api = Api(app)

api.add_resource(Test, '/test/<string:message>')
api.add_resource(Search, '/search')
api.add_resource(EmbeddingResource, '/embeddings/<wordphrase>')
api.add_resource(EmbeddingList, '/embeddings')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_restful import Api
from stract.api.resources.search import Search
from stract.api.resources.test import Test
from stract.api.resources.embeddings import EmbeddingResource, EmbeddingList, MatSearch
from stract.api.resources.similar import Similar
from stract.api.resources.abstracts import Abstracts

app = Flask(__name__)
api = Api(app)

api.add_resource(Test, '/test/<string:message>')
api.add_resource(Search, '/search')
api.add_resource(EmbeddingResource, '/embeddings/<string:wordphrase>')
api.add_resource(EmbeddingList, '/embeddings')
api.add_resource(MatSearch, '/embeddings/matsearch/<string:wordphrase>')
api.add_resource(Similar, '/materials/similar/<string:material>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

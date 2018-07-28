from flask import Flask
from flask_restful import Api
from flask_marshmallow import Marshmallow
from stract.api.resources import *

app = Flask(__name__)
api = Api(app)
ma = Marshmallow(app)

api.add_resource(Abstracts, '/abstracts/<string:abstract_id>', endpoint='abstracts_endpoint')
api.add_resource(Search, '/api/search/')
api.add_resource(Embeddings, '/api/embeddings/<string:wordphrase>', endpoint='embeddings_endpoint')
api.add_resource(CompoundEmbeddings, '/api/embeddings/compound/<string:wordphrase>',
                       endpoint='compound_embeddings_endpoint')
api.add_resource(ClusterPlot, '/api/plots/cluster/')
api.add_resource(TrendsPlot, '/api/plots/trends/')
api.add_resource(Test, '/api/test/<string:message>')

if __name__ == '__main__':
    app.run(debug=True)

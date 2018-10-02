from flask import Flask, request, jsonify
from flask_restful import Api
from stract.api.models import *
from matstract.models.database import AtlasConnection
from matstract.models.word_embeddings import EmbeddingEngine
from matstract.models.cluster_plot import ClusterPlot
from matstract.models.search import Search
from matstract.models.similar_materials import SimilarMaterials
from matstract.models.errors import *
import json
db = AtlasConnection()
ee = EmbeddingEngine()

app = Flask(__name__)
api = Api(app)

cp = ClusterPlot()


# endpoint to test
@app.route('/api/test/<message>', methods=["Get"])
def test_api(message):
    messages = message.split(',')
    test = [APITest(message) for message in messages]
    return TestSchema(many=True).jsonify(test)


# endpoint to abstracts
@app.route('/api/abstracts/<abstract_id>', methods=["GET"])
def retrieve_abstracts(abstract_id):
    abstract_ids = abstract_id.split(',')
    entries = db.get_documents_by_id(abstract_ids)
    abstracts = [Abstract(**entry, id=str(entry["_id"])) for entry in entries]
    return AbstractSchema(many=True).jsonify(abstracts)


# endpoint to search
@app.route('/api/search', methods=['POST'])
def execute_search():
    o = request._get_current_object()
    if len(o.data) is 0:
        return AbstractSchema(many=True).jsonify([])
    content = json.loads(o.data)
    search = Search.from_dict(content["query"], max_results=content["limit"])
    for entry in search.results:
        entry["_id"] = str(entry["_id"])
    return AbstractSchema(many=True).jsonify(search.results)


# endpoint to more like this searches
@app.route('/api/morelikethis', methods=['POST'])
def more_like_this():
    search = Search.from_dict(**request.json)
    return jsonify(search.results)


# endpoint to materials summary
@app.route('/api/materials/<material>', methods=['GET'])
def get_material_summary(material):
    pass


# endpoint to similar materials
@app.route('/api/materials/similar', methods=['GET'])
def get_similar_materials():
    material = request.args.get('material', None)
    if material is None:
        raise StractError("Must supply a material!")
    cutoff = request.args.get('cutoff', None)
    sm = SimilarMaterials()
    return jsonify(sm.get_similar_mats(material))
    # if cutoff is None:
    #     return jsonify(sm.get_similar_mats(material))
    # else:
    #     return jsonify(sm.get_similar_mats(material, cutoff))


# endpoint to embeddings
@app.route('/api/mat2vec/embeddings/<wordphrase>', methods=["Get"])
def retrieve_embeddings(wordphrase):
    wps = wordphrase.split(',')
    embeddings = []
    for wp in wps:
        embeddings.append(Embedding(wp, '', ee.get_word_vector(wp), compound=True))
    return EmbeddingSchema(many=True).jsonify(embeddings)


## TODO: Fix compound vs non-compound embeddings


# endpoint to synonyms
@app.route('/api/mat2vec/synonyms/<wordphrase>', methods=['Get'])
def get_synonyms(wordphrase):
    return jsonify(ee.close_words(wordphrase, top_k=10)[0])


# endpoint to cluster plots
@app.route('/api/plots/cluster', methods=['Get'])
def get_cluster_plot():
    """
    Returns a dictionary that should be the data input to a plotly plot
    The data is a result of 2d tSNE performed on word embeddings, highlighted
    according to the config
    :param config:
    :return:
    """
    request_args = dict()
    for arg in request.args:
        request_args[arg] = request.args.get(arg).split(", ") if arg == "wordphrases" else request.args.get(arg)

    # getting the needed args as a dictionary
    config = ClusterPlotConfigSchema().load(request_args).data
    return jsonify(cp.get_plot_data(**config))


# endpoint to cluster plots
@app.route('/api/plots/trends/', methods=['Get'])
def get_trends_plot(config):
    return NotImplementedError()


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
from stract.api.models import *
from matstract.models.database import AtlasConnection
from matstract.models.word_embeddings import EmbeddingEngine
from matstract.models.search import Search

db = AtlasConnection()
ee = EmbeddingEngine()

app = Flask(__name__)


# endpoint to test
@app.route('/api/test/<message>', methods=["Get"])
def test_api(message):
    messages = message.split(',')
    test = [APITest(message) for message in messages]
    return TestSchema(many=True).jsonify(test)


# endpoint to abstracts
@app.route('/api/abstracts/<abstract_id>', methods=["POST"])
def retrieve_abstracts(abstract_id):
    abstract_ids = abstract_id.split(',')
    entries = db.get_documents_by_id(abstract_ids)
    abstracts = [Abstract(**entry, id=str(entry["_id"])) for entry in entries]
    return AbstractSchema(many=True).jsonify(abstracts)


# endpoint to search
@app.route('/api/search/', methods=['Post'])
def execute_search():
    filter = SearchFilter(**request.json)
    pass


# endpoint to more like this searches
@app.route('/api/morelikethis/', methods=['Post'])
def more_like_this():
    filter = SearchFilter(**request.json)
    conditions = {
        "text": filter.text,
        "material": {"positive": filter.material},
        "property": {"positive": filter.property},
        "application": {"positive": filter.application},
        "characterization": {"positive": filter.characterization}
        # TODO: figure out a better way of doing this
    }
    search = Search.from_dict(conditions)
    return jsonify(search.results)


# endpoint to similar materials
@app.route('/api/materials/similar/<material>', methods=['Get'])
def get_similar_materials(material):
    pass
    # return jsonify(GET_SIMILAR_MATERIALS(material, cutoff)


# endpoint to materials summary
@app.route('/api/materials/<material>', methods=['Get'])
def get_material_summary(material):
    pass


# TODO: Create DB of materials and metadata


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
@app.route('/api/plots/cluster/', methods=['Get'])
def get_cluster_plot(config):
    return NotImplementedError()


# endpoint to cluster plots
@app.route('/api/plots/trends/', methods=['Get'])
def get_trends_plot(config):
    return NotImplementedError()


# # endpoint to synonyms
# @app.route('/api/mat2vec/synonyms/<wordphrase>', methods=['Get'])
# def get_synonyms(wordphrase):
#     print(ee.close_words(wordphrase,  top_k=10))
#     return jsonify(ee.close_words(wordphrase,  top_k=10)[0])

if __name__ == '__main__':
    app.run(debug=True)

from flask_restful import fields

### Still need to figure out marshmallow integration ###

abstract_fields = {
    'id': fields.String,
    'uri': fields.Url('abstracts_endpoint'),
    'title': fields.String,
    'authors': fields.List,
    'year': fields.String,
    'abstract': fields.String,
    'doi': fields.String,
    'journal': fields.String,
    'keywords': fields.List,
    'link': fields.String,
    'source': fields.String(default='scopus'),
}

material_fields = {
    'uri': fields.Url('materials_endpoint'),
    'formula': fields.String,
    'mpid_exists': fields.Boolean,
    'mpid': fields.String,
    'chemical_system': fields.List,
    'properties': fields.List,
    'characterizations': fields.List,
    'phases': fields.List,
    'descriptors': fields.List,
    'applications': fields.List,
    'synthesis': fields.List,
}

search_filter_fields = {
    'text': fields.String,
    'author': fields.List,
    'year': fields.List,
    'journal': fields.List,
    'keywords': fields.List,
    'material': fields.List,
    'formula': fields.List,
    'chemsys': fields.List,
    'property': fields.List,
    'characterization': fields.List,
    'phase': fields.List,
    'descriptor': fields.List,
    'application': fields.List,
    'synthesis': fields.List,
    'sortby': fields.String(default='relevance'),
    'limit': fields.Integer(default=1000)
}

embedding_fields = {
    'uri': fields.Url('embeddings_endpoint'),
    'wordphrase': fields.String,
    'tag': fields.String,
    'embedding': fields.List
}

compound_embedding_fields = {
    'uri': fields.Url('compound_embeddings_endpoint'),
    'wordphrase': fields.String,
    'tag': fields.String,
    'embedding': fields.List
}

clusterplot_config_fields = {
    'heatphrase': fields.String,
    'entity_type': fields.String(default='all'),
    'wordphrases': fields.List,
    'limit': fields.Integer
}

trendsplot_config_fields = {
    'filter': fields.Nested(search_filter_fields),
    'begin': fields.String,
    'end': fields.String,
}

test_fields = {
    'message': fields.String
}
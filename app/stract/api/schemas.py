import marshmallow.fields as fields
from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import URLFor
import numpy as np

# Field options are String, Integer, List, Number, Nested, Url, etc


ma = Marshmallow()

class EntryRequestSchema(ma.Schema):
    ids = fields.List(fields.String())
    fields = fields.List(fields.String())

class AbstractSchema(ma.Schema):
    class Meta:
        # fields to expose
        fields = ('_id', 'title', 'authors', 'abstract', 'year', 'journal', 'keywords', 'doi', 'link')


class MaterialSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('name', 'formula', 'mpid_exists', 'mpid', 'chemical_system', 'properties',
                  'characterizations', 'phases', 'applications', 'descriptors', 'synthesis')


class SearchSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('text', 'author', 'year', 'journal', 'keywords', 'material', 'properties',
                      'characterizations', 'phases', 'applications', 'descriptors', 'synthesis')


class EmbeddingSchema(ma.Schema):
    wordphrase = fields.String()
    tag = fields.String()
    embedding = fields.List(fields.Decimal(as_string=True))
    compound = fields.Boolean(default=False)


class ClusterPlotConfigSchema(ma.Schema):
    heatphrase = fields.String(default=None, missing=None)
    entity_type = fields.String(default='all', missing='all')
    wordphrases = fields.List(fields.String(), default=None, missing=None)
    limit = fields.Integer(default=-1, missing=-1)  # get all
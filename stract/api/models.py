import marshmallow.fields as fields
from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import URLFor
import json
import numpy as np

# Field options are String, Integer, List, Number, Nested, Url, etc

ma = Marshmallow()

class Abstract:
    """
    An abstract and its associated metadata. Mirrors how we store entries in the MongoDB database.
    Used to construct lists of search results.

    """

    _id = fields.String(required=True)
    # uri = URLFor('abstracts_endpoint')
    title = fields.String()
    authors = fields.List(fields.String())
    year = fields.String()
    abstract = fields.String()
    doi = fields.String()
    journal = fields.String()
    keywords = fields.List(fields.String())
    link = fields.String()
    # source = fields.String(default='scopus')


    def __init__(self, _id, title, authors, year, abstract, doi, journal, keywords, link, source='scopus', **kwargs):
        """
        Create an Abstract.

        Args:
            id (str): id of the abstract
            title (str): title of the article
            authors ([str]): list of authors
            year (str): year of publication
            abstract (str): abstract for the article
            doi (str): doi for the article
            journal (str): Journal the paper was published in
            keywords ([str]: Keywords, usually from scopus
            link (str): The url of the paper.
            source (str): Where the abstract was obtained from (Default is "scopus")
        """
        self._id = _id
        self.title = title
        self.authors = authors
        self.abstract = abstract
        self.year = year
        self.journal = journal
        self.keywords = keywords
        self.doi = doi
        # self.source = source
        self.link = link


class AbstractSchema(ma.Schema):
    class Meta:
        # fields to expose
        fields = ('_id', 'title', 'authors', 'abstract', 'year', 'journal', 'keywords', 'doi', 'link')


abstract_shema = AbstractSchema()
abstracts_shema = AbstractSchema(many=True)


class Material:
    """
    A material and all of its associated metadata (chemical system, anonymous formula,
    linked named entities, etc.) Used to construct materials summaries.

    """

    uri = URLFor('materials_endpoint')
    name = fields.String(default="NOT IMPLEMENTED")
    formula = fields.String()
    mpid_exists = fields.Boolean()
    mpid = fields.String()
    chemical_system = fields.List(fields.String())
    properties = fields.List(fields.String())
    characterizations = fields.List(fields.String())
    phases = fields.List(fields.String())
    descriptors = fields.List(fields.String())
    applications = fields.List(fields.String())
    synthesis = fields.List(fields.String())

    def __init__(self, name, formula, mpid_exists, mpid, chemical_system, properties, characterizations, phases,
                 applications, descriptors, synthesis):
        self.name = name
        self.formula = formula
        self.mpid_exists = mpid_exists
        self.mpid = mpid
        self.chemical_system = chemical_system
        self.properties = properties
        self.characterizations = characterizations
        self.phases = phases
        self.applications = applications
        self.descriptors = descriptors
        self.synthesis = synthesis


class MaterialSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('name', 'formula', 'mpid_exists', 'mpid', 'chemical_system', 'properties',
                      'characterizations', 'phases', 'applications', 'descriptors', 'synthesis')


# TODO: Add in models for all entities so we can do more interesting stuff with them.

class SearchFilter:
    """
    Schema for specifying how to filter and sort search results.
    """
    text = fields.String()
    author = fields.List(fields.String())
    year = fields.List(fields.String())
    journal = fields.List(fields.String())
    keywords = fields.List(fields.String())
    material = fields.List(fields.String())
    formula = fields.List(fields.String())
    chemsys = fields.List(fields.String())
    property = fields.List(fields.String())
    characterization = fields.List(fields.String())
    phase = fields.List(fields.String())
    descriptor = fields.List(fields.String())
    application = fields.List(fields.String())
    synthesis = fields.List(fields.String())
    sortby = fields.String(default='relevance')
    limit = fields.Integer(default=1000)

    def __init__(self, text, author, year, journal, keywords, material, properties, characterizations, phases,
                 applications, descriptors, synthesis):
        self.text = text
        self.author = author
        self.year = year
        self.journal = journal
        self.keywords = keywords
        self.material = material
        self.properties = properties
        self.characterizations = characterizations
        self.phases = phases
        self.applications = applications
        self.descriptors = descriptors
        self.synthesis = synthesis


class SearchFilterSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('text', 'author', 'year', 'journal', 'keywords', 'material', 'properties',
                      'characterizations', 'phases', 'applications', 'descriptors', 'synthesis')


class Embedding:
    """
    A Mat2Vec word/phrase embedding. Embeddings are 300-dimensional vectors that represent the meaning
    of words and phrases in a mathematical way. Matstract embeddings are derived from the Word2Vec
    NLP architecture (Google, 2013). If no embedding exists for the single wordphrase, the sum of the embeddings
    of the sub-wordphrases is used.
    """

    uri = URLFor('embeddings_endpoint')
    wordphrase = fields.String()
    tag = fields.String()
    embedding = fields.List(fields.Decimal())
    compound = fields.Boolean(default=False)

    def __init__(self, wordphrase, tag, embedding, compound):
        self.wordphrase = wordphrase
        self.tag = tag
        # ndarrays aren't json serializable, for now we'll just cast to a list.
        if isinstance(embedding, np.ndarray):
            self.embedding = embedding.tolist()
        else:
            self.embedding = embedding
        self.compound = compound

class EmbeddingSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('wordphrase', 'tag', 'embedding', 'compound')


class ClusterPlot:
    """
    A plot which shows how Mat2Vec word/phrase embeddings cluster. The layout of the points on the plot are derived
    using tSNE, which tries to preserve the clustering behavior of the individual word/phrase embeddings in the
    300-dimensional unit hypersphere. Distance between words and location on the 2D plane (other than clustering)
    are not meaningful. Note The graph is stored as a string representation of the dict of Plotly parameters.
    """

    plot = fields.Dict()

    def __init__(self, plot):
        self.plot = plot

class ClusterPlotSchema(ma.Schema):
    plot = fields.Dict()

class ClusterPlotConfig:
    """
    Parameters for constructing cluster plots.
    """

    heatphrase = fields.String()
    entity_type = fields.String(default='all')
    wordphrases = fields.List(fields.String())
    limit = fields.Integer()

    def __init__(self, heatphrase, entity_type, wordphrases, limit):
        self.heatphrase = heatphrase
        self.entity_type = entity_type
        self.wordphrases = wordphrases
        self.limit = limit

class ClusterPlotConfigSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('heatphrase', 'entity_type', 'wordphrases', 'limit')


class TrendsPlot:
    """
    A plot that shows the number of hits per year for a search. For example, this could be a plot of the number
    of times the material LiFePO4 has been mentioned. Note The graph is stored as a string representation of the
    dict of Plotly parameters.
    """

    plot = fields.Dict()

    def __init__(self, plot):
        self.plot = plot

class TrendsPlotSchema(ma.Schema):

    plot = fields.Dict()

class TrendsPlotConfig:
    """
    Parameters for constructing trends plots.
    """

    filter = fields.Nested(SearchFilterSchema())
    begin = fields.String()
    end = fields.String()

    def __init__(self, filter, begin, end):
        self.filter = filter
        self.begin = begin
        self.end = end

class TrendsPlotConfigSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('filter', 'begin', 'end')

class APITest:
    """
    Helps with testing the API
    """

    message = fields.String()

    def __init__(self, message):
        self.message = message

class TestSchema(ma.Schema):
    message = fields.String()
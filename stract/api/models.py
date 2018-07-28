from server import ma
from marshmallow.fields import String, Integer, List, Nested
from flask_marshmallow.fields import URLFor
from marshmallow import post_dump


class Abstract:
    """
    An abstract and its associated metadata. Mirrors how we store entries in the MongoDB database.
    Used to construct lists of search results.

    """

    def __init__(self, id, title, authors, date, abstract, doi, journal, keywords, link, source):
        """
        Create an Abstract.

        Args:
            id (str): id of the abstract
            title (str): title of the article
            authors ([str]): list of authors
            date (str): date of publication
            abstract (str): abstract for the article
            doi (str): doi for the article
            journal (str): Journal the paper was published in
            keywords ([str]: Keywords, usually from scopus
            link (str): The url of the paper.
            source (str): Where the abstract was obtained from (Default is "scopus")
        """
        self.id = id
        self.title = title
        self.authors = authors
        self.abstract = abstract
        self.date = date
        self.journal = journal
        self.keywords = keywords
        self.doi = doi
        self.source = source
        self.link = link


class AbstractSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'authors', 'year', 'abstract', 'doi', 'journal', 'keywords', 'link', 'source')


class Material:
    """
    A material and all of its associated metadata (chemical system, anonymous formula,
    linked named entities, etc.) Used to construct materials summaries.

    """

    def __init__(self, formula, mpid_exists, mpid, chemical_system, properties, characterizations, phases,
                 applications, descriptors, synthesis):
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
        fields = ('formula', 'mpid_exists', 'mpid', 'chemical_system', 'properties',
                      'characterizations', 'phases', 'applications', 'descriptors', 'synthesis')


class SearchFilter:
    """
    Schema for specifying how to filter and sort search results.
    """

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
        fields = ('text', 'author', 'year', 'journal', 'keywords', 'material', 'properties',
                      'characterizations', 'phases', 'applications', 'descriptors', 'synthesis')


class Embedding:
    """
    A Mat2Vec word/phrase embedding. Embeddings are 300-dimensional vectors that represent the meaning
    of words and phrases in a mathematical way. Matstract embeddings are derived from the Word2Vec
    NLP architecture (Google, 2013).
    """

    def __init__(self, wordphrase, tag, embedding):
        self.wordphrase = wordphrase
        self.tag = tag
        self.embedding = embedding

class EmbeddingSchema(ma.Schema):
    class Meta:
        fields = ('wordphrase', 'tag', 'embedding')


class ClusterPlot:
    """
    A plot which shows how Mat2Vec word/phrase embeddings cluster. The layout of the points on the plot are derived
    using tSNE, which tries to preserve the clustering behavior of the individual word/phrase embeddings in the
    300-dimensional unit hypersphere. Distance between words and location on the 2D plane (other than clustering)
    are not meaningful. Note The graph is stored as a string representation of the dict of Plotly parameters.
    """

    def __init__(self, plot):
        self.plot = plot

class ClusterPlotSchema(ma.Schema):
    class Meta:
        fields = ('plot')

class ClusterPlotConfig:
    """
    Parameters for constructing cluster plots.
    """

    def __init__(self, heatphrase, entity_type, wordphrases, limit):
        self.heatphrase = heatphrase
        self.entity_type = entity_type
        self.wordphrases = wordphrases
        self.limit = limit

class ClusterPlotConfigSchema(ma.Schema):
    class Meta:
        fields = ('heatphrase', 'entity_type', 'wordphrases', 'limit')


class TrendsPlot:
    """
    A plot that shows the number of hits per year for a search. For example, this could be a plot of the number
    of times the material LiFePO4 has been mentioned. Note The graph is stored as a string representation of the
    dict of Plotly parameters.
    """

    def __init__(self, plot):
        self.plot = plot

class TrendsPlotSchema(ma.Schema):
    class Meta:
        fields = ('plot')

class TrendsPlotConfig:
    """
    Parameters for constructing trends plots.
    """

    def __init__(self, filter, begin, end):
        self.filter = filter
        self.begin = begin
        self.end = end

class TrendsPlotConfigSchema(ma.Schema):
    class Meta:
        fields = ('filter', 'begin', 'end')

class APITest:
    """
    Helps with testing the API
    """

    def __init__(self, message):
        self.message = message

class TestSchema(ma.Schema):
    class Meta:
        fields = ('message')
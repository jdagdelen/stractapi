from stract.api.models import *
from server import app



# ### Left off here, need to get rid of reqparser and go with marshmallow ###
# class Abstracts:
#
#     def abort_if_abstract_doesnt_exist(self, ids):
#         # If id not found in MongoDB
#         missing = []
#         for id in ids:
#             if id not in atlas:
#                 missing.append(id)
#         if len(missing):
#             abort(status.HTTP_404_NOT_FOUND, message="Cannot find Abstract for id(s) {}".format(missing))
#
#     @marshal_with(abstract_fields)
#     def get(self):
#         ids = parser.parse_args()['abstract_id'].split(',')
#         self.abort_if_abstract_doesnt_exist(ids)
#         return atlas.get(ids), status.HTTP_501_NOT_IMPLEMENTED


#
# class Search(Resource):
#
#     @marshal_with(search_filter_fields)
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('filter', type=dict, required=True, help='Search cannot be empty')
#         args = parser.parse_args()
#         # Execute search using args
#         results = [args]
#         return results, status.HTTP_200_OK
#
#
# class MoreLikeThis(Resource):
#
#     @marshal_with(search_filter_fields)
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('filter', type=dict, required=True, help='Search cannot be empty')
#         args = parser.parse_args()
#         # Execute search using args
#         results = [args]
#         return results, status.HTTP_200_OK
#
#
# class Embeddings(Resource):
#
#     def abort_if_wordphrase_doesnt_exist(self, wordphrases):
#         """
#                Aborts if one or more of the word embeddings is not available for the provided words/phrases.
#                If WORDPHRASE is a multi-word phrase, a compound embedding will NOT be attempted first.
#
#                Args:
#                    wordphrase: (str) One or more words/multi-word phrases.
#
#                Returns:
#                    None
#
#                Calls:
#                    Resource.abort()
#
#                """
#         # if wordphrase is not in our list of embeddings
#         missing = []
#         for wordphrase in wordphrases:
#             # if wordphrase is not in our list of embeddings
#             if wordphrase not in atlas:
#                 missing.append(wordphrase)
#         if len(missing):
#             abort(status.HTTP_404_NOT_FOUND, message="Cannot find Embedding for {}".format(missing))
#
#     def get(self, ids):
#         self.abort_if_wordphrase_doesnt_exist(ids)
#         return atlas.get(ids)
#
#
# class CompoundEmbeddings(Resource):
#
#     def abort_if_wordphrase_doesnt_exist(self, phrases):
#         """
#         Aborts if a word embeddings is not available for one or more of the words in the provided multi-word phrases.
#
#         Args:
#            wordphrase: (str) One or more multi-word phrases.
#
#         Returns:
#            None
#
#         Calls:
#            Resource.abort()
#
#         """
#         # if wordphrase is not in our list of embeddings
#         missing = []
#         for phrase in phrases:
#             # if wordphrase is not in our list of embeddings
#             if phrase not in atlas:
#                 missing.append(phrase)
#         if len(missing):
#             abort(status.HTTP_404_NOT_FOUND, message="Cannot find Embedding for {}".format(missing))
#
#     def get(self, ids):
#         self.abort_if_wordphrase_doesnt_exist(ids)
#         return None, status.HTTP_501_NOT_IMPLEMENTED
#
#
# class Synonyms(Resource):
#     """
#     Get synonyms for a word/phrase.
#     """
#
#     def abort_if_wordphrase_doesnt_exist(self, wordphrase):
#         """
#         Aborts if a word embedding is not available for the provided word/phrase. If WORDPHRASE is a multi-word
#         phrase, a compound embedding will be attempted first.
#
#         Args:
#             wordphrase: (str) A word or multi-word phrase.
#
#         Returns:
#             None
#
#         Calls:
#             Resource.abort()
#
#         """
#         # if wordphrase is not in our list of embeddings
#         if wordphrase not in atlas:
#             abort(status.HTTP_404_NOT_FOUND, message="Cannot find Embedding for {}".format(wordphrase))
#
#     def get(self, wordphrase):
#         self.abort_if_wordphrase_doesnt_exist(wordphrase)
#         # return list of synonyms
#         return None
#
#
# class ClusterPlot(Resource):
#     @marshal_with(clusterplot_config_fields)
#     def get(self, config):
#         #make plotly graph from config
#         plot = [config]
#         return plot, status.HTTP_501_NOT_IMPLEMENTED
#
#
# class TrendsPlot(Resource):
#     @marshal_with(trendsplot_config_fields)
#     def get(self, config):
#         # Search for results
#         plot = [config]
#         return plot, status.HTTP_501_NOT_IMPLEMENTED
#
# class Test(Resource):
#     @marshal_with(test_fields)
#     def get(self, message):
#         return [{'message':message, 'id':1}, {'message':message, 'id':1}]
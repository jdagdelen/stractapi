import os
from flask import Flask
import flask_restful as restful
from flask_pymongo import PyMongo
from flask import make_response
from bson.json_util import dumps

app = Flask(__name__)

def output_json(obj, code, headers=None):
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp

DEFAULT_REPRESENTATIONS = {'application/json': output_json}
api = restful.Api(app)
api.representations = DEFAULT_REPRESENTATIONS

import flask_rest_service.resources

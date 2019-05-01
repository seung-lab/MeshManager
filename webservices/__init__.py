from flask import Flask
from flask_cors import CORS

from . import config

from webservices.meshmanager.app_blueprint import bp
from webservices.skeletonservice.app_blueprint import bps
import logging
import json 
import numpy as np

__version__ = "0.0.1"


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def create_app(test_config=None):
    app = Flask(__name__)
    app.json_encoder = NumpyEncoder
    CORS(app)

    configure_app(app)

    if test_config is not None:
        app.config.update(test_config)

    app.register_blueprint(bp)
    app.register_blueprint(bps)
    app.url_map.strict_slashes = False

    return app


def configure_app(app):

    # Load logging scheme from config.py
    app.config.from_object(config.BaseConfig)

    # Configure logging
    # handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    # handler.setLevel(app.config['LOGGING_LEVEL'])
    # formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    # handler.setFormatter(formatter)
    # app.logger.addHandler(handler)



from flask import Flask
from flask_cors import CORS


from .config import configure_app
from .database import db
from .admin import setup_admin

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

    #configure_app(app)

    if test_config is not None:
        app.config.update(test_config)
    else:
        app = configure_app(app)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        admin = setup_admin(app, db)

    app.register_blueprint(bp)
    app.register_blueprint(bps)
    app.url_map.strict_slashes = False

    return app




import logging
import os
from flask_sqlalchemy import SQLAlchemy 
from emannotationschemas.models import Base



class BaseConfig(object):
    DEBUG = False
    TESTING = False
    HOME = os.path.expanduser("~")
    CORS_HEADERS = 'Content-Type'
    #SECRET_KEY = '1d94e52c-1c89-4515-b87a-f48cf3cb7f0b'
    LOGGING_LEVEL = logging.DEBUG
    STORAGE_CV_PATH = 'file://Users/forrestc/meshmanagerdata'
    INFOSERVICE_URL = "https://www.dynamicannotationframework.com"
    INFOSERVICE_ENDPOINT = "http://info-service/info"

    SQLALCHEMY_DATABASE_URI = "postgresql://analysis_user:connectallthethings@35.196.105.34/postgres"
    DATABASE_CONNECT_OPTIONS = {}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "MYSUPERSECRETTESTINGKEY"

    TEMPFILE_DIR = "skeletons"


def configure_app(app):

    # Load logging scheme from config.py
    app.config.from_object(BaseConfig)
    
    #print(app.config)
    db = SQLAlchemy(model_class=Base)
    db.init_app(app)
    # Configure logging
    # handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    # handler.setLevel(app.config['LOGGING_LEVEL'])
    # formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    # handler.setFormatter(formatter)
    # app.logger.addHandler(handler)

    return app

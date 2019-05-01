from flask import Blueprint, request, make_response, jsonify, g, send_file
from flask import current_app
import json
import time
import datetime
from annotationframeworkclient import infoservice
import cloudvolume
import numpy as np
from meshparty import trimesh_io
from cloudvolume.storage import SimpleStorage
from cachetools import cached, LRUCache, TTLCache
import io
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import gzip 

bps = Blueprint('skeletonservice', __name__, url_prefix="/skeletonservice")
__version__ = "0.0.1"

@bps.route('/', methods=["GET"])
@bps.route("/index", methods=["GET"])
def index():
    return "Skeleton Web Server - version " + __version__

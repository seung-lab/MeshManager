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
import json


def get_datasets():
    url = current_app.config['INFOSERVICE_ENDPOINT'] + "/api/datasets"
    return requests.get(url).json()
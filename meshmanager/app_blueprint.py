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
from StringIO import StringIO
import gzip 

bp = Blueprint('meshmanager', __name__, url_prefix="/meshmanager")
__version__ = "0.0.1"
# -------------------------------
# ------ Access control and index
# -------------------------------


@cached(cache=LRUCache(maxsize=32))
def get_cv_source(dataset):
    info_url = current_app.config['INFOSERVICE_URL']
    infoclient = infoservice.InfoServiceClient(info_url)
    ds_info = infoclient.get_dataset_info(dataset)
    cv_path = ds_info['pychunkedgraph_viewer_source']
    cv_source = cloudvolume.CloudVolumeFactory('graphene://'+cv_path)
    return cv_source


@cached(cache=LRUCache(maxsize=32))
def get_simple_storage():
    local_path = current_app.config['STORAGE_CV_PATH']
    local_storage = SimpleStorage(local_path)
    return local_storage


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


@bp.route('/', methods=["GET"])
@bp.route("/index", methods=["GET"])
def index():
    return "MeshManager Server - version " + __version__


@bp.route
def home():
    resp = make_response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    acah = "Origin, X-Requested-With, Content-Type, Accept"
    resp.headers["Access-Control-Allow-Headers"] = acah
    resp.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    resp.headers["Connection"] = "keep-alive"
    return resp


# -------------------------------
# ------ Measurements and Logging
# -------------------------------

@bp.before_request
def before_request():
    print("NEW REQUEST:", datetime.datetime.now(), request.url)
    g.request_start_time = time.time()


@bp.after_request
def after_request(response):
    dt = (time.time() - g.request_start_time) * 1000

    url_split = request.url.split("/")
    current_app.logger.info("%s - %s - %s - %s - %f.3" %
                            (request.path.split("/")[-1], "1",
                             "".join([url_split[-2], "/", url_split[-1]]),
                             str(request.data), dt))

    print("Response time: %.3fms" % (dt))
    return response


@bp.errorhandler(500)
def internal_server_error(error):
    dt = (time.time() - g.request_start_time) * 1000

    url_split = request.url.split("/")
    current_app.logger.error("%s - %s - %s - %s - %f.3" %
                             (request.path.split("/")[-1],
                              "Server Error: " + error,
                              "".join([url_split[-2], "/", url_split[-1]]),
                              str(request.data), dt))
    return 500


@bp.errorhandler(Exception)
def unhandled_exception(e):
    dt = (time.time() - g.request_start_time) * 1000

    url_split = request.url.split("/")
    current_app.logger.error("%s - %s - %s - %s - %f.3" %
                             (request.path.split("/")[-1],
                              "Exception: " + str(e),
                              "".join([url_split[-2], "/", url_split[-1]]),
                              str(request.data), dt))
    return 500

# -------------------
# ------ Applications
# -------------------

@bp.route('/dataset/<dataset>/<int:seg_id>', methods=['GET'])
def get_mesh(dataset, seg_id):
    cv_source = get_cv_source(dataset)
    local_storage = get_simple_storage()
    local_filepath = f'{dataset}/{seg_id}.gz'
    file_exists = local_storage.files_exist([local_filepath])
    if file_exists[local_filepath]:
        print('file exists')
        content, encoding = local_storage._interface.get_file(local_filepath)
        return send_file(io.BytesIO(bytes(content)),
                         attachment_filename=f'{seg_id}.gz',
                         as_attachment=True)
    else:
        print('downloading mesh')
        mesh_d = cv_source.mesh.get(seg_id=seg_id)
        print('dumping to json')
        str_io = io.BytesIO()
        content = json.dumps(mesh_d, cls=NumpyEncoder)
        gzip_obj = gzip.GzipFile(mode='wb', fileobj=str_io)
        gzip_obj.write(content)

        r=local_storage.put_file(local_filepath, str_io.getvalue())
        print('sending file')
        return send_file(io.BytesIO(content),
                         attachment_filename=f'{seg_id}.gz',
                         as_attachment=True)

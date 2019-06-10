from flask import Blueprint, request, make_response, jsonify, g, send_file, render_template, url_for, redirect
from flask import current_app, send_file
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

from webservices.utils import get_datasets, get_dataset_versions, skeletonizeMesh
from .forms import datasetForm, skeletonizeForm, skeletonViewerForm

from analysisdatalink.datalink_ext import AnalysisDataLinkExt as AnalysisDataLink


bps = Blueprint('skeletonservice', __name__, url_prefix="/skeletonservice", template_folder="templates")
__version__ = "0.0.1"


versions = {}
#versions['basil'] = []
#versions['pinky100'] = [36, 39, 46, 49, 50, 51, 52, 57, 58]



@bps.route('/', methods=["GET"])
@bps.route("/index", methods=["GET"])
def index():
    #return "Skeleton Web Server - version " + __version__
    return render_template('index.html')

@bps.route('/datasets')
def dataset_list():
    datasets, versions = get_datasets()
    return render_template('datasets.html',
                           datasets=datasets,
                           version=__version__)

@bps.route('/form', methods=['GET', 'POST'])
def dataform():
    form = datasetForm()
    data, versions = get_datasets()
    datasets = [(d, d) for d in data]
    form.dataset.choices = datasets 
    
    #form.version.choices = [(v,v) for v in versions[list(versions.keys())[0]]]
    form.version.choices = [(v,v) for v in versions[data[0]]]

    if form.validate_on_submit():
        return redirect(url_for('index'))

    if request.method == 'POST':
        return '<h1>Dataset: {}, Version: {}</h1>'.format(form.dataset.data, form.version.data)

    return render_template('index.html', form=form)


@bps.route('/download/<path:filename>', methods=['GET', 'POST'])
def download_swc(filename):
    return send_file(filename, as_attachment=True)

@bps.route("/view_skeleton/dataset/<dataset>/version/<version>/root_id/<root_id>/somapt_x/<somapt_x>/somapt_y/<somapt_y>/somapt_z/<somapt_z>",
           methods=['GET', 'POST'])
def view_skeleton(dataset, version, root_id, somapt_x, somapt_y, somapt_z):
    dl = AnalysisDataLink(dataset_name=dataset,
                        sqlalchemy_database_uri=current_app.config['SQLALCHEMY_DATABASE_URI'],
                        materialization_version=int(version),
                        verbose=False)
    
    if somapt_x == -1 or somapt_y == -1 or somapt_z == -1:
        somapt_x, somapt_y, somapt_z = dl.query_cell_types('soma_valence').query('pt_root_id == @root_id').item()

    swc_filename = skeletonizeMesh(dataset, int(version), int(root_id), [int(float(somapt_x)), int(float(somapt_y)), int(float(somapt_z))])

    #swc_filename = "skeleton.swc"

    f = open(swc_filename, 'r')
    swcTxt = f.read()

    form = skeletonViewerForm()
    form.swc_input.data = swcTxt

    if request.method == 'POST':
        result = request.form
        return redirect(url_for('skeletonservice.download', filename=result['swc_input']))
    
    return render_template('skeleton_viewer.html', form=form)


@bps.route('/skeletonize', methods=['GET', 'POST'])
def skeletonize_form():
    form = skeletonizeForm()
    data, versions = get_datasets()
    datasets = [(d,d) for d in data]
    form.dataset.choices = datasets 

    if form.validate_on_submit():
        return redirect('.index')

    if request.method == 'POST':
        result = request.form
        #text = ''
        #for k,v in result.items():
        #    text += '<br><h2>{}: {}</h2>'.format(k, v)
        #return text
        if result['somapt_x'] is None:
            result['somapt_x'] = "None"
        if result['somapt_y'] is None:
            result['somapt_y'] = "None"
        if result['somapt_z'] is None:
            result['somapt_z'] = "None"
        return redirect(url_for('skeletonservice.view_skeleton', 
                                dataset=result['dataset'],
                                version=result['version'],
                                root_id=int(result['root_id']),
                                somapt_x=result['somapt_x'],
                                somapt_y=result['somapt_y'],
                                somapt_z=result['somapt_z']))
    
    return render_template('skeletonize_form.html', form=form)


@bps.route('/version/<dataset_name>')
def dataset_version(dataset_name):
    
    dversion = get_dataset_versions(dataset_name)
    darray = []
    
    for v in dversion:
        dobj = {}
        dobj['id'] = v
        dobj['name'] = v
        darray.append(dobj)

    return jsonify({'versions': darray})
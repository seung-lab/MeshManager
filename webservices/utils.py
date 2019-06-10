import cloudvolume
import numpy as np
import io
import json
import time 
import requests
import pandas as pd
from scipy import sparse 
from cachetools import cached, LRUCache, TTLCache

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from flask import current_app
from webservices.database import db

from annotationframeworkclient import infoservice
from cloudvolume.storage import SimpleStorage
from emannotationschemas import get_types, get_schema
from emannotationschemas.models import AnalysisTable, AnalysisVersion
from meshparty import trimesh_io, trimesh_vtk, skeletonize, skeleton 
from annotationframeworkclient.infoservice import InfoServiceClient
from analysisdatalink.datalink_base import get_materialization_versions

#from materializationengine.schemas import AnalysisVersionSchema, AnalysisTableSchema
#from emannotationschemas.models import make_annotation_model, make_dataset_models, declare_annotation_model


def get_datasets():
    info_client = InfoServiceClient(current_app.config['INFOSERVICE_URL'])
    datasets = info_client.get_datasets()
    
    versions = {}
    for dataset in datasets:
        versions[dataset] = get_dataset_versions(dataset)
    
    return datasets, versions

'''
def get_dataset_versions(dataset_name):
    versions = (AnalysisVersion.query.filter(
        AnalysisVersion.dataset == dataset_name).
        order_by(AnalysisVersion.version.desc()).all())
    
    return versions
'''

def get_dataset_versions(dataset_name):
    version = []
    version = get_materialization_versions(dataset_name)
    
    return version.keys()


def skeletonizeMesh(dataset_name, mat_version, seg_id, soma_pt, soma_thresh=15000, invalidation_d=12000):
    info_client = InfoServiceClient(current_app.config['INFOSERVICE_URL'])
    ds_info = info_client.get_dataset_info(dataset_name)

    soma_pt = np.array(soma_pt)*[4, 4, 40]

    mm = trimesh_io.MeshMeta(cv_path = ds_info['graphene_source'],
                             map_gs_to_https=True,
                             cache_size=0,
                             disk_cache_path='meshes') # disk_cache_path needs to be update appropriately

    cell_mesh = mm.mesh(seg_id = seg_id, 
                        remove_duplicate_vertices=False,
                        merge_large_components=False,
                        masked_mesh=True)

    cell_mesh.add_link_edges(seg_id, dataset_name)

    new_ccs, new_labels = sparse.csgraph.connected_components(cell_mesh.csgraph, return_labels=True)
    uniq_labels, label_counts = np.unique(new_labels, return_counts=True)
    new_mesh_filt = cell_mesh.apply_mask(new_labels==uniq_labels[np.argmax(label_counts)])

    skel_verts, skel_edges, smooth_verts, skel_map = skeletonize.skeletonize_mesh(new_mesh_filt,
                                                                        soma_pt=soma_pt,
                                                                        soma_thresh=soma_thresh,
                                                                        invalidation_d=invalidation_d,
                                                                        merge_components_at_tips=False)

    tot_skeleton = skeleton.Skeleton(skel_verts, skel_edges)

    filename = "skeleton.swc"
    tot_skeleton.export_to_swc(filename)


    return filename

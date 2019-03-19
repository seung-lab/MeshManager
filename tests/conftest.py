import pytest
from meshmanager import create_app
import subprocess
from time import sleep
import os

INFOSERVICE_ENDPOINT = "https://www.dynamicannotationframework.com"
tempdir = tempfile.mkdtemp()
TEST_PATH = "file:/{}".format(tempdir)

def mock_info_service(requests_mock):
    dataset_url = os.path.join(INFOSERVICE_ENDPOINT, 'api/datasets')
    requests_mock.get(dataset_url, json=[TEST_DATASET_NAME])
    dataset_info_url = os.path.join(INFOSERVICE_ENDPOINT,
                                    'api/dataset/{}'.format(TEST_DATASET_NAME))
    dataset_d = {
        "annotation_engine_endpoint": "http://35.237.200.246",
        "flat_segmentation_source": TEST_PATH,
        "id": 1,
        "image_source": TEST_PATH,
        "name": TEST_DATASET_NAME,
        "pychunkgraph_endpoint": "http://pcg/segmentation",
        "pychunkgraph_segmentation_source": TEST_PATH
    }
    requests_mock.get(dataset_info_url, json=dataset_d)

@pytest.fixture(scope='session')
def test_dataset():
    return 'test'

@pytest.fixture(scope='session')
def local_mesh_folder(tmpdir_factory):
    tmpdir = str(tmpdir_factory.mktemp('test_mesh_local_storage'))
    yield tmpdir

@pytest.fixture(scope='session')
def cv_folder(tmpdir_factory):
    tmpdir = str(tmpdir_factory.mktemp('test_cv_path'))
    yield tmpdir


@pytest.fixture(scope='session')
def app(settings, local_mesh_folder):
    app = create_app(
        {
            'TESTING': True,
            'INFOSERVICE_URL': INFOSERVICE_ENDPOINT,
            'STORAGE_CV_PATH': "file://"+str(local_mesh_folder),
            'SECRET_KEY': 'xxxxx'
        }
    )

    yield app


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()

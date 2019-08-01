from setuptools import setup
import re
import os
import codecs
from setuptools.command.test import test as TestCommand
import sys


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()

with open('requirements.txt', 'r') as f:
    required = f.read().splitlines()

setup(
    use_scm_version=True,
    name='meshmanager',
    description='a service for managing skeletons',
    author='Gayathri Mahalingam',
    author_email='gayathrim@alleninstitute.org',
    url='https://github.com/seung-lab/MeshManager.git',
    packages=['webservices'],
    include_package_data=True,
    install_requires=required,
    setup_requires=['pytest-runner']
)

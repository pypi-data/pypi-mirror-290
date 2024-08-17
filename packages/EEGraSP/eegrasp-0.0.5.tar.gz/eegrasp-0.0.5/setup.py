#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import find_packages, setup


def read_license():
    license_path = os.path.join(os.path.dirname(__file__), 'LICENSE')
    if os.path.exists(license_path):
        with open(license_path, 'r') as file:
            return file.read().strip()
    return 'MIT'


setup(
    name='eegrasp',
    version='v0.0.5',
    description='Graph Signal Processing in Python',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    author='GSP EEG',
    url='https://github.com/gsp-eeg/EEGrasp',
    project_urls={
        'Documentation': 'https://eegrasp.readthedocs.io',
        'Download': 'https://pypi.org/project/eegrasp',
        'Source Code': 'https://github.com/gsp-eeg/eegrasp',
        'Bug Tracker': 'https://github.com/gsp-eeg/eegrasp/issues',
        #'Try It Online': 'https://mybinder.org/v2/gh/epfl-lts2/eegrasp/master?urlpath=lab/tree/examples/playground.ipynb',
    },
    packages=[
        'eegrasp',
        'eegrasp.tests',
    ],
    package_data={'eegrasp': ['data/pointclouds/*.mat']},
    test_suite='eegrasp.tests.suite',
    python_requires='>=3.11',
    install_requires=[
        'numpy',
        'matplotlib',
        'pylint',
        'tqdm',
        'mne',
        'joblib',
        'scipy',
        'pandas',
        'pygsp2',
        'numpydoc',
    ],
    extras_require={
        # Optional dependencies for development. Some bring additional
        # functionalities, others are for testing, documentation, or packaging.
        'dev': [
            'numpy',
            'matplotlib',
            'pylint',
            'tqdm',
            'mne',
            'joblib',
            'scipy',
            'pandas',
            'pygsp2',
            # Import and export.
            'networkx',
            #'json',
            'utm',
            'geopy',
            'pyxlsb',
            'unidecode',
            # 'graph-tool', cannot be installed by pip
            # Construct patch graphs from images.
            'scikit-image',
            # Approximate nearest neighbors for kNN graphs.
            'pyflann3',
            # Convex optimization on graph.
            'pyunlocbox',
            # Plot graphs, signals, and filters.
            'matplotlib',
            # Interactive graph visualization.
            'pyqtgraph',
            'PyOpenGL',
            'PyQt5',
            # Run the tests.
            'flake8',
            'coverage',
            'coveralls',
            # Build the documentation.
            'sphinx',
            'numpydoc',
            'sphinxcontrib-bibtex',
            'sphinx-gallery',
            'memory_profiler',
            'sphinx-rtd-theme',
            'sphinx-copybutton',
            # Build and upload packages.
            'wheel',
            'twine',
            'ruff',
            'codespell',
            'tomli',
            'isort',
            'toml',
            'yapf'
        ],
    },
    keywords='graph signal processing',
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Scientific/Engineering',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: ' + read_license(),
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)

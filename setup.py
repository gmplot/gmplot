import os
from setuptools import setup, find_packages

__version__ = '1.4.1'

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

def get_requirements(requirements_file):
    with open(requirements_file) as f:
        return f.read().strip().splitlines()

setup(
    name = 'gmplot',
    version = __version__,
    author = 'gmplot contributors',
    description = 'A matplotlib-like interface to plot data with Google Maps.',
    long_description=read('README.rst'),
    license='MIT',
    keywords='python google-maps visualization',
    packages = find_packages(),
    include_package_data=True,
    package_data = {
        'gmplot': ['markers/*.png'],
    },
    project_urls = {
        'Documentation': 'https://github.com/gmplot/gmplot/wiki',
        'Tracker': 'https://github.com/gmplot/gmplot/issues',
        'Source': 'https://github.com/gmplot/gmplot'
    },
    install_requires=get_requirements('requirements.txt'),
    classifiers = ['Programming Language :: Python :: %s' % version for version in ['2', '2.7', '3', '3.5', '3.6', '3.7', '3.8']]
)

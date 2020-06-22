import os
from setuptools import setup, find_packages

__version__ = '1.3.1'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def get_requirements(requirements_file):
    with open(requirements_file) as f:
        return f.read().strip().splitlines()

setup(
    name = 'gmplot',
    version = __version__,
    author = 'gmplot contributors',
    url = 'https://github.com/gmplot/gmplot',
    description = 'A matplotlib-like interface to plot data with Google Maps.',
    long_description=read('README.rst'),
    license='MIT',
    keywords='python google-maps visualization',
    packages = find_packages(),
    include_package_data=True,
    package_data = {
        'gmplot': ['markers/*.png'],
    },
    install_requires=get_requirements('requirements.txt'),
)

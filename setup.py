import os
from setuptools import setup, find_packages

__version__ = '1.0.2'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'aviplot',
    version = __version__,
    author = 'Avijit Ghosh',
    author_email = 'avijitg22@gmail.com',
    url = 'https://github.com/AvijitGhosh82/aviplot',
    description = 'Provide a matplotlib like interface to plotting data with Google Maps',
    long_description=read('README.rst'),
    license='MIT',
    keywords='python wrapper google maps',
    packages = find_packages(),
    include_package_data=True,
    package_data = {
        'aviplot': ['markers/*.png'],
    },
    install_requires=['requests'],
)

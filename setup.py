import os
from setuptools import setup, find_packages

__version__ = '1.2.0'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'gmplot',
    version = __version__,
    author = 'Michael Woods',
    author_email = 'physicsmichael@gmail.com',
    url = 'https://github.com/vgm64/gmplot',
    description = 'Provide a matplotlib like interface to plotting data with Google Maps',
    long_description=read('README.rst'),
    license='MIT',
    keywords='python wrapper google maps',
    packages = find_packages(),
    include_package_data=True,
    package_data = {
        'gmplot': ['markers/*.png'],
    },
    install_requires=['requests'],
)

import os
from distutils.core import setup

__version__ = '0.0.1'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'gmplot',
    version = __version__,
    author = 'Michael Woods',
    author_email = 'physicsmichael@gmail.com',
    url = 'https://github.com/vgm64/gmplot',
    py_modules = ['gmplot'],
    description = 'Provide a matplotlib like interface to plotting data with Google Maps',
    long_description=read('README.rst'),
    license='MIT',
    keywords='python wrapper google maps',

)

### Configuration file for the Sphinx documentation builder.

# Set up the path:
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# Configure base functionality:
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.coverage',
    'sphinx_markdown_builder',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'Home'

# Configure extensions:
autoclass_content = 'both'

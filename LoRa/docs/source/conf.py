# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'LoRa'
copyright = '2023, Thomas Kidd & Hunter Green'
author = 'Thomas Kidd & Hunter Green'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join('..', '..')))

extensions = [ 'myst_parser',
               'sphinx.ext.graphviz',
               'sphinxcontrib.plantuml',
              ]

extensions.append('autoapi.extension')
autoapi_type = 'python'
autoapi_dirs = ['/home/tk/Work/ComsBoard/LoRa/RpiTesting/RN2903/RpiMaster/src/',
                '/home/tk/Work/ComsBoard/LoRa/RpiTesting/RN2903/RpiMaster/Libraries/',
                '/home/tk/Work/ComsBoard/LoRa/RpiTesting/RYLR998/src/',
                '/home/tk/Work/ComsBoard/LoRa/RpiTesting/RYLR998/Libraries/',]

autoapi_python_class_content = "class"

templates_path = ['_templates']
exclude_patterns = []

language = 'python'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']

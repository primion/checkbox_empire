# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath('../..'))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Checkbox Empire'
copyright = '2023, Thorsten Sick, Primion'
author = 'Thorsten Sick'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

autodoc_default_options = {
    'member-order': 'bysource',
}

# Sphinx argparse https://sphinx-argparse.readthedocs.io/en/latest/install.html
extensions += ['sphinxarg.ext']

# UML diagrams https://github.com/alendit/sphinx-pyreverse
extensions += ['sphinx_pyreverse']

# YAML config file documentation https://github.com/Jakski/sphinxcontrib-autoyaml
extensions += ['sphinxcontrib.autoyaml']
autoyaml_level = 5

# Graphviz
extensions += [
    "sphinx.ext.graphviz"
]

# -- GraphViz configuration ----------------------------------
graphviz_output_format = 'svg'


templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'whatstk'
copyright = '2020, lucasrodes'
author = 'lucasrodes'

# The full version, including alpha/beta/rc tags
release = '0.3.0.dev1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    'sphinx.ext.githubpages',
    'sphinx.ext.autosummary',
    'sphinx_rtd_theme',
    'sphinx_copybutton',
    'sphinx.ext.autosectionlabel',
    'sphinx_git'
]

# The name of the entry point, without the ".rst" extension.
# By convention this will be "index"
master_doc = "source/content"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '../../setup.py']
EXCLUDE_PATTERN = ['../setup.py']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
# html_theme = 'python_docs_theme'
# html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Copybutton ---------------------------------------------------------------
copybutton_prompt_text = ">>>"


# -- Theme --------------------------------------------------------------------
def setup(app):
    app.add_stylesheet('css/custom.css')


html_title = "WhatsApp Analysis Toolkit"
html_logo = "../assets/logo.png"
html_favicon = "_static/favicon.png"

html_show_sourcelink = False
html_copy_source = True

# github_url = 'https://github.com/lucasrodes/whatstk'

html_theme_options = {
    'logo_only': True,
    'display_version': True,
    'navigation_depth': 10,
    'display_version': True,
    'collapse_navigation': False,
    'sticky_navigation': False
}

# -- Args ---------------------------------------------------------------------
html4_writer = True
napoleon_use_rtype = False
autosummary_generate = True
